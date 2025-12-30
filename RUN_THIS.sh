#!/bin/bash

echo "🎉 RunLab - Quick Setup Script"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "START_HERE.md" ]; then
    echo "❌ Please run this from the RunLab root directory"
    exit 1
fi

echo "Step 1: Checking for API keys..."
echo ""

# Check for .env file first
if [ -f "backend/.env" ]; then
    echo "📄 Found backend/.env file, loading it..."
    export $(grep -v '^#' backend/.env | xargs)
fi

if [ -z "$HUGGINGFACE_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  No API key found!"
    echo ""
    echo "Choose an option:"
    echo "  1) Use Hugging Face (FREE!) - Recommended ⭐"
    echo "  2) Use Anthropic Claude (Paid)"
    echo ""
    read -p "Enter your choice (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "🤗 Great! Let's set up Hugging Face (FREE!)"
        echo ""
        echo "Get your FREE token here:"
        echo "👉 https://huggingface.co/settings/tokens"
        echo ""
        echo "Steps:"
        echo "  1. Sign up (free!)"
        echo "  2. Click 'New token'"
        echo "  3. Name: runlab"
        echo "  4. Copy the token"
        echo ""
        read -p "Paste your token (hf_...): " hf_key
        export HUGGINGFACE_API_KEY=$hf_key
        
        cd backend
        if [ ! -f .env ]; then
            cp .env.example .env 2>/dev/null || touch .env
        fi
        
        # Check if key already exists in .env
        if grep -q "HUGGINGFACE_API_KEY=" .env; then
            # Update existing key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/HUGGINGFACE_API_KEY=.*/HUGGINGFACE_API_KEY=$hf_key/" .env
            else
                sed -i "s/HUGGINGFACE_API_KEY=.*/HUGGINGFACE_API_KEY=$hf_key/" .env
            fi
        else
            # Add new key
            echo "HUGGINGFACE_API_KEY=$hf_key" >> .env
        fi
        echo "✅ Saved to backend/.env"
        cd ..
        
    elif [ "$choice" = "2" ]; then
        echo ""
        echo "Using Anthropic Claude"
        read -p "Enter your API key (sk-ant-...): " claude_key
        export ANTHROPIC_API_KEY=$claude_key
        
        cd backend
        if [ ! -f .env ]; then
            cp .env.example .env 2>/dev/null || touch .env
        fi
        
        # Check if key already exists in .env
        if grep -q "ANTHROPIC_API_KEY=" .env; then
            # Update existing key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$claude_key/" .env
            else
                sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$claude_key/" .env
            fi
        else
            # Add new key
            echo "ANTHROPIC_API_KEY=$claude_key" >> .env
        fi
        echo "✅ Saved to backend/.env"
        cd ..
    else
        echo "Invalid choice"
        exit 1
    fi
else
    if [ ! -z "$HUGGINGFACE_API_KEY" ]; then
        echo "✅ Hugging Face API key found!"
    elif [ ! -z "$ANTHROPIC_API_KEY" ]; then
        echo "✅ Anthropic API key found!"
    fi
fi

echo ""
echo "Step 2: Installing dependencies..."
cd backend

if command -v uv &> /dev/null; then
    echo "Using uv (fast!)..."
    uv pip install -r requirements.txt
else
    echo "Using pip..."
    pip install -r requirements.txt
fi

cd ..

echo ""
echo "Step 3: Testing the parser..."
cd backend

if [ ! -z "$HUGGINGFACE_API_KEY" ]; then
    echo "Testing Hugging Face parser..."
    python test_hf_parser.py
else
    echo "Testing Claude parser..."
    python test_parser.py
fi

cd ..

echo ""
echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the server:"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "2. Visit the API docs:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. (Optional) Set up Modal:"
echo "   pip install modal && modal setup"
echo ""
echo "📚 See START_HERE.md for more info!"
echo ""