# 🤖 RAG-based Commit Message Generator

An AI-powered tool that automatically generates high-quality, conventional commit messages from your `git diff` output. This project leverages a **Retrieval-Augmented Generation (RAG)** architecture, using the extensive commit history of the **TensorFlow** repository as a knowledge base to produce contextually relevant and stylistically consistent commit messages with **Google's Gemini 2.0 Flash**.

## The Problem
Manually writing descriptive and consistent commit messages is a time-consuming but crucial task for maintaining a clean project history. Developers often struggle to succinctly summarize complex changes, leading to inconsistent or uninformative commit logs. This tool aims to automate that process, saving time and improving the quality of your version control history.

## 🚀 How It Works (RAG Architecture)
This tool goes beyond simple text generation by using a sophisticated RAG pipeline to provide rich context to the Large Language Model (LLM).

1.  **Input:** The user provides a `git diff` of their staged changes.
2.  **Embedding:** The `git diff` content is converted into a numerical vector (embedding) using a `SentenceTransformer` model. This vector represents the semantic meaning of the code changes.
3.  **Retrieval:** The system uses **FAISS (Facebook AI Similarity Search)** to search a pre-built knowledge base (created from thousands of TensorFlow commit messages) for the top 5 most semantically similar commit examples.
4.  **Augmentation:** A detailed prompt is constructed, combining the user's `git diff`, the retrieved high-quality examples, and specific instructions.
5.  **Generation:** This enriched prompt is sent to the **Google Gemini 2.0 Flash** API, which generates a final, well-structured commit message.

## 📊 Results and Evaluation
The model's performance is evaluated qualitatively based on its ability to generate relevant, accurate, and stylistically correct commit messages for a given set of code changes.

The RAG approach proves highly effective, consistently producing messages that correctly identify the commit type (e.g., `feat`, `fix`, `refactor`) and provide a concise, meaningful summary.

**Example:**

Given a complex `git diff` that introduces a new user validation feature (creating a new `validator.py` file and modifying `main.py` to use it), the model generated the following high-quality commit message:

**Generated Commit Message:**
```
feat: add user input validation

Introduces a new Validator class to validate username and email formats before user registration.

The registration logic in main.py is updated to use this new validator to ensure data integrity and prevent invalid entries.
```
This result demonstrates the model's ability to understand changes across multiple files, synthesize the core purpose of the changes, and adhere to the conventional commit format.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Core Framework:** LangChain
* **Large Language Model (LLM):** Google Gemini 2.0 Flash
* **Embedding Model:** `sentence-transformers` (`all-MiniLM-L6-v2`)
* **Vector Database:** FAISS (Facebook AI Similarity Search)

## 📁 Project Structure
```
rag-based-commit-message-generator/
│
├── data/
│   ├── commit_messages.txt
│   ├── faiss_index.bin
│   └── commit_texts.pkl
│
├── src/
│   ├── build_knowledge_base.py
│   ├── main.py
│   └── rag_chain.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Setup and Installation Guide

#### Step 1: Clone the Repository
```bash
git clone [YOUR_REPOSITORY_URL]
cd rag-based-commit-message-generator
```

#### Step 2: Create and Activate a Virtual Environment
```bash
# Create the virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Set Up Your API Key
1.  Create a file named `.env` in the project's root directory.
2.  Get your API key from [Google AI Studio](https://aistudio.google.com/).
3.  Add your key to the `.env` file:
    ```
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```

#### Step 5: Build the Knowledge Base
This tool requires a knowledge base of commit messages. The following steps will download the TensorFlow commit history and process it.
```bash
# 1. Clone the TensorFlow repository (a shallow clone is sufficient)
git clone --depth 100 [https://github.com/tensorflow/tensorflow.git](https://github.com/tensorflow/tensorflow.git) ../tensorflow-data

# 2. Extract the commit logs and move them to the data directory
cd ../tensorflow-data && git log --pretty=%B > ../rag-based-commit-message-generator/data/commit_messages.txt
cd ../rag-based-commit-message-generator

# 3. Run the script to build the FAISS index (this may take 5-15 minutes)
python src/build_knowledge_base.py
```

## 📖 Usage

#### Method 1: Manual Generation
You can generate a commit message for any `diff` content stored in a text file.
1.  Save your `git diff` output to a file (e.g., `my_diff.txt`).
2.  Run the main script from the project root:
    ```bash
    python -m src.main my_diff.txt
    ```

#### Method 2: Automated with Git Hooks (Recommended)
Integrate the script to run automatically every time you `git commit`.
1.  Find the absolute path to your virtual environment's Python executable:
    ```bash
    # On Windows (in CMD or PowerShell)
    where python
    ```
2.  Create a new file at `.git/hooks/prepare-commit-msg` (no file extension).
3.  Paste the following script into the file, **updating the `PYTHON_EXEC` variable** with the path you found above.
    ```bash
    #!/bin/bash
    COMMIT_MSG_FILE=$1
    STAGED_DIFF=$(git diff --staged)
    
    if [ -z "$STAGED_DIFF" ]; then
        exit 0
    fi
    
    echo "🤖 Generating AI commit message..."
    
    export PYTHONIOENCODING=utf-8
    PYTHON_EXEC="C:\path\to\your\project\venv\Scripts\python.exe" # <-- IMPORTANT: UPDATE THIS PATH
    
    AI_MSG=$("$PYTHON_EXEC" "src/main.py" --diff "$STAGED_DIFF")
    
    echo "$AI_MSG" > "$COMMIT_MSG_FILE"
    ```
4.  Make the hook executable (if using Git Bash or on macOS/Linux):
    ```bash
    chmod +x .git/hooks/prepare-commit-msg
    ```
5.  Now, simply run `git add .` and `git commit`, and the message will be generated automatically.

## ✨ Future Improvements
-   **Multi-Source Retrieval:** Enhance the knowledge base by retrieving from docstrings and issue tracker discussions in addition to commit messages.
-   **Fine-Tuning:** Fine-tune the embedding model on a dedicated `(git diff, commit message)` dataset for more accurate retrieval.
-   **VS Code Extension:** Package the tool into a Visual Studio Code extension for a seamless UI integration.

## 👤 Author
-   **Phuong Linh**
-   [GitHub](YOUR_GITHUB_LINK) | [LinkedIn](YOUR_LINKEDIN_LINK)
