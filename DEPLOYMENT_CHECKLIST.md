# 🎬 The Spielberg - Production Deployment Checklist

## 📋 Pre-Deployment

- [ ] **Server Requirements**
  - [ ] Ubuntu/Debian server with SSH access
  - [ ] Docker 20.10+ installed
  - [ ] Docker Compose 2.0+ installed
  - [ ] At least 2GB RAM, 20GB disk space
  - [ ] Firewall configured (ports 80, 443, 22)

- [ ] **Domain Configuration**
  - [ ] Domain DNS A record points to server IP
  - [ ] Domain: `spielberg.elimbadi.com`
  - [ ] DNS propagation complete (check with `dig spielberg.elimbadi.com`)

- [ ] **API Keys & Credentials**
  - [ ] Anthropic API key obtained from https://console.anthropic.com/
  - [ ] API key has sufficient credits
  - [ ] Generated new Django SECRET_KEY
  - [ ] Created strong database password
  - [ ] Created strong admin password

## 🔧 Configuration

- [ ] **Environment Variables (.env)**
  - [ ] Copied `.env.example` to `.env`
  - [ ] Set `SECRET_KEY` (generated, not default)
  - [ ] Set `DEBUG=False`
  - [ ] Set `ALLOWED_HOSTS=spielberg.elimbadi.com`
  - [ ] Set `ANTHROPIC_API_KEY`
  - [ ] Set `DATABASE_PASSWORD` (strong password)
  - [ ] Set `DJANGO_SUPERUSER_PASSWORD` (strong password)

- [ ] **Docker Configuration**
  - [ ] Reviewed `docker-compose.yml`
  - [ ] Reviewed `nginx.conf` for domain name
  - [ ] Reviewed `Dockerfile`

## 🚀 Deployment Steps

- [ ] **Initial Setup**
  - [ ] Cloned repository to server
  - [ ] Configured environment variables
  - [ ] Ran `./deploy.sh` or manual deployment

- [ ] **SSL Certificate**
  - [ ] Obtained Let's Encrypt certificate
  - [ ] Certificate for `spielberg.elimbadi.com`
  - [ ] Nginx configured to use certificate
  - [ ] HTTPS redirect working

- [ ] **Services Running**
  - [ ] Web container: `docker-compose ps web` shows "Up"
  - [ ] Database: `docker-compose ps db` shows "Up (healthy)"
  - [ ] Redis: `docker-compose ps redis` shows "Up (healthy)"
  - [ ] Celery worker: `docker-compose ps celery_worker` shows "Up"
  - [ ] Celery beat: `docker-compose ps celery_beat` shows "Up"
  - [ ] Nginx: `docker-compose ps nginx` shows "Up"

## ✅ Post-Deployment Verification

- [ ] **Application Access**
  - [ ] Website loads: https://spielberg.elimbadi.com
  - [ ] SSL certificate valid (no browser warnings)
  - [ ] Admin panel accessible: https://spielberg.elimbadi.com/admin
  - [ ] Can login with admin credentials
  - [ ] Health check endpoint: https://spielberg.elimbadi.com/health/

- [ ] **Functionality Tests**
  - [ ] User authentication working
  - [ ] Can create new script
  - [ ] Can generate script content (creates job)
  - [ ] Job appears in Jobs tab
  - [ ] Celery worker processes job
  - [ ] Job status updates
  - [ ] Can view completed script in viewer
  - [ ] Can create characters
  - [ ] Can create scenes

- [ ] **API Tests**
  - [ ] GET /api/scripts/ returns data
  - [ ] POST /api/scripts/ creates script
  - [ ] POST /api/jobs/create/ creates job
  - [ ] GET /api/jobs/ shows jobs
  - [ ] Rate limiting working (test with multiple rapid requests)

- [ ] **Celery Tests**
  ```bash
  docker-compose exec celery_worker celery -A spielberg_project inspect active
  docker-compose exec celery_worker celery -A spielberg_project inspect registered
  ```
  - [ ] Worker responds to inspect commands
  - [ ] Tasks registered: `generate_script_task`, `generate_scene_task`

