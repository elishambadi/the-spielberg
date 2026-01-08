#!/bin/bash
set -e

echo "🎬 The Spielberg - Docker Deployment Script"
echo "==========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env file with your credentials:${NC}"
    echo "   - POSTGRES_PASSWORD"
    echo "   - SECRET_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    echo -e "${YELLOW}Press Enter after editing .env to continue...${NC}"
    read -r
fi

# Generate SECRET_KEY if not set
if grep -q "your_django_secret_key_here" .env; then
    echo -e "${YELLOW}⚠️  Generating new SECRET_KEY...${NC}"
    SECRET_KEY=$(python3 -c 'from secrets import token_urlsafe; print(token_urlsafe(50))' 2>/dev/null || openssl rand -base64 50 | tr -d '\n')
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env
    echo -e "${GREEN}✅ New SECRET_KEY generated${NC}"
fi

# Check if ANTHROPIC_API_KEY is set
if grep -q "your_anthropic_api_key_here" .env; then
    echo -e "${RED}❌ Please set your ANTHROPIC_API_KEY in .env${NC}"
    exit 1
fi

# Check if POSTGRES_PASSWORD is set
if grep -q "your_secure_postgres_password" .env; then
    echo -e "${RED}❌ Please set your POSTGRES_PASSWORD in .env${NC}"
    exit 1
fi

echo ""
echo "🔧 Configuration OK"
echo ""

echo "🏗️  Building Docker images..."
docker compose build

echo ""
echo "🚀 Starting services..."
docker compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo ""
echo "📊 Service Status:"
docker compose ps

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo -e "${GREEN}✅ Application is running at: http://localhost:8000"
echo ""
echo "📝 Next steps:"
echo "   1. Create admin user: docker compose exec app python manage.py createsuperuser"
echo "   2. Access admin: http://localhost:8000/admin"
echo ""
echo "📊 Useful commands:"
echo "   - View logs: docker compose logs -f app"
echo "   - View celery logs: docker compose logs -f celery"
echo "   - Stop services: docker compose down"
echo "   - Restart: docker compose restart"
echo ""
echo "📖 Full documentation: DOCKER_DEPLOYMENT.md"
echo ""
