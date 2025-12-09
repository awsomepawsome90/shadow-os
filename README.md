# Shadow OS

This repository contains the source code for the Shadow OS project, a custom RAG (Retrieval-Augmented Generation) system designed to stream intelligence to Even Realities G2 Smart Glasses.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:
- Git
- Python 3.10 or higher
- `pip` (Python package installer)

## Setup Instructions

Follow these steps to get the project running on a new computer.

### 1. Clone the Repository
Open your terminal and run the following command to download the project files:
```bash
git clone https://github.com/awsomepawsome90/shadow-os.git
```

### 2. Navigate to the Project Directory
Change into the newly created project folder:
```bash
cd shadow-os
```

### 3. Create and Activate a Python Virtual Environment
This keeps the project's dependencies isolated from your system.
```bash
# Create the virtual environment
python3 -m venv backend_venv

# Activate the virtual environment
source backend_venv/bin/activate
```
**Note:** Your terminal prompt should now be prefixed with `(backend_venv)`.

### 4. Install Dependencies
Install all the required Python packages using the `requirements.txt` file:
```bash
pip install -r backend/requirements.txt
```

### 5. Configure Your Gemini API Key
The application requires a Gemini API key to function.

a. Create a new file named `.env` inside the `backend` directory:
```bash
touch backend/.env
```

b. Open the `backend/.env` file with a text editor and add your API key in the following format, replacing `"your_api_key_here"` with your actual key:
```
GEMINI_API_KEY="your_api_key_here"
```

### 6. Populate the Knowledge Base
The RAG system needs data to draw answers from.

a. Place one or more `.txt` or `.pdf` files into the `data/` directory.

b. Run the ingestion script to process your documents and load them into the local vector database:
```bash
python backend/ingest_docs.py
```

## Running the Application

### 1. Start the Backend Server
With your virtual environment still active, run the following command from the main `shadow-os` directory to start the FastAPI server:
```bash
./backend_venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
The server is now running and listening for requests. Leave this terminal window open.

### 2. Test the RAG Pipeline
To verify that everything is working, open a **new, separate terminal window**.

a. Navigate back to the project directory and activate the virtual environment in this new terminal:
```bash
cd path/to/shadow-os
source backend_venv/bin/activate
```

b. Run the test script:
```bash
python test_brain.py
```

You should see a `--- ✅ SUCCESS ---` message followed by a JSON response, confirming the entire pipeline is operational.
