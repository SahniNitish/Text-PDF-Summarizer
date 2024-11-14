import re
import streamlit as st
from pdfplumber import PDF
from transformers import pipeline

# Set up the Streamlit app
st.title("PDF and Text Summarizer")

# File upload section
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Text input section with word count display
text = st.text_area("Or enter text directly")
word_limit = 500  # Set the desired word limit

# Calculate and display the word count
word_count = len(text.split())
st.write(f"Word count: {word_count} / {word_limit}")

# Initialize the summarizer with an alternative model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Text cleaning function to remove unwanted patterns
def clean_text(text):
    # Remove duplicate words or phrases
    text = re.sub(r'(\b\w+\b)(\s+\1\b)+', r'\1', text)
    # Remove special characters and excessive spaces
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    return text.strip()

# Function to generate summary for large text
def summarize_large_text(text, chunk_size=1000, max_len=500, min_len=100):
    # Break text into chunks and summarize each
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = [summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]["summary_text"] for chunk in chunks]
    # Combine summaries and clean up
    combined_summary = " ".join(summaries)
    combined_summary = clean_text(combined_summary)
    return combined_summary

if st.button("Summarize"):
    if uploaded_file is not None:
        with PDF(uploaded_file) as pdf:
            pages = pdf.pages
            full_text = "\n".join([page.extract_text() for page in pages if page.extract_text() is not None])
            full_text = clean_text(full_text)  # Clean the text before summarizing
            if full_text.strip():
                summary = summarize_large_text(full_text, max_len=500, min_len=100)
                st.write("PDF Summary:")
                st.write(summary)
            else:
                st.write("The PDF does not contain extractable text.")
    elif text.strip():
        cleaned_text = clean_text(text)  # Clean the text before summarizing
        summary = summarize_large_text(cleaned_text, max_len=500, min_len=100)
        st.write("Text Summary:")
        st.write(summary)
    else:
        st.write("Please upload a PDF or enter some text to summarize.")