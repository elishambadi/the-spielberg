# The Spielberg 🎬

An AI-powered script writing web application that helps screenwriters create professional scripts using Claude AI. Built with Django and Alpine.js, it applies fundamental principles of screenplay writing and formatting.

## Features

- 🤖 **AI-Powered Script Generation**: Uses Claude AI (Anthropic) to generate professional scripts
- 📝 **Multiple Script Formats**:
  - **Screenplay**: Full professional screenplay format with scene headings, action lines, and dialogue
  - **Treatment**: Narrative prose description of your story
  - **Outline**: Structured breakdown with acts, sequences, and story beats
- 💾 **Save & Manage Scripts**: Store your generated scripts in a database
- 🎨 **Beautiful UI**: Modern, cinematic interface with Alpine.js reactivity
- 📋 **Copy to Clipboard**: Easy script sharing and export
- 🎭 **Script Writing Principles**: Built-in system prompts that follow industry-standard screenplay formatting and storytelling principles

## Script Writing Principles Included

The application incorporates professional screenwriting principles:

### Screenplay Format
- Proper scene headings (INT./EXT. LOCATION - TIME)
- Action lines in present tense
- Character introductions and dialogue formatting
- Parentheticals for actor direction
- Standard transitions (FADE IN, CUT TO, etc.)

### Storytelling Structure
- Three-act structure (Setup, Confrontation, Resolution)
- Character arcs and development
- Visual storytelling over exposition
- Subtext in dialogue
- Rising tension and conflict
- Strong opening hooks
- Satisfying resolutions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Claude API key from [Anthropic Console](https://console.anthropic.com/)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/elishambadi/the-spielberg.git
cd the-spielberg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## Usage

1. **Get Your API Key**: 
   - Visit [console.anthropic.com](https://console.anthropic.com/)
   - Sign up/login and create an API key

2. **Enter Your API Key**: 
   - Paste your Claude API key in the "Claude API Key" field
   - The key is used client-side and not stored on the server

3. **Choose Script Type**:
   - **Screenplay**: For traditional script format with scenes and dialogue
   - **Treatment**: For narrative story descriptions
   - **Outline**: For structured story beats and act breakdowns

4. **Write Your Prompt**:
   - Describe the story you want to create
   - Be specific about genre, tone, characters, and setting
   - Example: "Write the opening scene of a noir detective story set in 1940s Los Angeles"

5. **Generate Script**:
   - Click "Generate Script" and wait for Claude to create your content
   - The script will appear in the output panel with proper formatting

6. **Save or Copy**:
   - Use "Copy" to copy the script to your clipboard
   - Use "Save" to store it in the database for future reference

## System Prompts

The application uses carefully crafted system prompts that instruct Claude AI to:

- Follow professional screenplay formatting standards
- Apply three-act structure and story beats
- Create compelling character development
- Use visual storytelling techniques
- Write authentic dialogue with subtext
- Maintain proper screenplay style (Courier font conventions)

## Project Structure

```
the-spielberg/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── spielberg_project/            # Django project settings
│   ├── settings.py               # Application configuration
│   ├── urls.py                   # URL routing
│   └── ...
└── scriptwriter/                 # Main Django app
    ├── models.py                 # Database models
    ├── views.py                  # View logic and API endpoints
    ├── urls.py                   # App-specific URLs
    ├── admin.py                  # Admin interface configuration
    └── templates/
        └── scriptwriter/
            └── index.html        # Main UI with Alpine.js
```

## API Endpoints

- `GET /` - Main script writing interface
- `POST /api/generate/` - Generate script using Claude AI
  - Body: `{ "api_key": "...", "prompt": "...", "script_type": "screenplay" }`
- `POST /api/save/` - Save generated script
  - Body: `{ "title": "...", "content": "...", "genre": "...", "logline": "..." }`

## Technologies Used

- **Backend**: Django 6.0.1
- **Frontend**: Alpine.js 3.x
- **AI**: Claude 3.5 Sonnet (Anthropic)
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Styling**: Custom CSS with cinematic theme

## Security Notes

- API keys are handled client-side and not stored in the database
- CSRF protection is disabled for API endpoints (use tokens in production)
- For production deployment, ensure you:
  - Set `DEBUG = False`
  - Configure `ALLOWED_HOSTS`
  - Use environment variables for sensitive settings
  - Implement proper API key management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Credits

Built with ❤️ for screenwriters and storytellers everywhere.
