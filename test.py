import streamlit as st
import os
from dotenv import load_dotenv
from utils import summarizer
import openai
openai.api_key = os.getenv("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")

# Explicitly load .env from the current directory
load_dotenv(dotenv_path="./.env")

def main():
    # Set page configurations
    st.set_page_config(page_title="RESEARCH PAPER SUMMARIZER")
    
    st.title("RESEARCH PAPER SUMMARIZER")
    st.write("Summarize your research paper or PDF in a few seconds")
    st.divider()

    # Retrieve the OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please check your .env file.")
        return  # Stop execution if the API key is missing

    # Creating a file uploader widget to upload PDF files
    pdf = st.file_uploader('Upload your File', type='pdf')

    # Submit button for summarization
    submit = st.button("Generate summary")

    if submit and pdf:
        # Call the summarizer function with the uploaded PDF
        response = summarizer(pdf)

        # Display the summary of the PDF file
        st.subheader('Summary of File:')
        st.write(response)

if __name__ == '__main__':
    main()
