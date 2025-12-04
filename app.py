import os
import json
import fitz  
from flask import Flask, request, jsonify, render_template
from model_client import DistilLabsLLM

# --- 1. SETUP & CONFIGURATION ---
app = Flask(__name__)

# Configuration matches your Ollama setup
MODEL_NAME = "roast_master" 
PORT = 11434

# Initialize the Client
try:
    client = DistilLabsLLM(model_name=MODEL_NAME, port=PORT)
    print(f"✅ Connected to Model Client (Target: {MODEL_NAME})")
except Exception as e:
    print(f"❌ Error initializing client: {e}")
    client = None

# --- 2. PDF EXTRACTION HELPER ---
def extract_text_from_pdf(file_stream):
    """Reads a PDF file stream and converts it to plain text."""
    try:
        doc = fitz.open(stream=file_stream.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"PDF Error: {e}")
        return ""

# --- 3. FLASK ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    if not client:
        return jsonify({"error": "Model Client is not ready. Is Ollama running?"}), 500

    # Check if file part exists
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 1. Extract Text from PDF
        resume_text = extract_text_from_pdf(file)
        
        if len(resume_text.strip()) < 50:
            return jsonify({"error": "Could not read text. Is this PDF empty or scanned?"}), 400

        # 2. Call the Model 
        raw_response = client.invoke(resume_text)

        # 3. Clean & Parse Output
        clean_json = raw_response.replace("```json", "").replace("```", "").strip()
        json_response = json.loads(clean_json)
        
        return jsonify(json_response)

    except Exception as e:
        print(f"Processing Error: {e}")
        return jsonify({"error": "Failed to generate roast.", "details": str(e)}), 500

if __name__ == '__main__':
    # We allow the port to be set by environment for deployment flexibility
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)