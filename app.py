import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

# Set Tesseract path (update this path based on your Tesseract installation)
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit App
st.title("Handwritten Math Solver Using AI")
st.write("Upload images of handwritten mathematical equations, and the app will solve them for you!")

# Upload multiple images
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.subheader(f"**Image {i + 1}:**")
        
        # Read the image
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded Image {i + 1}', use_container_width=True)

        # Convert to OpenCV format
        image_cv = np.array(image)

        # Ensure the image has 3 channels (RGB)
        if len(image_cv.shape) == 2:  # Grayscale image
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_GRAY2RGB)
        elif image_cv.shape[2] == 4:  # RGBA image (with transparency)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2RGB)

        # Convert to grayscale
        gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)

        # Preprocess the image (improves OCR accuracy)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Use Tesseract OCR to recognize text
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789+-*/÷()"'
        equation = pytesseract.image_to_string(binary, config=custom_config)

        # Print raw output for debugging
        st.write(f"**Raw Recognized Equation:** {equation}")

        # Clean the recognized equation
        equation = equation.strip().replace(" ", "").replace("\n", "")

        # Map common OCR misreadings to correct symbols
        ocr_mappings = {
            'S': '5', 's': '5', 'T': '+', 't': '+', 'x': '*', 'X': '*', 
            'o': '0', 'O': '0', 'l': '1', 'L': '1', 'z': '2', 'Z': '2',
            'a': '4', 'A': '4', 'b': '6', 'B': '6', 'g': '9', 'G': '9',
            '÷': '/'  # Fix division symbol
        }

        # Replace misread characters in the equation
        equation = ''.join([ocr_mappings.get(char, char) for char in equation])

        # Remove invalid characters (keep only digits, operators, and parentheses)
        equation = re.sub(r'[^\d+\-*/().]', '', equation)

        st.write(f"**Cleaned Equation:** {equation}")

        # Validate the equation (allow only digits and basic operators)
        if re.match(r'^[\d+\-*/().]+$', equation):
            try:
                # Evaluate the equation
                result = eval(equation)
                st.success(f"**Result:** {result}")
            except Exception as e:
                st.error(f"Error: Unable to solve the equation. Details: {e}")
        else:
            st.error("Error: The recognized equation contains invalid characters. Please ensure the equation is clear and valid.")