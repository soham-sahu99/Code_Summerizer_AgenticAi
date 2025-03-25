# SOHAM SAHU
# roll no : 22052158 

import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai

from dotenv import load_dotenv  
load_dotenv()
import os

# Load API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
 
# Page configuration
st.set_page_config(
    page_title="AI Code Summarizer",
    page_icon="🖥️",
    layout="wide"
)

st.title("SOHAM'S AI Code Summarizer 🖥️")
st.header("Powered by SOHAM")




@st.cache_resource
def initialize_agent():
    return Agent(
        name="Code AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

## Initialize the agent
code_agent = initialize_agent()

# Text area for code input
code_input = st.text_area(
    "Paste your code here:",
    placeholder="Enter your code snippet...",
    help="The AI agent will analyze and summarize the code."
)

if st.button("😮 Summarize Code", key="summarize_code_button"):
    if not code_input.strip():
        st.warning("Please enter some code to analyze.")
    else:
        try:
            with st.spinner("Analyzing and summarizing the code..."):
                # Generate analysis prompt
                analysis_prompt = (
                    f"""
                    Analyze the given code and provide a clear and concise summary.
                    Explain its functionality, key components, and potential optimizations.
                    Also, include real-world applications if relevant.

                    Code:
                    ```
                    {code_input}
                    ```
                    """
                )

                # AI agent processing
                response = code_agent.run(analysis_prompt)

            # Display the result
            st.subheader("Code Summary")
            st.markdown(response.content)

        except Exception as error:
            st.error(f"An error occurred during analysis: {error}")

# Section to ask questions about the code
st.subheader("Ask a Question About the Code")
question_input = st.text_input(
    "Enter your question:",
    placeholder="Ask something about the code..."
)

if st.button("🤔 Ask Question", key="ask_question_button"):
    if not code_input.strip():
        st.warning("Please enter a code snippet first.")
    elif not question_input.strip():
        st.warning("Please enter a question to ask about the code.")
    else:
        try:
            with st.spinner("Analyzing and answering your question..."):
                # Generate question prompt
                question_prompt = (
                    f"""
                    The user has provided the following code:
                    ```
                    {code_input}
                    ```
                    
                    The user asks:
                    "{question_input}"
                    
                    Provide a clear, concise, and accurate answer.
                    """
                )

                # AI agent processing
                response = code_agent.run(question_prompt)

            # Display the result
            st.subheader("Answer")
            st.markdown(response.content)

        except Exception as error:
            st.error(f"An error occurred while answering the question: {error}")
