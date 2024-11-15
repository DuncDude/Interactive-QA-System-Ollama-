import os
import fitz  # PyMuPDF to read PDF files
import ollama
import chromadb
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from chromadb.config import Settings

# Configure logging to print out the requests and responses
logging.basicConfig(level=logging.DEBUG)

# Initialize the ChromaDB client
client = chromadb.Client(Settings(anonymized_telemetry=False))

# Function to extract text from a PDF file
def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Function to extract text from a Python file
def extract_text_from_python(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Function to chunk documents into smaller parts (e.g., paragraphs or sentences)
def chunk_document(text):
    return text.split("\n\n")

# Function to extract embeddings for a list of documents
def get_embeddings(documents):
    embeddings = []
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(lambda doc: ollama.embeddings(model="mxbai-embed-large", prompt=doc), documents))
        for response in responses:
            embeddings.append(response["embedding"])
    return embeddings

# Add documents to the database and return the collection
def add_documents_to_db(documents):
    # Check if the collection exists to avoid duplicates
    if "docs" in [col.name for col in client.list_collections()]:
        collection = client.get_collection("docs")
    else:
        collection = client.create_collection(name="docs")

    for i, doc in enumerate(documents):
        chunks = chunk_document(doc)
        embeddings = get_embeddings(chunks)  # Get embeddings in parallel
        for j, chunk in enumerate(chunks):
            collection.add(
                ids=[f"{i}_{j}"],
                embeddings=[embeddings[j]],
                documents=[chunk]
            )
    
    return collection

# Query the collection with the prompt embedding
def query_collection(collection, prompt):
    # Log the incoming prompt and when the query starts
    logging.debug(f"Querying the collection with prompt: {prompt}")

    start_time = time.time()  # Start tracking time
    
    response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
    
    # Log response time
    end_time = time.time()
    logging.debug(f"Ollama API call took {end_time - start_time:.2f} seconds")
    
    results = collection.query(query_embeddings=[response["embedding"]], n_results=1)
    return results['documents'][0][0]

# Function to interactively ask questions and get answers
def start_interactive_loop(collection):
    print("\nWelcome to the interactive Q&A system!")
    print("Ask your questions, or type 'exit' to quit.\n")

    while True:
        # Prompt the user for a question
        prompt = input("Your question: ")
        
        # Exit the loop if the user types 'exit'
        if prompt.lower() == 'exit':
            print("Exiting the Q&A system.")
            break
        
        # Query the database and retrieve the most relevant document
        relevant_chunk = query_collection(collection, prompt)
        
        # Generate a response using the retrieved document
        logging.debug(f"Generating response for prompt: {prompt}")
        output = ollama.generate(
            model="llama2-uncensored:latest",
            prompt=f"Using this data: {relevant_chunk}. Respond to this prompt: {prompt}"
        )
        
        # Print the generated answer
        print("\nGenerated Answer:")
        print(output["response"])

# Main logic
docs_folder = os.path.join(os.getcwd(), "docs")
documents = []

for filename in os.listdir(docs_folder):
    filepath = os.path.join(docs_folder, filename)
    if filename.endswith('.pdf'):
        documents.append(extract_text_from_pdf(filepath))
    elif filename.endswith('.py'):
        documents.append(extract_text_from_python(filepath))

# Add documents to the collection and create a vector database
collection = add_documents_to_db(documents)

# Start the interactive Q&A loop
start_interactive_loop(collection)
