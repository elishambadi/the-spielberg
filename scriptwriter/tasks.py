"""
Celery tasks for async script generation.
"""
from celery import shared_task
from django.utils import timezone
from anthropic import Anthropic
import os
from .models import Job, Script, ScriptVersion, Scene, Character


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
def generate_script_task(self, job_id, prompt, script_id=None, script_type='screenplay'):
    """
    Async task to generate a script using Claude AI.
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
        
        # Generate script using Claude
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        script_content = message.content[0].text
        
        # Update job with result
        job.status = 'completed'
        job.result = script_content
        job.completed_at = timezone.now()
        job.save()
        
        # If script is provided, create a new version
        if script:
            latest_version = script.get_latest_version()
            version_number = (latest_version.version_number + 1) if latest_version else 1
            
            ScriptVersion.objects.create(
                script=script,
                version_number=version_number,
                content=script_content
            )
        
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
        
        full_prompt = scene_context + "\n\n" + prompt
        
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
            max_tokens=2048,
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
