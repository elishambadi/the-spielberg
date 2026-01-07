# Example Usage Guide

## Quick Start Example

Here's a step-by-step guide to generate your first script:

### 1. Get Your Claude API Key
- Visit https://console.anthropic.com/
- Create an account or log in
- Navigate to API Keys section
- Create a new API key (starts with `sk-ant-`)

### 2. Launch the Application
```bash
python manage.py runserver
```
Navigate to: http://127.0.0.1:8000/

### 3. Example Prompts

#### Example 1: Opening Scene (Screenplay)
**Script Type:** Screenplay (Full Format)

**Prompt:**
```
Write the opening scene of a psychological thriller. A therapist arrives at her office 
to find all her patient files scattered across the floor. She doesn't remember leaving 
them that way. Include atmospheric description and her internal conflict.
```

**Expected Output:** Properly formatted screenplay with scene heading, action lines, and if appropriate, inner thoughts or dialogue.

#### Example 2: Full Story Treatment
**Script Type:** Treatment (Narrative)

**Prompt:**
```
A treatment for a 90-minute romantic comedy about a wedding planner who accidentally 
books the same venue twice - once for her best friend's wedding and once for her ex-boyfriend's 
wedding on the same day. Tell the complete story from setup through resolution.
```

**Expected Output:** Narrative prose describing the complete story arc.

#### Example 3: Story Outline
**Script Type:** Outline (Story Beats)

**Prompt:**
```
Create a detailed outline for an action-adventure film about a retired treasure hunter 
forced back into the game when her daughter is kidnapped by a rival seeking a legendary artifact.
```

**Expected Output:** Structured act breakdown with key plot points.

## Tips for Better Results

### Be Specific
❌ "Write a scene about a detective"
✅ "Write a scene where a detective interviews a nervous witness in a dimly lit interrogation room. The witness knows more than they're saying."

### Set the Tone
Include descriptive words like:
- Genre: noir, comedy, horror, sci-fi, drama
- Mood: tense, lighthearted, mysterious, emotional
- Style: Tarantino-esque, Hitchcockian, documentary-style

### Specify Format Needs
- "Include dialogue between two characters"
- "Focus on visual action, minimal dialogue"
- "Show the character's internal struggle"
- "Create a montage sequence"

## Advanced Examples

### Complex Scene with Multiple Elements
```
Write the climactic scene of a heist film. The crew of five thieves must work together 
to crack a vault in real-time while security closes in. Include:
- Cross-cutting between the tech expert on comms and the safecracker
- Rising tension through short, punchy dialogue
- Visual details of the vault mechanism
- A twist when they discover the vault is empty
```

### Character-Driven Drama
```
Write a two-person scene between a mother and daughter meeting after 10 years of estrangement. 
They're at a neutral location - a coffee shop. Neither knows what to say first. The daughter 
came to tell her mother something important. Show subtext through what they don't say.
```

### Genre-Specific Formatting
```
Write the opening of a horror screenplay set in an abandoned asylum. Use classic horror 
screenplay techniques: slow build of dread, environmental storytelling through production 
design details, and a shocking ending to the sequence.
```

## Troubleshooting

### "API key required" Error
- Make sure you've pasted your API key in the field
- Verify the key starts with `sk-ant-`
- Check that there are no extra spaces

### Script Seems Generic
- Add more specific details to your prompt
- Include character descriptions
- Specify the exact moment in the story
- Reference tone and style inspirations

### Formatting Issues
- The system prompts are designed for proper formatting
- If format isn't right, try specifying: "Use standard screenplay format"
- For treatments, remind: "Write in prose, not script format"

## Saving Your Work

1. After generation, click **💾 Save**
2. Enter a memorable title
3. Scripts are saved with:
   - Title
   - Content
   - Script type (as genre)
   - Your original prompt (as logline)

4. Access saved scripts through Django admin:
   - Navigate to: http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - View all saved scripts in ScriptProject section

## Export Options

- **Copy to Clipboard**: Click 📋 Copy to copy the entire script
- **Paste into**: 
  - Final Draft
  - Celtx  
  - WriterDuet
  - Any text editor

## Best Practices

1. **Start Small**: Begin with a single scene, not an entire screenplay
2. **Iterate**: Generate multiple versions, refine your prompt
3. **Be Specific**: More details = better results
4. **Save Often**: Save versions you like before generating new ones
5. **Edit After**: Use the AI output as a foundation, then polish in a proper screenwriting tool

## Need Help?

- Check the README.md for installation issues
- Review system prompts in `views.py` to understand what the AI knows
- Try simplifying your prompt if results are unexpected
- Remember: This is a tool to help with writing, not replace the writer!
