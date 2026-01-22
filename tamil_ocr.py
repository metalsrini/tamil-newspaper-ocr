#!/usr/bin/env python3
"""
Tamil Newspaper OCR Scanner using PaddleOCR 3.x
Optimized for Mac M1

Usage:
    python tamil_ocr.py <image_path>
    python tamil_ocr.py                   # Uses default image
"""

import sys
import os
from pathlib import Path


def scan_tamil_newspaper(image_path: str, output_dir: str = "output"):
    """
    Scan a Tamil newspaper image and extract text using PaddleOCR 3.x.
    
    Args:
        image_path: Path to the newspaper image (jpg, png, etc.)
        output_dir: Directory to save output files
    
    Returns:
        List of extracted text strings
    """
    # Disable model source check for faster startup
    os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
    
    from paddleocr import PaddleOCR
    
    # Verify image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return []
    
    print(f"📰 Processing Tamil newspaper: {image_path}")
    print("-" * 50)
    
    # Initialize PaddleOCR with Tamil language support (PaddleOCR 3.x API)
    ocr = PaddleOCR(
        lang='ta',                              # Tamil language
        use_textline_orientation=True,          # Detect text orientation
        device='cpu',                           # Mac M1 - use CPU
        text_det_thresh=0.3,                    # Detection threshold
        text_det_box_thresh=0.5,                # Box threshold
    )
    
    # Perform OCR using PaddleOCR 3.x predict API
    print("🔍 Detecting text regions...")
    result = ocr.predict(image_path)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    if not result:
        print("⚠️  No text detected in the image.")
        return []
    
    # Process and extract text from results
    extracted_texts = []
    all_scores = []
    
    for res in result:
        # Save the visualization and JSON output
        res.save_to_img(output_dir)
        res.save_to_json(output_dir)
        
        # Read the JSON output to get the texts
        import json
        image_name = Path(image_path).stem
        json_path = os.path.join(output_dir, f"{image_name}_res.json")
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'rec_texts' in data:
                    extracted_texts = data['rec_texts']
                    all_scores = data.get('rec_scores', [0.0] * len(extracted_texts))
    
    # Display extracted text
    print("\n📝 Extracted Tamil Text:")
    print("=" * 60)
    
    for idx, text in enumerate(extracted_texts, 1):
        score = all_scores[idx-1] if idx-1 < len(all_scores) else 0.0
        print(f"{idx:3}. [{score:.1%}] {text}")
    
    print("=" * 60)
    print(f"✅ Total lines extracted: {len(extracted_texts)}")
    
    # Save plain text file
    output_txt = os.path.join(output_dir, "extracted_text.txt")
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"Tamil OCR Results - {os.path.basename(image_path)}\n")
        f.write("=" * 60 + "\n\n")
        for text in extracted_texts:
            f.write(text + "\n")
    print(f"\n💾 Plain text saved to: {output_txt}")
    
    # Print summary statistics
    if all_scores:
        avg_score = sum(all_scores) / len(all_scores)
        print(f"📊 Average confidence: {avg_score:.1%}")
    
    return extracted_texts


def main():
    # Default to the sample newspaper image
    default_image = "1702553327433.jpeg"
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = default_image
        print(f"ℹ️  Using default image: {image_path}")
    
    # Get the script directory
    script_dir = Path(__file__).parent
    
    # If relative path, make it relative to script directory
    if not os.path.isabs(image_path):
        image_path = str(script_dir / image_path)
    
    # Run OCR
    output_dir = str(script_dir / "output")
    texts = scan_tamil_newspaper(image_path, output_dir)
    
    if texts:
        print("\n✨ OCR processing complete!")
    else:
        print("\n⚠️  No text was extracted. Try adjusting thresholds.")


if __name__ == "__main__":
    main()
