# **Interactive Q&A System**

An interactive system that allows users to query a database of documents (PDFs and Python files) and receive meaningful, AI-generated responses based on the content of those documents.

---

## **Features**

- Extracts text from **PDF** and **Python (.py)** files.
- Splits extracted text into smaller chunks for efficient query processing.
- Leverages **ChromaDB** for vector storage and **Ollama** models for embeddings and response generation.
- Provides an interactive command-line interface for Q&A.
- Supports easy extensibility for new file formats and models.

---

## **Directory Structure**

Place your files in the following structure:

.
├── docs/                 # Directory for input documents
│   ├── file1.pdf         # Example PDF file (also where you'll put your files
│   ├── script.py         # Example Python script
|   |--(also where you'll put your files)
│   └── ...
├── main.py               # Main Python script
├── requirements.txt      # Python dependencies
├── README.md             # This README file

---

## **Installation**

1. **Install Python**: Ensure you have Python 3.8 or later installed. You can download it [here](https://www.python.org/downloads/).

2. **Clone this Repository**:
    ```bash
    git clone https://github.com/yourusername/Interactive-QA-System.git
    cd Interactive-QA-System
    ```

3. **Install Dependencies**:
    Use the provided `requirements.txt` file to install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Ollama**:
    - Follow the instructions on the [Ollama documentation](https://ollama.ai) to install the CLI.
    - Verify installation by running:
      ```bash
      ollama --version
      ```

5. **Download Ollama Models**:
    - Install the necessary Ollama models:
      ```bash
      ollama pull mxbai-embed-large
      ollama pull llama2-uncensored:latest
      ```

---

## **Usage**

### **Running the System**

1. Place your **PDF** and **Python (.py)** files inside the `docs` directory.
2. Start the program:
    ```bash
    python main.py
    ```
3. Interact with the system by typing questions. For example:
    ```
    Your question: What is the purpose of this Python script?
    ```

### **Example Workflow**

- Add `docs/myfile.pdf` and `docs/myscript.py` to the `docs` folder.
- Run `python main.py`.
- Query:
