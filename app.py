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
    # Replace common handwritten symbols with valid ones
    equation = equation.replace('×', '*').replace('÷', '/').replace(' ', '')
    
    # Ensure multiplication is explicit (e.g., "2x" -> "2*x")
    cleaned = []
    for i, char in enumerate(equation):
        if char.isdigit() and i + 1 < len(equation) and equation[i + 1] in 'x(':
            cleaned.append(char + '*')
        else:
            cleaned.append(char)
    cleaned = ''.join(cleaned)
    
    # Remove any invalid characters
    allowed_chars = "0123456789+-*/=().x"
    cleaned = ''.join(char for char in cleaned if char in allowed_chars)
    
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

        # Display raw extracted equation
        st.write(f"**Raw Extracted Equation:** {equation}")

        # Clean the extracted equation
        cleaned_equation = clean_equation(equation)

        # Check if equation is empty
        if not cleaned_equation:
            st.error("❌ No valid equation detected. Please try a clearer image.")
            continue

        # Check if the equation contains an equal sign
        if '=' not in cleaned_equation:
            st.error("❌ Equation must contain an equal sign (=).")
            continue

        # Display cleaned equation
        st.success(f"**Cleaned Equation:** {cleaned_equation}")

        try:
            x = symbols('x')
            
            # Split the equation into LHS and RHS
            lhs, rhs = cleaned_equation.split('=')
            
            # Parse both sides of the equation
            lhs_expr = sympify(lhs)
            rhs_expr = sympify(rhs)
            
            # Create the equation
            sympy_eq = Eq(lhs_expr, rhs_expr)
            
            # Solve the equation
            solution = solve(sympy_eq, x)
            
            if solution:
                st.success(f"**Solution:** x = {solution[0]}")
            else:
                st.error("❌ No solution found!")
        except SyntaxError:
            st.error("⚠️ Invalid equation syntax. Please ensure the equation is correctly formatted.")
        except Exception as e:
            st.error(f"⚠️ Error solving equation: {e}")
