#!/bin/bash

# Quick Start Script for The Spielberg
# This script sets up and runs the development environment

echo "🎬 The Spielberg - Quick Start"
echo "================================"
echo ""

# Check if Redis is running
echo "📡 Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "❌ Redis is not running. Please start Redis:"
    echo "   - Ubuntu/Debian: sudo systemctl start redis"
    echo "   - macOS: brew services start redis"
    echo "   - Manual: redis-server"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << EOF
ANTHROPIC_API_KEY=your-api-key-here
DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DJANGO_DEBUG=True
REDIS_URL=redis://localhost:6379/0
EOF
    echo "✅ Created .env file. Please add your ANTHROPIC_API_KEY"
    echo "   Get your API key from: https://console.anthropic.com/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".movie-venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .movie-venv
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source .movie-venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate

# Check if superuser exists
echo ""
echo "👤 Checking for superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  No superuser found. Creating one..."
    python manage.py createsuperuser
fi

# Display startup instructions
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Start Celery worker (in a new terminal):"
echo "   celery -A spielberg_project worker --loglevel=info"
echo ""
echo "2. Start Django server (in another terminal):"
echo "   python manage.py runserver"
echo ""
echo "3. Access the application:"
echo "   - Main app: http://localhost:8000/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - API docs: http://localhost:8000/api/"
echo ""
echo "4. Review documentation:"
echo "   - DEPLOYMENT.md - Full deployment guide"
echo "   - IMPLEMENTATION_SUMMARY.md - What was implemented"
echo ""
echo "🎬 Happy writing!"
