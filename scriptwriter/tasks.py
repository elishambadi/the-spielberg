"""
Celery tasks for async script generation.
"""
from celery import shared_task
from django.utils import timezone
from anthropic import Anthropic
import os
import re
import uuid
from .models import Job, Script, ScriptVersion, Scene, Character


def detect_incomplete_content(content):
    """
    Detect if content was cut off mid-generation.
    Returns True if content appears incomplete.
    """
    if not content:
        return False
    
    content = content.strip()
    
    # Check for common cutoff indicators
    indicators = [
        # Cut off mid-sentence
        not content.endswith(('.', '!', '?', '"', ')', ']', 'OUT.', 'FADE OUT.', 'THE END')),
        # Cut off mid-dialogue
        content.count('"') % 2 != 0,  # Odd number of quotes
        # Cut off mid-action line
        content.endswith(('that', 'and', ' but', ' the', ' a', ' an', ' is', ' are', ' was', ' were', 'if', 'then', 'when', 'while', 'because', 'as', 'so', 'after', 'before', 'until', 'although', 'though', 'unless', 'whereas')),
        # Cut off mid-scene heading
        bool(re.search(r'(INT\.|EXT\.)(?!\s+\w+\s+-\s+\w+)', content[-100:])),
        # Ends with incomplete character name (caps line without dialogue)
        bool(re.search(r'\n[A-Z\s]{3,}\n*$', content[-50:])),
    ]
    
    return any(indicators)


def combine_content_parts(previous_content, new_content):
    """
    Intelligently combine continuation with previous content.
    """
    if not previous_content:
        return new_content
    
    # Remove common continuation artifacts
    new_content = new_content.strip()
    
    # If new content starts with a repeat of the last line, remove it
    last_lines = previous_content.strip().split('\n')[-3:]
    for i, line in enumerate(last_lines):
        if new_content.startswith(line.strip()):
            # Found a repeat, skip past it
            new_content = '\n'.join(new_content.split('\n')[1:])
            break
    
    return previous_content + "\n" + new_content


def get_script_writing_system_prompt(script_type='screenplay', genre='', tone='', characters=None):
    """Get the system prompt for script writing based on type"""
    
    base_prompt = """You are an expert screenwriter and script consultant with deep knowledge of storytelling, 
    character development, and screenplay formatting. You understand the principles of dramatic structure, 
    including the three-act structure, character arcs, and compelling dialogue."""
    
    # Add genre and tone context
    if genre:
        base_prompt += f"\n\nThis is a {genre} script."
    if tone:
        base_prompt += f" The tone should be {tone}."
    
    # Add character context
    if characters:
        base_prompt += "\n\nCHARACTERS IN THIS SCRIPT:\n"
        for char in characters:
            base_prompt += f"\n{char.name}:"
            if char.personality:
                base_prompt += f"\n  Personality: {char.personality}"
            if char.goals:
                base_prompt += f"\n  Goals: {char.goals}"
            if char.voice:
                base_prompt += f"\n  Voice: {char.voice}"
            if char.backstory:
                base_prompt += f"\n  Backstory: {char.backstory}"
    
    if script_type == 'screenplay':
        base_prompt += """

SCREENPLAY FORMAT RULES:
1. Use proper screenplay formatting with scene headings, action lines, character names, and dialogue
2. Scene headings: INT./EXT. LOCATION - TIME OF DAY (e.g., INT. COFFEE SHOP - DAY)
3. Action lines: Present tense, active voice, describing what we see and hear
4. Character names: ALL CAPS when they first appear and above dialogue
5. Dialogue: Character name centered, dialogue below
6. Parentheticals: Brief direction for how a line should be delivered
7. Transitions: FADE IN:, CUT TO:, FADE OUT: (use sparingly)

STORYTELLING PRINCIPLES:
- Strong opening hook that establishes the world and protagonist
- Clear character motivations and goals
- Rising tension and conflict
- Well-paced scenes with purpose
- Subtext in dialogue - show don't tell
- Visual storytelling over exposition
- Satisfying character arcs
- Three-act structure: Setup, Confrontation, Resolution

Generate professional, properly formatted screenplay content. Focus on vivid visual storytelling, 
authentic dialogue, and compelling character development."""
    
    elif script_type == 'treatment':
        base_prompt += """

TREATMENT FORMAT:
- Write in present tense, third person
- Describe the story chronologically from beginning to end
- Include major plot points, character arcs, and turning points
- Paint a vivid picture of the story world
- Convey the tone and style of the piece
- No dialogue, just narrative description
- 3-5 pages for a short treatment, 10-30 for a full treatment

Focus on compelling story structure and emotional journey."""
    
    elif script_type == 'scene':
        base_prompt += """

SCENE GENERATION:
- Write a complete, well-structured scene
- Include proper scene heading
- Clear visual action and character behavior
- Authentic dialogue with subtext
- Scene should have a clear beginning, middle, and end
- Advance the plot or develop character
- Maintain consistent tone and pacing"""
    
    else:  # outline
        base_prompt += """

OUTLINE FORMAT:
- Organized by acts and sequences
- Clear beat sheet of major story moments
- Character introductions and arc progressions
- Key plot points and turning points
- Theme development
- Conflict escalation

Structure:
ACT ONE: Setup
- Opening Image
- Inciting Incident
- First Plot Point

ACT TWO: Confrontation
- Rising Action
- Midpoint
- Complications
- Crisis

ACT THREE: Resolution
- Climax
- Falling Action
- Resolution
- Closing Image

Provide a comprehensive story outline with dramatic beats."""
    
    return base_prompt


