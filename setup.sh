#!/bin/bash

echo "🚀 Setting up Genesis Auditor development environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
fi

echo "✅ Setup complete! Run: source venv/bin/activate"
