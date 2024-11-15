import re
import streamlit as st
import cohere
from pdfplumber import PDF

# Initialize Cohere client with API key
COHERE_API_KEY = 'mL5NDWoXHW0UiUqd4uoxbe7Om27Q82OyLukMrjgk'  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

# Custom CSS to style Streamlit components
st.markdown("""
    <style>
        /* Set main background color */
        .stApp {
            background-color: #f4f7fa;
        }
        /* Title styling */
        .title {
            font-size: 2em;
            color: #333333;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #0078D7;
            color: white;
            border-radius: 10px;
        }
        /* File uploader and text input styling */
        .input-section {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        /* Button styling */
        .stButton > button {
            background-color: #0078D7;
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-size: 1em;
            font-weight: bold;
        }
        /* Summary output styling */
        .summary-section {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            color: #333333;
            line-height: 1.6;
            margin-top: 20px;
        }
        /* Word count styling */
        .word-count {
            font-size: 0.9em;
            color: #666;
            margin-top: -15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown('<div class="title">PDF and Text Summarizer</div>', unsafe_allow_html=True)

# File upload and text input section
with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Text input with word count
    text = st.text_area("Or enter text directly")
    word_limit = 500  # Word limit for input text
    word_count = len(text.split())
    st.markdown(f'<p class="word-count">Word count: {word_count} / {word_limit}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Function to clean text
def clean_text(text):
    text = re.sub(r'(\b\w+\b)(\s+\1\b)+', r'\1', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    return text.strip()

# Function to call Cohere API for summarization
def cohere_summarize(text):
    response = co.summarize(
        text=text,
        length="short"  # Options: short, medium, long
    )
    return response.summary if response else "Unable to generate summary."

# Summarize button and output display
if st.button("Summarize"):
    if uploaded_file is not None:
        with PDF(uploaded_file) as pdf:
            full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text() is not None])
            full_text = clean_text(full_text)
            if full_text:
                summary = cohere_summarize(full_text)
                st.markdown('<div class="summary-section"><h3>PDF Summary:</h3><p>' + summary + '</p></div>', unsafe_allow_html=True)
            else:
                st.write("The PDF does not contain extractable text.")
    elif text.strip():
        cleaned_text = clean_text(text)
        summary = cohere_summarize(cleaned_text)
        st.markdown('<div class="summary-section"><h3>Text Summary:</h3><p>' + summary + '</p></div>', unsafe_allow_html=True)
    else:
        st.write("Please upload a PDF or enter some text to summarize.")
