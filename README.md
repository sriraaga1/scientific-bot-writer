# scientific-bot-writer

A beginner-friendly GenAI project that summarizes scientific research PDFs based on user preferences.

## Project Overview

This app allows users to:
- Upload research papers in PDF format
- Clean the content by removing special characters and citations
- Personalize the output using dropdown-based form inputs
- Automatically generate a human-readable summary using a Generative AI model

## Folder Structure

scientific-bot-writer/
├── app.py # Main Streamlit app
├── bot_writer.py # Handles PDF extraction and cleaning
├── requirements.txt # List of required Python packages
├── sample.pdf # Test PDF file
└── README.md # Project overview and instructions

##  Tech Stack

- **Python**
- **Streamlit** for UI
- **Transformers (HuggingFace)** for text generation
- **PyMuPDF** for PDF parsing

## How It Works

1. User uploads a PDF file
2. Text is extracted and cleaned
3. User selects options like profession, age group, tone
4. The app uses a prompt + selected data + cleaned text to generate a summary
5. Summary is displayed for download or copy

##  How to Run It

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the Streamlit app
streamlit run app.py


Example Prompt (Behind the Scenes)
css
Copy
Edit
"Summarize this research paper for a 25-year-old software engineer in a friendly tone."



Future Improvements
Add multi-language support

Allow summary export as Word/PDF

Integrate citation generator

Improve PDF parsing with AI OCR
