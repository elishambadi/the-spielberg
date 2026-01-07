from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from anthropic import Anthropic
from .models import ScriptProject

def index(request):
    """Main view for the script writing interface"""
    projects = ScriptProject.objects.all()
    return render(request, 'scriptwriter/index.html', {'projects': projects})

@csrf_exempt
@require_http_methods(["POST"])
def generate_script(request):
    """API endpoint to generate script using Claude AI"""
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        prompt = data.get('prompt')
        script_type = data.get('script_type', 'screenplay')
        
        if not api_key or not prompt:
            return JsonResponse({
                'error': 'API key and prompt are required'
            }, status=400)
        
        # Initialize Claude AI client
        client = Anthropic(api_key=api_key)
        
        # System prompt for script writing
        system_prompt = get_script_writing_system_prompt(script_type)
        
        # Generate script using Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        script_content = message.content[0].text
        
        return JsonResponse({
            'success': True,
            'script': script_content
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_script(request):
    """Save a script project"""
    try:
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        genre = data.get('genre', '')
        logline = data.get('logline', '')
        
        script = ScriptProject.objects.create(
            title=title,
            content=content,
            genre=genre,
            logline=logline
        )
        
        return JsonResponse({
            'success': True,
            'id': script.id
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

def get_script_writing_system_prompt(script_type):
    """Get the system prompt for script writing based on type"""
    
    base_prompt = """You are an expert screenwriter and script consultant with deep knowledge of storytelling, 
    character development, and screenplay formatting. You understand the principles of dramatic structure, 
    including the three-act structure, character arcs, and compelling dialogue."""
    
    if script_type == 'screenplay':
        return base_prompt + """

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
        return base_prompt + """

TREATMENT FORMAT:
- Write in present tense, third person
- Describe the story chronologically from beginning to end
- Include major plot points, character arcs, and turning points
- Paint a vivid picture of the story world
- Convey the tone and style of the piece
- No dialogue, just narrative description
- 3-5 pages for a short treatment, 10-30 for a full treatment

Focus on compelling story structure and emotional journey."""
    
    else:  # outline
        return base_prompt + """

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
