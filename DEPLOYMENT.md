# The Spielberg - Deployment & Usage Guide

## Overview

All improvements from `improvements.txt` have been successfully implemented:

1. ✅ Async AI Generation with Celery + Redis
2. ✅ Job-Based API Flow (submit → poll → retrieve)
3. ✅ Job Tracking (pending, running, completed, failed)
4. ✅ Authentication & Ownership (User-based access control)
5. ✅ Script Storage & Versioning (v1, v2, v3, etc.)
6. ✅ Character System (create & attach to scripts)
7. ✅ Scene-Based Generation (individual scene management)
8. ✅ Tone & Genre Locking (per script configuration)
9. ✅ Frontend with Alpine.js (job polling, character management, scene regeneration)

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your-api-key-here
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
REDIS_URL=redis://localhost:6379/0
```

### 3. Apply Database Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser

```bash
python manage.py createsuperuser
```

### 5. Start Redis Server

```bash
# On Ubuntu/Debian
sudo systemctl start redis

# On macOS with Homebrew
brew services start redis

# Or run directly
redis-server
```

### 6. Start Celery Worker

In a separate terminal:

```bash
celery -A spielberg_project worker --loglevel=info
```

### 7. (Optional) Start Celery Beat for Scheduled Tasks

In another terminal:

```bash
celery -A spielberg_project beat --loglevel=info
```

### 8. Run Django Development Server

```bash
python manage.py runserver
```

---

## API Endpoints

### Authentication Required Endpoints

All API endpoints except legacy ones require authentication. Login via Django admin at `/admin/`.

### Job Management

- **Create Job**: `POST /api/jobs/create/`
  ```json
  {
    "prompt": "Write a scene where...",
    "job_type": "script_generation",  // or "scene_generation"
    "script_id": 1,  // optional
    "scene_id": 1,   // optional, for scene regeneration
    "script_type": "screenplay"  // or "treatment", "outline"
  }
  ```
  Returns: `{ "job_id": "uuid", "status": "pending" }` (HTTP 202)

- **Check Job Status**: `GET /api/jobs/<job_id>/status/`
  Returns: `{ "job_id": "...", "status": "running", ... }`

- **Get Job Result**: `GET /api/jobs/<job_id>/result/`
  Returns: `{ "job_id": "...", "status": "completed", "result": "..." }`

- **List All Jobs**: `GET /api/jobs/`

### Character Management

- **List Characters**: `GET /api/characters/`
- **Create Character**: `POST /api/characters/`
  ```json
  {
    "name": "John Doe",
    "personality": "Cynical detective with a heart of gold",
    "goals": "Solve the case and reconnect with his daughter",
    "voice": "Speaks in short, clipped sentences. Uses noir-style metaphors",
    "backstory": "Former FBI agent turned private investigator"
  }
  ```
- **Update Character**: `PUT /api/characters/<id>/`
- **Delete Character**: `DELETE /api/characters/<id>/`

### Script Management

- **List Scripts**: `GET /api/scripts/`
- **Create Script**: `POST /api/scripts/`
  ```json
  {
    "title": "Dark City Nights",
    "genre": "thriller",
    "tone": "dark",
    "logline": "A detective investigates memory theft in a neo-noir future",
    "character_ids": [1, 2, 3]
  }
  ```
- **Get Script**: `GET /api/scripts/<id>/`
- **Create Version**: `POST /api/scripts/<id>/create_version/`
- **List Versions**: `GET /api/scripts/<id>/versions/`

### Scene Management

- **List Scenes**: `GET /api/scenes/`
- **Create Scene**: `POST /api/scenes/`
  ```json
  {
    "script_version": 1,
    "scene_number": 1,
    "setting": "INT. DETECTIVE'S OFFICE - NIGHT",
    "goal": "Introduce the protagonist and establish the tone",
    "tension": "Client arrives with an impossible case",
    "tone": "suspenseful",
    "content": "Scene content will be generated or can be manually entered"
  }
  ```
- **Regenerate Scene**: `POST /api/scenes/<id>/regenerate/`

### Legacy Endpoints (No Auth Required, Requires API Key in Request)

- **Generate Script (Direct)**: `POST /api/generate/`
- **Save Script**: `POST /api/save/`

---

## Frontend Usage

### Two Interfaces Available

1. **Legacy Generator** (`/`)
   - Original simple interface
   - Requires Claude API key in UI
   - Direct generation (no job system)
   - Good for quick tests

2. **Professional Interface** (`/`)
   - Tabs for Scripts, Characters, Jobs, and Legacy Generator
   - Full job-based workflow with polling
   - Character management
   - Script versioning
   - Requires user login

### Workflow Example

1. **Create Characters**
   - Go to Characters tab
   - Click "New Character"
   - Fill in personality, goals, voice, backstory
   - Save

2. **Create Script**
   - Go to Scripts tab
   - Click "New Script"
   - Set title, genre, tone, logline
   - Optionally attach characters
   - Save

3. **Generate Script Version**
   - Click "Generate" on a script card
   - Enter prompt (e.g., "Write Act 1 following the three-act structure")
   - System creates a job
   - Job is automatically polled every 2 seconds
   - Result appears when completed

4. **Manage Scenes**
   - Create individual scenes with setting, goal, tension
   - Regenerate specific scenes
   - Scene content uses character data from script

5. **Monitor Jobs**
   - Go to Jobs tab
   - See all pending/running/completed jobs
   - View results directly from job cards

---

## Architecture

### Models

- **User**: Django built-in user model
- **Character**: Reusable character profiles
- **Script**: Main script container with genre/tone
- **ScriptVersion**: Versioned script content (v1, v2, v3...)
- **Scene**: Individual scenes within a version
- **Job**: Async job tracking for all AI operations
- **ScriptProject**: Legacy model for backwards compatibility

### Celery Tasks

- `generate_script_task(job_id, prompt, script_id, script_type)`
  - Generates full scripts or script versions
  - Injects character data into prompts
  - Creates new ScriptVersion on completion

- `generate_scene_task(job_id, scene_id, prompt)`
  - Generates/regenerates individual scenes
  - Uses scene metadata (setting, goal, tension)
  - Updates scene content directly

### System Prompts

System prompts automatically include:
- Selected genre and tone
- Character personality, goals, voice, backstory
- Scene-specific requirements (for scene generation)
- Format-specific rules (screenplay vs treatment vs outline)

---

## Configuration

### Celery Settings

In `settings.py`:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
```

### REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

---

## Troubleshooting

### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
redis-server
```

### Celery Worker Not Processing Jobs

```bash
# Check Celery worker logs
# Make sure worker is running with correct app name
celery -A spielberg_project worker --loglevel=debug
```

### Jobs Stuck in "Pending"

- Ensure Celery worker is running
- Check Redis connection
- Verify ANTHROPIC_API_KEY is set in environment

### Authentication Issues

- Create a user via Django admin
- Login at `/admin/`
- Session auth is automatically used for API calls

---

## Production Considerations

1. **Security**
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Use environment variables for secrets
   - Configure ALLOWED_HOSTS

2. **Redis**
   - Use Redis with persistence enabled
   - Consider Redis Cluster for high availability

3. **Celery**
   - Use supervisord or systemd to manage worker processes
   - Run multiple workers for better throughput
   - Monitor with Flower: `pip install flower && celery -A spielberg_project flower`

4. **Database**
   - Switch from SQLite to PostgreSQL for production
   - Configure database connection pooling

5. **Web Server**
   - Use Gunicorn + Nginx
   - Configure static files serving
   - Set up SSL/TLS

---

## Testing the System

### Quick Test

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A spielberg_project worker --loglevel=info

# Terminal 3: Start Django
python manage.py runserver

# Terminal 4: Test API
curl -X POST http://localhost:8000/api/jobs/create/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "job_type": "script_generation", "script_type": "outline"}'
```

---

## Future Enhancements

Possible additions:
- WebSocket support for real-time job updates
- Export scripts to PDF (proper screenplay format)
- Collaborative editing (multiple users per script)
- Template library (common plot structures)
- AI-powered script analysis and feedback
- Integration with fountain format
- Version diff viewer
- Scene breakdown tools

---

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Celery Documentation: https://docs.celeryproject.org/
- DRF Documentation: https://www.django-rest-framework.org/
- Anthropic Claude API: https://docs.anthropic.com/

---

## License

See LICENSE file for details.
