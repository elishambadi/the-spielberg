# 🎬 The Spielberg - Quick Reference

## 🚀 One-Line Deploy
```bash
./deploy.sh
```

## 📦 Essential Commands

### Service Management
```bash
docker-compose up -d              # Start all services
docker-compose down               # Stop all services
docker-compose restart web        # Restart specific service
docker-compose ps                 # Check status
docker-compose logs -f web        # View logs
```

### Application Updates
```bash
git pull
docker-compose up -d --build web celery_worker celery_beat
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### Database
```bash
# Backup
docker-compose exec db pg_dump -U spielberg spielberg > backup.sql

# Restore
docker-compose exec -T db psql -U spielberg spielberg < backup.sql

# Shell
docker-compose exec web python manage.py shell

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### SSL Certificate
```bash
# Initial setup
docker-compose run --rm certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  -d spielberg.elimbadi.com \
  --email your@email.com \
  --agree-tos --no-eff-email

# Manual renewal
docker-compose run --rm certbot renew
docker-compose restart nginx
```

### Monitoring
```bash
# Service health
docker-compose ps

# Resource usage
docker stats

# Celery status
docker-compose exec celery_worker celery -A spielberg_project inspect active

# Redis status
docker-compose exec redis redis-cli INFO stats

# Database connections
docker-compose exec db psql -U spielberg -c "SELECT count(*) FROM pg_stat_activity;"
```

## 🌐 URLs

| URL | Purpose |
|-----|---------|
| https://spielberg.elimbadi.com | Main app |
| https://spielberg.elimbadi.com/admin | Admin panel |
| https://spielberg.elimbadi.com/viewer/ | Script viewer |
| https://spielberg.elimbadi.com/health/ | Health check |
| https://spielberg.elimbadi.com/api/ | REST API |

## 🔑 Default Credentials

**Admin Panel**
- URL: https://spielberg.elimbadi.com/admin
- Username: `admin`
- Password: Check `DJANGO_SUPERUSER_PASSWORD` in `.env`

## 🐛 Quick Troubleshooting

### 502 Bad Gateway
```bash
docker-compose restart web
docker-compose logs web
```

### Jobs Not Processing
```bash
docker-compose restart celery_worker
docker-compose logs celery_worker
docker-compose exec celery_worker celery -A spielberg_project inspect active
```

### Database Connection Error
```bash
docker-compose restart db
docker-compose exec db pg_isready -U spielberg
```

### Static Files Not Loading
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

## 📊 Service Ports

| Service | Internal Port | External Port |
|---------|--------------|---------------|
| Nginx | - | 80, 443 |
| Web | 8000 | - |
| PostgreSQL | 5432 | - |
| Redis | 6379 | - |

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `docker-compose.yml` | Container orchestration |
| `nginx.conf` | Nginx configuration |
| `Dockerfile` | Container build |
| `settings.py` | Django settings |

## 🔄 Update Workflow

1. **Pull changes**: `git pull`
2. **Rebuild**: `docker-compose up -d --build`
3. **Migrate**: `docker-compose exec web python manage.py migrate`
4. **Static**: `docker-compose exec web python manage.py collectstatic --noinput`
5. **Test**: Visit site and test functionality

## 📝 Environment Variables

Required in `.env`:
```bash
SECRET_KEY=                    # Django secret
DEBUG=False                    # Production mode
ALLOWED_HOSTS=spielberg.elimbadi.com
ANTHROPIC_API_KEY=            # AI key
DATABASE_PASSWORD=            # DB password
DJANGO_SUPERUSER_PASSWORD=   # Admin password
```

## 🚨 Emergency Procedures

### Complete Restart
```bash
docker-compose down
docker-compose up -d
```

### Reset Everything (⚠️ DESTROYS DATA)
```bash
docker-compose down -v
docker-compose up -d --build
```

### View All Errors
```bash
docker-compose logs --tail=100 | grep -i error
```

## 📚 Documentation

- **Full Guide**: DOCKER_DEPLOYMENT.md
- **Checklist**: DEPLOYMENT_CHECKLIST.md
- **Package Info**: DEPLOYMENT_PACKAGE.md
- **Implementation**: IMPLEMENTATION_SUMMARY.md

---

**Need Help?** Check DOCKER_DEPLOYMENT.md for detailed troubleshooting
