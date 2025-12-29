#!/bin/bash

echo "🚀 RunLab Setup Script"
echo "======================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo ""
    echo "Please get your API key from: https://console.anthropic.com/"
    echo ""
    read -p "Enter your Anthropic API key: " api_key
    export ANTHROPIC_API_KEY=$api_key

    # Ask if user wants to save it
    read -p "Save this to backend/.env file? (y/n): " save_env
    if [ "$save_env" = "y" ]; then
        cd backend
        if [ ! -f .env ]; then
            cp .env.example .env
        fi
        echo "ANTHROPIC_API_KEY=$api_key" >> .env
        echo "✅ Saved to backend/.env"
        cd ..
    fi
else
    echo "✅ ANTHROPIC_API_KEY found in environment"
fi

echo ""
echo "Installing dependencies..."
cd backend

# Check if uv is available (faster)
if command -v uv &> /dev/null; then
    echo "Using uv (fast installer)..."
    uv pip install -r requirements.txt
else
    echo "Using pip..."
    pip3 install -r requirements.txt
fi

cd ..

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Test the parser:"
echo "   cd backend && python test_parser.py"
echo ""
echo "2. Start the API server:"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "3. Visit http://localhost:8000/docs"
echo ""
echo "📖 See QUICKSTART.md for detailed instructions"
echo ""
echo "🎉 Happy hacking!"
