#!/usr/bin/env python3
"""
Resize image to 5x3 aspect ratio for landscape sticker printing
"""

from PIL import Image


def resize_to_5x3(input_path, output_path, target_width=1500):
    """
    Resize image to 5:3 aspect ratio (landscape)
    target_width: width in pixels (1500px = 300dpi for 5" width)
    """
    
    # Open the original image
    img = Image.open(input_path)
    
    # Calculate 5:3 dimensions (landscape)
    # For 5x3 sticker: width=5", height=3"
    width = target_width
    height = int(target_width * (3/5))  # 3:5 ratio (landscape)
    
    print(f"Target dimensions: {width}x{height} pixels")
    print("Aspect ratio: 5:3 (landscape)")
    
    # Get current dimensions
    current_w, current_h = img.size
    current_ratio = current_w / current_h
    target_ratio = width / height
    
    print(f"Current: {current_w}x{current_h} (ratio: {current_ratio:.2f})")
    print(f"Target ratio: {target_ratio:.2f}")
    
    if current_ratio > target_ratio:
        # Image is too wide, crop width
        new_width = int(current_h * target_ratio)
        left = (current_w - new_width) // 2
        img_cropped = img.crop((left, 0, left + new_width, current_h))
        print(f"Cropped width: removed {current_w - new_width}px from sides")
    else:
        # Image is too tall, crop height  
        new_height = int(current_w / target_ratio)
        top = (current_h - new_height) // 2
        img_cropped = img.crop((0, top, current_w, top + new_height))
        removed_px = current_h - new_height
        print(f"Cropped height: removed {removed_px}px from top/bottom")
    
    # Resize to final dimensions
    img_final = img_cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    # Save the result
    img_final.save(output_path, 'JPEG', quality=95)
    print(f"✅ 5x3 landscape image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    # Resize the image
    try:
        output_file = resize_to_5x3('the-man.jpg', 'the-man-5x3.jpg', 1500)
        print("\n🎯 Ready for 5x3 landscape sticker printing!")
        print("📐 Dimensions: 1500x900 pixels (300 DPI)")
        print("📁 Use 'the-man-5x3.jpg' as input for your radio guide")
    except Exception as e:
        print(f"❌ Error: {e}") 