from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader

def process_text(text):
    # Process the given text, splitting it into chunks and creating embeddings

    # Initialize a text splitter to divide the text into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",  # <-- Corrected 'separator'
        chunk_size=1000,  # Size of each chunk
        chunk_overlap=200,  # Overlap between chunks
        length_function=len,
    )

    chunks = text_splitter.split_text(text)  # Split the text into chunks

    # Load the HuggingFace model for generating embeddings
    embedding = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a FAISS index from text chunks using embeddings
    knowledgeBase = FAISS.from_texts(chunks, embedding)

    return knowledgeBase

def summarizer(PDF):
    # Summarize the content in the provided PDF file
    if PDF is not None:
        # Read the PDF file
        pdf_reader = PdfReader(PDF)
        text = ""

        # Extract text from each page of the PDF
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        # Process the extracted text to create a knowledge base
        knowledgeBase = process_text(text)

        query = "Summarize the content of the uploaded PDF file in 3-5 sentences."

        if query:
            # Search the knowledge base with the query
            docs = knowledgeBase.similarity_search(query)

            # Initialize the OpenAI model
            OpenAIModel = "gpt-40-mini"
            llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)

            # Load the QA chain
            chain = load_qa_chain(llm, chain_type='stuff')

            with get_openai_callback() as cost:
                # Run the chain and print the cost
                response = chain.run(input_documents=docs, question=query)
                print(cost)

                return response
