import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
import io
import PyPDF2

# Path to the folders containing front and back participant images
FOLDER = "lanyards/"

# Get a list of all image files in the front and back folders
front_image_files = sorted([f for f in os.listdir(FOLDER) if f.endswith('_1front.png')])
back_image_files = sorted([f for f in os.listdir(FOLDER) if f.endswith('_back.png')])

def create_page(image_files, folder_path, page_num, is_front=True, dpi=300):
    # A4 dimensions with higher DPI
    width, height = [dim * dpi // 72 for dim in A4]
    
    # Create a new PDF with Reportlab in memory
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    # Calculate image dimensions (2x4 grid with some padding)
    num_cols, num_rows = 2, 4
    margin = int(10 * dpi / 25.4)  # Convert mm to pixels at given DPI
    
    # Calculate image size
    img_width = (width - (margin * 3)) // num_cols
    img_height = (height - (margin * 5)) // num_rows
    
    # Place images in a 2x4 grid
    for row in range(num_rows):
        for col in range(num_cols):
            # Calculate image index
            image_index = page_num * (num_rows * num_cols) + row * num_cols + col
            
            # Check if we have more images
            if image_index < len(image_files):
                # Open the image
                img_path = os.path.join(folder_path, image_files[image_index])
                img = Image.open(img_path)
                
                # Calculate position
                if is_front:
                    x = margin + col * (img_width + margin)
                else:
                    # For back side, swap column positions
                    x = width - margin - (col + 1) * (img_width + margin)
                
                y = height - margin - (row + 1) * (img_height + margin)
                
                # Save temporary image
                temp_img_path = f"temp_image_{image_index}.png"
                
                # Resize image to fit while maintaining aspect ratio
                img.thumbnail((img_width, img_height), Image.LANCZOS)
                img.save(temp_img_path, dpi=(dpi, dpi))
                
                # Draw image on PDF
                c.drawImage(temp_img_path, x, y, width=img_width, height=img_height)
                
                # Remove temporary image
                os.remove(temp_img_path)
    
    # Save the PDF page
    c.save()
    
    # Get the value of the BytesIO buffer and write it to a file
    packet.seek(0)
    return packet

# Calculate number of pages
num_images = min(len(front_image_files), len(back_image_files))
num_pages = (num_images + 7) // 8  # Ceiling division to ensure all images are included

# Create the final merged PDF
output_pdf = PyPDF2.PdfWriter()

# Create pages for front and back images
for page_num in range(num_pages):
    # Create front page
    front_page_buffer = create_page(front_image_files, FOLDER, page_num, is_front=True)
    front_pdf_reader = PyPDF2.PdfReader(front_page_buffer)
    output_pdf.add_page(front_pdf_reader.pages[0])
    
    # Create back page
    back_page_buffer = create_page(back_image_files, FOLDER, page_num, is_front=False)
    back_pdf_reader = PyPDF2.PdfReader(back_page_buffer)
    output_pdf.add_page(back_pdf_reader.pages[0])

# Write the merged PDF to a file
with open("Participant_Images.pdf", "wb") as output_file:
    output_pdf.write(output_file)

print(f"Created Participant_Images.pdf with {num_pages * 2} pages.")