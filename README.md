# **Handwritten Math Solver Using AI**

This is a Streamlit app that extracts and solves handwritten math equations using EasyOCR and SymPy.

## **🚀 Features**
- ✅ Upload multiple handwritten math equation images
- ✅ Extract equation using EasyOCR
- ✅ Clean and validate extracted equations
- ✅ Solve equations using SymPy
- ✅ Display solution or error if no solution is found

## **🛠️ How to Run**
1. Clone the repository:
``` bash
git clone https://github.com/your-username/handwritten-math-solver.git
```
2. Navigate to the project folder:
``` bash
cd handwritten-math-solver
```
3. Install dependencies:
``` bash
pip install -r requirements.txt
```
4. Run the Streamlit app:
``` bash
streamlit run app.py
```
## **📂 Dependencies**
- streamlit
- opencv-python
- numpy
- Pillow
- easyocr
- sympy

## **📝 Usage**
1. Upload a math equation image.
2. The app will extract and clean the equation.
3. If the equation is valid, it will be solved and the solution will be displayed.
4. If there's an error, an appropriate message will be shown.
### **💡 Example**
```
Input: 2x + 4 = 10
Output: x = 3
```

## **📌 Note**
- Ensure the uploaded image is clear and well-lit for better recognition.
- Supports only basic algebraic equations.
## **🏆 Contributors**
Amna Shahzad
