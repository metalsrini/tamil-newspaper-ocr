#!/bin/bash
# ============================================================
# Tamil Newspaper OCR Setup Script
# Optimized for Mac M1/M2/M3
# ============================================================

set -e

echo ""
echo "🔤 Tamil Newspaper OCR - Setup Script"
echo "============================================================"
echo ""

# Check Python version
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" == "3.10" || "$PYTHON_VERSION" == "3.11" || "$PYTHON_VERSION" == "3.12" ]]; then
        PYTHON_CMD="python3"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10+ is required but not found."
    echo "   Please install Python 3.10 or 3.11 using Homebrew:"
    echo "   brew install python@3.11"
    exit 1
fi

echo "📦 Using Python: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📁 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
else
    echo "📁 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install PaddlePaddle
echo "🏓 Installing PaddlePaddle (this may take a moment)..."
pip install paddlepaddle --quiet

# Install PaddleOCR
echo "👁️  Installing PaddleOCR..."
pip install "paddleocr>=2.9.0" --quiet

# Install additional dependencies
echo "📚 Installing additional dependencies..."
pip install opencv-python Pillow --quiet

echo ""
echo "============================================================"
echo "✅ Setup complete!"
echo "============================================================"
echo ""
echo "To use the Tamil OCR scanner:"
echo ""
echo "  1. Activate the environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the scanner:"
echo "     python tamil_ocr.py your_image.jpg"
echo ""
echo "  3. Or use the default sample image:"
echo "     python tamil_ocr.py"
echo ""
echo "============================================================"
echo "Made with ❤️ for the Tamil community"
echo "============================================================"
