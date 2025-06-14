import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq
import os
import re
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="AI Chart Generator with Groq",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 AI-Powered Chart Generator")
st.markdown("""
This application allows you to:
1. Upload a CSV file
2. Extract 20 random rows from your data
3. Describe what chart you want to create
4. Use Groq AI to generate the chart code automatically
5. Display the generated chart
""")

# Sidebar for API key and model selection
st.sidebar.header("⚙️ Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Enter your Groq API key. You can get one from https://console.groq.com/keys"
)

# Model selection
model_options = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    'qwen/qwen3-32b'
]
selected_model = st.sidebar.selectbox(
    "Select Groq Model",
    model_options,
    help="Choose the AI model for code generation"
)

# Initialize session state
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = None
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None

def initialize_groq_client(api_key):
    """Initialize Groq client with provided API key"""
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        return None

def extract_code_from_response(response_text):
    """Extract Python code from Groq response"""
    # Look for code blocks in markdown format
    code_pattern = r'```python\n(.*?)\n```'
    matches = re.findall(code_pattern, response_text, re.DOTALL)

    if matches:
        return matches[0].strip()

    # If no markdown code block, try to find code without markdown
    code_pattern = r'```\n(.*?)\n```'
    matches = re.findall(code_pattern, response_text, re.DOTALL)

    if matches:
        return matches[0].strip()

    # Return the whole response if no code blocks found
    return response_text.strip()

def generate_chart_code(client, model, sample_data, user_description):
    """Generate chart code using Groq AI"""

    # Prepare the data sample for the prompt
    data_info = f"""
    Data columns: {list(sample_data.columns)}
    Data types: {sample_data.dtypes.to_dict()}
    Sample data (first 5 rows):
    {sample_data.head().to_string()}

    Data shape: {sample_data.shape}
    """

    system_prompt = """You are a Python data visualization expert. Generate clean, executable Python code for creating charts using plotly or matplotlib.

    Rules:
    1. Use the provided sample_data DataFrame (it's already loaded)
    2. Generate code that creates a figure and assigns it to a variable called 'fig'
    3. Use plotly.express (px), plotly.graph_objects (go), or matplotlib.pyplot (plt)
    4. Include proper error handling
    5. Make the chart interactive and visually appealing
    6. Only return the code, no explanations
    7. Don't include imports - they're already imported
    8. The code should be ready to execute with exec()
    """

    user_prompt = f"""
    Based on this data information:
    {data_info}

    User wants: {user_description}

    Generate Python code to create this chart. Remember:
    - The DataFrame is called 'sample_data'
    - Assign the final figure to variable 'fig'
    - Use appropriate chart type based on the data and user request
    - Make it visually appealing
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating code: {str(e)}")
        return None

def safe_execute_code(code, sample_data):
    """Safely execute the generated code with restricted environment"""

    # Create a restricted environment for code execution
    restricted_globals = {
        '__builtins__': {
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
        },
        'pd': pd,
        'np': np,
        'px': px,
        'go': go,
        'plt': plt,
        'sns': sns,
        'sample_data': sample_data,
        'fig': None
    }

    try:
        # Execute the code in restricted environment
        exec(code, restricted_globals)
        return restricted_globals.get('fig'), None
    except Exception as e:
        return None, str(e)

# Main application
def main():
    # File upload section
    st.header("📁 Step 1: Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file to analyze"
    )

    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)

            st.success(f"✅ File uploaded successfully! Shape: {df.shape}")

            # Display basic info about the dataset
            with st.expander("📋 Dataset Overview"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Columns:**")
                    st.write(df.columns.tolist())
                    st.write("**Data Types:**")
                    st.write(df.dtypes.to_dict())

                with col2:
                    st.write("**Basic Statistics:**")
                    st.write(df.describe())

            # Extract random 20 rows
            st.header("🎲 Step 2: Random Sample")

            if st.button("Extract 20 Random Rows", type="primary"):
                if len(df) >= 20:
                    sample_data = df.sample(n=20, random_state=None)
                    st.session_state.sample_data = sample_data
                    st.success("✅ Random sample extracted!")
                else:
                    sample_data = df.copy()
                    st.session_state.sample_data = sample_data
                    st.warning(f"⚠️ Dataset has only {len(df)} rows. Using all data.")

            # Display sample data
            if st.session_state.sample_data is not None:
                st.subheader("📊 Sample Data (20 rows)")
                st.dataframe(st.session_state.sample_data, use_container_width=True)

                # Chart generation section
                st.header("🤖 Step 3: AI Chart Generation")

                if not api_key:
                    st.warning("⚠️ Please enter your Groq API key in the sidebar to continue.")
                    st.info("You can get a free API key from https://console.groq.com/keys")
                else:
                    # Initialize Groq client
                    client = initialize_groq_client(api_key)

                    if client:
                        # User input for chart description
                        user_description = st.text_area(
                            "Describe the chart you want to create:",
                            placeholder="E.g., Create a bar chart showing the relationship between category and values, or make a scatter plot of x vs y colored by category",
                            height=100
                        )

                        if st.button("🎨 Generate Chart", type="primary") and user_description:
                            with st.spinner("🤖 AI is generating your chart code..."):
                                # Generate code using Groq
                                code_response = generate_chart_code(
                                    client, selected_model, st.session_state.sample_data, user_description
                                )

                                if code_response:
                                    # Extract and clean the code
                                    generated_code = extract_code_from_response(code_response)
                                    st.session_state.generated_code = generated_code

                                    # Display the generated code
                                    st.subheader("🔧 Generated Code")
                                    st.code(generated_code, language='python')

                                    # Execute the code safely
                                    st.subheader("📈 Generated Chart")
                                    fig, error = safe_execute_code(generated_code, st.session_state.sample_data)

                                    if fig is not None:
                                        # Display the chart based on type
                                        if hasattr(fig, 'show'):  # Plotly figure
                                            st.plotly_chart(fig, use_container_width=True)
                                        else:  # Matplotlib figure
                                            st.pyplot(fig)

                                        st.success("✅ Chart generated successfully!")
                                    else:
                                        st.error(f"❌ Error executing code: {error}")
                                        st.info("💡 Try modifying your description or check if the column names match your data.")

                        # Option to manually edit and execute code
                        if st.session_state.generated_code:
                            st.subheader("✏️ Manual Code Editor")
                            edited_code = st.text_area(
                                "Edit the generated code if needed:",
                                value=st.session_state.generated_code,
                                height=200,
                                help="You can modify the generated code and re-execute it"
                            )

                            if st.button("🔄 Execute Edited Code"):
                                fig, error = safe_execute_code(edited_code, st.session_state.sample_data)

                                if fig is not None:
                                    if hasattr(fig, 'show'):  # Plotly figure
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:  # Matplotlib figure
                                        st.pyplot(fig)
                                    st.success("✅ Custom code executed successfully!")
                                else:
                                    st.error(f"❌ Error executing code: {error}")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please make sure you uploaded a valid CSV file.")

    else:
        st.info("👆 Please upload a CSV file to get started.")

    # Footer
    st.markdown("---")
    st.markdown("""
    **About this app:**
    - Built with Streamlit and Groq AI
    - Supports CSV file upload and random sampling
    - Generates charts using AI-powered code generation
    - Safe code execution with restricted environment
    - Interactive charts with Plotly and Matplotlib
    """)

if __name__ == "__main__":
    main()