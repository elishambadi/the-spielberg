# Docker Deployment Guide

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   POSTGRES_PASSWORD=your_secure_password
   SECRET_KEY=your_django_secret_key
   ANTHROPIC_API_KEY=your_api_key
   ```

3. **Build and start containers:**
   ```bash
   docker-compose up -d
   ```

4. **Create superuser:**
   ```bash
   docker-compose exec app python manage.py createsuperuser
   ```

5. **Access the application:**
   - App: http://spielberg.elimbadi.com:8000
   - Admin: http://spielberg.elimbadi.com:8000/admin

## Container Architecture

- **app**: Django application (port 8000)
- **celery**: Async task worker for AI generation
- **postgres**: PostgreSQL database
- **redis**: Cache and message broker

## Useful Commands

```bash
# View logs
docker-compose logs -f app
docker-compose logs -f celery

# Restart services
docker-compose restart app
docker-compose restart celery

# Run migrations
docker-compose exec app python manage.py migrate

# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Production Notes

- Configure nginx/reverse proxy at server level for SSL and port 80/443
- Set secure passwords in `.env`
- Ensure `DEBUG=False` in production
- Regular backups of `postgres_data` volume
