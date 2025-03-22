import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from sympy import sympify, Eq, solve, symbols

# Title
st.title("📝 Handwritten Math Solver Using AI")

# File uploader
uploaded_files = st.file_uploader("Upload Math Equation Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def clean_equation(equation):
    # ✅ Sirf allowed characters ko allow karein
    allowed_chars = "0123456789+-*/=().x "
    cleaned = ''.join(char for char in equation if char in allowed_chars)
    return cleaned.strip()

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

        # ✅ Clean and validate equation
        cleaned_equation = clean_equation(equation)

        # ✅ Agar equation blank hai toh error handle karein
        if not cleaned_equation:
            st.error("❌ No valid equation detected. Please try a clearer image.")
            continue
        
        # ✅ Display extracted equation
        st.success(f"**Extracted Equation:** {cleaned_equation}")

        try:
            # ✅ Fix for tuple issue - Separate LHS and RHS properly
            x = symbols('x')

            # ✅ Equal sign ke bina equation ko handle karein
            if '=' in cleaned_equation:
                lhs, rhs = cleaned_equation.split('=')
                sympy_eq = Eq(sympify(lhs), sympify(rhs))
            else:
                sympy_eq = sympify(cleaned_equation)
                sympy_eq = Eq(sympy_eq,0) #solve for equation equals zero.

            # ✅ Solve the equation
            solution = solve(sympy_eq, x)

            if solution:
                if isinstance(solution, list):
                    st.success(f"**Solution:** x = {solution[0]}")
                else:
                    st.success(f"**Solution:** x = {solution}")
            else:
                st.error("❌ No solution found!")
        except Exception as e:
            st.error(f"⚠️ Error solving equation: {e}")