@shared_task(bind=True)
def generate_script_task(self, job_id, prompt, script_id=None, script_type='screenplay', continuation_of=None):
    """
    Async task to generate a script using Claude AI.
    Supports automatic continuation if content is cut off.
    """
    try:
        job = Job.objects.get(job_id=job_id)
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        # Get script and related data if provided
        script = None
        characters = []
        genre = ''
        tone = ''
        
        if script_id:
            script = Script.objects.get(id=script_id)
            characters = list(script.characters.all())
            genre = script.get_genre_display()
            tone = script.get_tone_display()
        
        # Handle continuation
        previous_content = ""
        if continuation_of:
            parent_job = Job.objects.get(job_id=continuation_of)
            previous_content = parent_job.result
            job.is_continuation = True
            job.parent_job = parent_job
            job.continuation_count = parent_job.continuation_count + 1
            job.save()
        
        # Get API key from environment
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        # Initialize Claude AI client
        client = Anthropic(api_key=api_key)
        
        # System prompt for script writing
        system_prompt = get_script_writing_system_prompt(
            script_type=script_type,
            genre=genre,
            tone=tone,
            characters=characters
        )
        
        # Build prompt based on whether this is a continuation
        if continuation_of:
            # For continuations, provide context and ask to continue
            last_500_chars = previous_content[-500:] if len(previous_content) > 500 else previous_content
            full_prompt = f"""CONTINUATION REQUEST:

The story so far (last 500 characters):
\"\"\"
{last_500_chars}
\"\"\"

Continue from exactly where it left off. Do not repeat what was already written. Pick up mid-sentence if necessary and continue the story naturally. Complete the section requested in the original prompt:

{prompt}

IMPORTANT: Continue seamlessly from where it stopped. Finish the current scene/act properly."""
        else:
            # Original generation
            full_prompt = f"{script.logline}\n\n{prompt}\n\nIMPORTANT: Ensure you complete the entire section/act requested. If approaching token limits, prioritize finishing the current scene or beat properly rather than cutting off mid-dialogue or mid-action."
        
        # Generate script using Claude
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=8192,
            system=system_prompt,
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            stream=False
        )
        
        script_content = message.content[0].text
        
        # Combine with previous content if continuation
        if continuation_of:
            script_content = combine_content_parts(previous_content, script_content)
        
        # Check if content is still incomplete (max 3 continuations)
        if detect_incomplete_content(script_content) and job.continuation_count < 3:
            # Save current progress
            job.status = 'completed'
            job.result = script_content
            job.completed_at = timezone.now()
            job.save()
            
            # Automatically create continuation job
            continuation_job_id = str(uuid.uuid4())
            continuation_job = Job.objects.create(
                user=job.user,
                job_id=continuation_job_id,
                job_type=job.job_type,
                status='pending',
                prompt=prompt,
                script_id=script_id,
                scene_id=job.scene_id,
                is_continuation=True,
                parent_job=job,
                continuation_count=job.continuation_count + 1
            )
            
            # Enqueue continuation task
            generate_script_task.delay(
                continuation_job_id, 
                prompt, 
                script_id, 
                script_type, 
                continuation_of=job_id
            )
            
            return {
                'status': 'continued',
                'result': script_content,
                'continuation_job_id': continuation_job_id
            }
        
        # Update job with result
        job.status = 'completed'
        job.result = script_content
        job.completed_at = timezone.now()
        job.save()
        
        # If script is provided, create a new version (only for original job, not continuations)
        if script and not continuation_of:
            latest_version = script.get_latest_version()
            version_number = (latest_version.version_number + 1) if latest_version else 1
            
            ScriptVersion.objects.create(
                script=script,
                version_number=version_number,
                content=script_content
            )
        elif script and continuation_of:
            # Update the existing version with the complete content
            latest_version = script.get_latest_version()
            if latest_version:
                latest_version.content = script_content
                latest_version.save()
        
        return {'status': 'completed', 'result': script_content}
        
    except Exception as e:
        # Update job with error
        job = Job.objects.get(job_id=job_id)
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        return {'status': 'failed', 'error': str(e)}


@shared_task(bind=True)
def generate_scene_task(self, job_id, scene_id, prompt):
    """
    Async task to generate or regenerate a scene.
    """
    try:
        job = Job.objects.get(job_id=job_id)
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        scene = Scene.objects.get(id=scene_id)
        script_version = scene.script_version
        script = script_version.script
        
        # Get characters
        characters = list(script.characters.all())
        
        # Get API key from environment
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        # Initialize Claude AI client
        client = Anthropic(api_key=api_key)
        
        # Build scene-specific prompt
        scene_context = f"""
Scene {scene.scene_number}:
Setting: {scene.setting}
Goal: {scene.goal}
Tension: {scene.tension}
"""
        if scene.tone:
            scene_context += f"Tone: {scene.tone}\n"
        
        full_prompt = scene_context + "\n\n" + prompt + "\n\nIMPORTANT: Complete the entire scene properly with a clear beginning, middle, and end. Do not cut off mid-dialogue."
        
        # System prompt for scene writing
        system_prompt = get_script_writing_system_prompt(
            script_type='scene',
            genre=script.get_genre_display(),
            tone=scene.tone or script.get_tone_display(),
            characters=characters
        )
        
        # Generate scene using Claude
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,  # Scenes are shorter, 4096 should be sufficient
            system=system_prompt,
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            stream=False
        )
        
        scene_content = message.content[0].text
        
        # Update scene
        scene.content = scene_content
        scene.save()
        
        # Update job with result
        job.status = 'completed'
        job.result = scene_content
        job.completed_at = timezone.now()
        job.save()
        
        return {'status': 'completed', 'result': scene_content}
        
    except Exception as e:
        # Update job with error
        job = Job.objects.get(job_id=job_id)
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        return {'status': 'failed', 'error': str(e)}
