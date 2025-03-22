import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from sympy import sympify, solve, Eq, symbols

# Title
st.title("📝 Handwritten Math Solver Using AI")

# File uploader
uploaded_files = st.file_uploader("Upload Math Equation Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Load image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Preprocessing
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Extract text using EasyOCR
        with st.spinner("🔎 Extracting equation..."):
            result = reader.readtext(binary)
            equation = ''.join([text[1] for text in result])

        # Display extracted equation
        if equation:
            st.success(f"**Extracted Equation:** {equation}")

            try:
                # Solve the equation
                st.subheader("📐 Solving Equation...")
                x = symbols('x')
                sympy_eq = sympify(equation.replace('=', '-(') + ')')
                solution = solve(sympy_eq, x)

                if solution:
                    st.success(f"**Solution:** x = {solution[0]}")
                else:
                    st.error("❌ No solution found!")
            except Exception as e:
                st.error(f"⚠️ Error solving equation: {e}")
        else:
            st.error("❌ No equation detected. Please try a clearer image.")