- [ ] **Database Tests**
  ```bash
  docker-compose exec db psql -U spielberg -c "SELECT COUNT(*) FROM auth_user;"
  docker-compose exec db psql -U spielberg -c "SELECT COUNT(*) FROM scriptwriter_script;"
  ```
  - [ ] Database accepting connections
  - [ ] Admin user exists
  - [ ] Can create/read data

## 🔐 Security Checklist

- [ ] **Django Security**
  - [ ] `DEBUG=False` in production
  - [ ] `SECRET_KEY` changed from default
  - [ ] `ALLOWED_HOSTS` properly configured
  - [ ] HTTPS enforced (SECURE_SSL_REDIRECT=True)
  - [ ] Secure cookies enabled
  - [ ] HSTS headers configured
  - [ ] XSS protection enabled

- [ ] **Server Security**
  - [ ] Firewall active (ufw/iptables)
  - [ ] Only ports 22, 80, 443 open
  - [ ] SSH key authentication (password disabled)
  - [ ] Root login disabled
  - [ ] Fail2ban installed (optional but recommended)

- [ ] **Application Security**
  - [ ] Default passwords changed
  - [ ] Database password strong (not default)
  - [ ] Admin password strong (not default)
  - [ ] CSRF protection enabled
  - [ ] Rate limiting configured in nginx

## 📊 Monitoring Setup

- [ ] **Logging**
  - [ ] Can view logs: `docker-compose logs -f`
  - [ ] Logs persisting correctly
  - [ ] Log rotation configured (optional)

- [ ] **Backups**
  - [ ] Database backup script created
  - [ ] Cron job for automated backups (optional)
  - [ ] Backup location configured
  - [ ] Tested restore procedure

- [ ] **Monitoring**
  - [ ] Uptime monitoring configured (optional)
  - [ ] SSL certificate expiry monitoring (certbot auto-renews)
  - [ ] Disk space monitoring (optional)
  - [ ] Error alerting (optional)

## 🔄 Maintenance Setup

- [ ] **Documentation**
  - [ ] Team has access to DOCKER_DEPLOYMENT.md
  - [ ] Deployment credentials documented securely
  - [ ] Backup procedures documented
  - [ ] Incident response plan (optional)

- [ ] **Update Procedures**
  - [ ] Git repository access configured
  - [ ] Update procedure tested
  - [ ] Rollback procedure documented

## 🎯 Final Checks

- [ ] **Performance**
  - [ ] Page load times acceptable
  - [ ] API response times < 2 seconds
  - [ ] Script generation completes successfully
  - [ ] No 500 errors in logs

- [ ] **User Experience**
  - [ ] All tabs working (Scripts, Characters, Jobs, Legacy)
  - [ ] Forms submitting correctly
  - [ ] Error messages displaying
  - [ ] Success messages displaying
  - [ ] Script viewer rendering properly

- [ ] **Documentation**
  - [ ] README.md updated
  - [ ] DOCKER_DEPLOYMENT.md available
  - [ ] .env.example up to date
  - [ ] API documentation available (optional)

## 📝 Post-Launch

- [ ] **Communication**
  - [ ] Stakeholders notified of launch
  - [ ] User documentation shared
  - [ ] Support channels established

- [ ] **Initial Users**
  - [ ] Test users created
  - [ ] Initial feedback collected
  - [ ] Issues tracked and prioritized

- [ ] **Optimization**
  - [ ] Monitor resource usage first week
  - [ ] Adjust worker concurrency if needed
  - [ ] Optimize database queries if needed
  - [ ] Configure CDN if needed (optional)

---

## 🆘 Emergency Contacts

- **Server Provider**: ___________________
- **Domain Registrar**: ___________________
- **On-Call Engineer**: ___________________
- **Anthropic Support**: https://support.anthropic.com

## 🔗 Important URLs

- **Production**: https://spielberg.elimbadi.com
- **Admin**: https://spielberg.elimbadi.com/admin
- **API**: https://spielberg.elimbadi.com/api/
- **Health Check**: https://spielberg.elimbadi.com/health/
- **Repository**: https://github.com/elishambadi/the-spielberg

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Sign-off**: _______________
