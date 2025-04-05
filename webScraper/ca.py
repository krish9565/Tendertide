import easyocr

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # Pass the language as a list, e.g., ['en'] for English

# Read text from the image
result = reader.readtext('output_image.png')

# Print the detected text
for detection in result:
    print(f"Detected text: {detection[1]}")
