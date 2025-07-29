#!/bin/bash
# SyntaxMem Auth Test Runner
# Simple, Uniform, Consistent testing script

echo "🧪 SyntaxMem Auth Testing Suite"
echo "================================"
echo ""

# Check if auth server is running
echo "📡 Checking if auth server is running..."
if ! curl -s http://localhost:8081/health > /dev/null; then
    echo "❌ Auth server not running on port 8081"
    echo "💡 Start it with: cd auth && python main.py"
    exit 1
fi

echo "✅ Auth server is running"
echo ""

# Install test dependencies if needed
echo "📦 Installing test dependencies..."

# Check if we're in a virtual environment or if aiohttp is available
if command -v pip > /dev/null && python -c "import aiohttp" 2>/dev/null; then
    echo "✅ Dependencies already available"
elif [ -d "../venv" ]; then
    echo "🐍 Using virtual environment..."
    source ../venv/bin/activate
    pip install -q aiohttp
else
    echo "🐍 Creating virtual environment..."
    cd ..
    python -m venv venv
    source venv/bin/activate
    pip install -q aiohttp python-dotenv motor pymongo PyJWT Flask Flask-CORS cryptography
    cd tests
fi

# Run the tests
echo "🚀 Running Phase 2 automated tests..."
echo ""

# Make sure we're using the virtual environment for test execution too
if [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

cd "$(dirname "$0")"
python test_auth.py

echo ""
echo "✨ Test run complete!"