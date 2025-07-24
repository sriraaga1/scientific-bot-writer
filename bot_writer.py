import streamlit as st
import pdfplumber
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API Key from environment
api_key = os.getenv("DEESEEK_API_KEY")

def extract_text_from_pdf(file):
    """Extract and clean text from uploaded PDF file"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    # Clean extra spaces and line breaks
    cleaned_text = ' '.join(text.split())
    return cleaned_text

def generate_summary_deepseek(api_key, text, age_group, profession, knowledge_level):
    """
    Call DeepSeek API (via OpenRouter) to generate tailored summary
    """
    prompt = f"""
You are an expert summarizer. Review the following text, then produce a clear summary that fits the reader’s background and needs:

- Audience age group: {age_group}
- Profession: {profession}
- Background knowledge: {knowledge_level} (Beginner / Intermediate / Expert)

Instructions:
1. Write a summary in no more than 300 words.
2. Use vocabulary and explanations suitable for this audience.
3. Highlight the most important findings, conclusions, or actionable insights from the original text.
4. Avoid jargon whenever possible, unless the reader’s background implies expertise.
5. If complex concepts are involved, explain them simply for beginners, or assume familiarity for experts.

Text to summarize:
\"\"\" 
{text}
\"\"\"
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.95,
        "n": 1,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()
        summary = json_response['choices'][0]['message']['content']
        return summary
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        try:
            st.error(f"Details: {response.json()}")
        except Exception:
            pass
    except Exception as err:
        st.error(f"Unexpected error occurred: {err}")

    return None

# Streamlit UI
st.title("PDF Summarizer Bot ")

if not api_key:
    st.error("DeepSeek API key not found. Please set DEESEEK_API_KEY in your .env file.")
    st.stop()

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.text_area("Extracted Text ", text, height=200)

    age_group = st.selectbox("Select Age Group", ["Child", "Teen", "Adult", "Senior"])
    profession = st.text_input("Enter Profession")
    knowledge_level = st.selectbox("Knowledge Level", ["Beginner", "Intermediate", "Expert"])

    if st.button("Generate Summary"):
        if not profession.strip():
            st.warning("Please enter a profession.")
        else:
            with st.spinner("Generating summary with DeepSeek..."):
                summary = generate_summary_deepseek(api_key, text, age_group, profession.strip(), knowledge_level)
            if summary:
                st.subheader("Summary Output")
                st.write(summary)
else:
    st.info("Upload a PDF file to extract text and generate summary.")
