#!/usr/bin/env python3
"""
Radio Burning Man 2025 - Frequency Guide Generator
Creates a visual guide overlaying radio frequencies on the Burning Man image
"""

import csv
from PIL import Image, ImageDraw, ImageFont


def load_frequencies(csv_file):
    """Load frequency data from CSV file"""
    frequencies = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            frequencies.append({
                'freq': row['Frequency'],
                'station': row['Station ID']
            })
    return frequencies


def get_font(size, bold=False):
    """Get font with fallback options"""
    font_options = [
        '/System/Library/Fonts/Helvetica.ttc',  # macOS
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        'arial.ttf',  # Windows
    ]
    
    for font_path in font_options:
        try:
            return ImageFont.truetype(font_path, size)
        except (IOError, OSError):
            continue
    
    # Fallback to default font
    return ImageFont.load_default()


def create_radio_guide(image_path, csv_path,
                       output_path='radio_guide_2025.jpg'):
    """Create the radio frequency guide overlay"""
    
    # Load the background image
    img = Image.open(image_path)
    img = img.convert('RGBA')
    
    # Create a semi-transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Load frequency data
    frequencies = load_frequencies(csv_path)
    
    # Image dimensions
    width, height = img.size
    
    # Create semi-transparent background for text readability
    bg_padding = 20
    bg_top = 20
    bg_height = height - 40
    bg_rect = [bg_padding, bg_top, width - bg_padding, bg_top + bg_height]
    draw.rectangle(bg_rect, fill=(0, 0, 0, 0))
    
    # Set up fonts - adjusted for better spacing
    title_font = get_font(int(width * 0.06), bold=True)  # Slightly smaller
    freq_font = get_font(int(width * 0.024))  # Increased by 2pt equivalent
    station_font = get_font(int(width * 0.022))  # Increased by 2pt equivalent
    font_color = (255, 255, 0, 255)
    
    # Add top margin
    top_margin = int(height * 0.09)  # 12% of image height for top margin
    
    # Title - centered with top margin
    title = "Black Rock Radio 2025"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (width - title_width) // 2
    title_y = bg_top + top_margin
    draw.text((title_x, title_y), title, fill=font_color,
              font=title_font)
    
    # Add margin between title and table
    title_table_margin = int(height * 0.08)  # 8% of image height
    
    # Calculate table dimensions and center it vertically
    table_start_y = title_y + title_height + title_table_margin
    bottom_margin = int(height * 0.05)  # Leave some space at bottom
    available_height = bg_height - (table_start_y - bg_top) - bottom_margin
    
    # Calculate proper row spacing with much more generous margins
    num_rows_per_column = (len(frequencies) + 1) // 2
    row_margin = int(height * 0.035)  # Much larger margin between rows
    text_height = int(height * 0.03)  # Height for text
    total_row_height = text_height + row_margin
    table_height = num_rows_per_column * total_row_height
    
    # Center the table vertically in remaining space
    if table_height < available_height:
        vertical_center_offset = (available_height - table_height) // 2
        content_start_y = table_start_y + vertical_center_offset
    else:
        content_start_y = table_start_y
        # Adjust spacing if table is too tall
        total_row_height = available_height // num_rows_per_column
        row_margin = max(int(total_row_height * 0.4), 8)  # At least 40% margin
    
    # Column positioning - use full width with better spacing
    col1_x = bg_padding + 60
    col2_x = width // 2 + 40
    col_width = (width // 2) - 80
    
    # Split frequencies into two columns
    mid_point = (len(frequencies) + 1) // 2
    col1_freqs = frequencies[:mid_point]
    col2_freqs = frequencies[mid_point:]
    
    # Draw first column
    for i, freq_data in enumerate(col1_freqs):
        y_pos = content_start_y + (i * total_row_height)
        if y_pos + total_row_height > bg_top + bg_height - bottom_margin:
            break
            
        # Frequency - now yellow
        draw.text((col1_x, y_pos), freq_data['freq'], 
                  fill=font_color, font=freq_font)
        
        # Station - now yellow (truncate if too long for available width)
        station_text = freq_data['station']
        # Adjusted for new font size
        max_chars = int(col_width / (width * 0.014))
        if len(station_text) > max_chars:
            station_text = station_text[:max_chars-3] + "..."
        draw.text((col1_x + int(width * 0.08), y_pos), station_text, 
                  fill=(255, 255, 0, 255), font=station_font)
    
    # Draw second column
    for i, freq_data in enumerate(col2_freqs):
        y_pos = content_start_y + (i * total_row_height)
        if y_pos + total_row_height > bg_top + bg_height - bottom_margin:
            break
            
        # Frequency - now yellow
        draw.text((col2_x, y_pos), freq_data['freq'], 
                  fill=(255, 255, 0, 255), font=freq_font)
        
        # Station - now yellow (truncate if too long for available width)
        station_text = freq_data['station']
        # Adjusted for new font size
        max_chars = int(col_width / (width * 0.014))
        if len(station_text) > max_chars:
            station_text = station_text[:max_chars-3] + "..."
        draw.text((col2_x + int(width * 0.08), y_pos), station_text, 
                  fill=(255, 255, 0, 255), font=station_font)
    
    # Combine the overlay with the original image
    final_img = Image.alpha_composite(img, overlay)
    final_img = final_img.convert('RGB')
    
    # Save the result
    final_img.save(output_path, 'JPEG', quality=95)
    print(f"Radio guide created successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    # Create the radio guide
    try:
        output_file = create_radio_guide('the-man-5x3.jpg', 'freqs.csv')
        print("\n✅ Success! Your Radio Burning Man 2025 guide created.")
        print(f"📁 Output file: {output_file}")
        print("🎯 Centered layout with proper margins")
        print("📻 Perfect for keeping track of all the stations!")
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file - {e}")
        print("Make sure files are in the current directory")
    except Exception as e:
        print(f"❌ Error creating radio guide: {e}") 