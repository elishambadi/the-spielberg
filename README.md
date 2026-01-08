# The Spielberg 🎬

An AI-powered script writing web application that helps screenwriters create professional scripts using Claude AI. Built with Django, Django REST Framework, Celery, and Alpine.js.

## ✨ Features

### Core Functionality
- 🤖 **AI-Powered Script Generation**: Uses Claude Opus 4 (Anthropic) with async job processing
- 📝 **Multiple Script Formats**: Screenplay, Treatment, Outline
- 💾 **Script Management**: CRUD operations with versioning support
- 🎭 **Character Management**: Create and manage character profiles
- 🎬 **Scene-by-Scene Generation**: Generate individual scenes with context
- 📊 **Job Monitoring**: Track AI generation progress in real-time
- 🔐 **Authentication**: User-based access control with session auth
- 🎨 **Modern UI**: Alpine.js-powered reactive interface with tabs
- 📖 **Script Viewer**: Beautiful formatted script reader with markdown parsing

### Technical Features
- ⚡ **Async Task Processing**: Celery workers for background AI generation
- 🔄 **RESTful API**: Django REST Framework with pagination
- 📦 **Version Control**: Track script versions and changes
- 🎯 **Tone & Genre Locking**: Control script style and mood
- 🚀 **Production Ready**: Docker deployment with PostgreSQL, Redis, Nginx

## 🚀 Quick Start

### Docker Deployment (Recommended for Production)

```bash
# Clone repository
git clone https://github.com/elishambadi/the-spielberg.git
cd the-spielberg

# Run automated deployment
./deploy.sh
```

For detailed deployment instructions, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

### Local Development

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
