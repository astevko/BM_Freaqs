#!/usr/bin/env python3
"""
Resize image to 3x5 aspect ratio for sticker printing
"""

from PIL import Image


def resize_to_3x5(input_path, output_path, target_width=1500):
    """
    Resize image to 3:5 aspect ratio
    target_width: width in pixels (1500px = 300dpi for 5" width)
    """
    
    # Open the original image
    img = Image.open(input_path)
    
    # Calculate 3:5 dimensions
    # For 3x5 sticker: width=3", height=5"
    width = target_width
    height = int(target_width * (5/3))  # 5:3 ratio (portrait)
    
    print(f"Target dimensions: {width}x{height} pixels")
    print("Aspect ratio: 3:5 (portrait)")
    
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
    print(f"✅ 3x5 image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    # Resize the image
    try:
        output_file = resize_to_3x5('the-man.jpg', 'the-man-3x5.jpg', 1500)
        print("\n🎯 Ready for 3x5 sticker printing!")
        print("📐 Dimensions: 1500x2500 pixels (300 DPI)")
        print("📁 Use 'the-man-3x5.jpg' as input for your radio guide")
    except Exception as e:
        print(f"❌ Error: {e}") 