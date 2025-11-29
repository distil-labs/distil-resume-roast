import os
import json
import torch
import fitz  # PyMuPDF
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from huggingface_hub import login
from dotenv import load_dotenv

# --- 1. SETUP & CONFIGURATION ---
load_dotenv()  # Load .env for local development

app = Flask(__name__)

# Get token (Securely)
HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_ID = "Priyansu19/Rost-Resume"

if HF_TOKEN:
    login(token=HF_TOKEN)

# --- 2. LOAD MODEL (CPU/GPU SAFE MODE) ---
print("Loading Model... (This runs once at startup)")

# Detect Hardware
device_map = "auto"
model_kwargs = {}

if torch.cuda.is_available():
    print("✅ GPU Detected: Enabling 4-bit quantization for speed.")
    model_kwargs = {"load_in_4bit": True}
else:
    print("⚠️ No GPU Detected: Loading in standard mode (slower but stable).")
    # On CPU, we don't use 4-bit because bitsandbytes is GPU-only usually.
    # The 16GB RAM in Free Tier is enough for the 6GB model.
    model_kwargs = {} 

try:
    roaster = pipeline(
        "text-generation",
        model=MODEL_ID,
        token=HF_TOKEN,
        device_map=device_map,
        model_kwargs=model_kwargs,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Critical Error Loading Model: {e}")
    roaster = None

# --- 3. PDF EXTRACTION HELPER ---
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

# --- 4. PROMPT GENERATOR ---
def generate_roast_prompt(resume_text):
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

## Task
Generate a brutally honest 'roast' critique of the provided resume.
The output MUST be a pure, stringified JSON object with exactly these fields:
- "roast_critique": Sarcastic, funny, mean paragraph.
- "professional_suggestions": List of 3 actionable tips.
- "rating": Integer 1-10.

<|eot_id|><|start_header_id|>user<|end_header_id|>

Process the context according to the task description.

Context:
{resume_text}

<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

# --- 5. FLASK ROUTES ---

@app.route('/')
def home():
    # Renders templates/index.html
    return render_template('index.html')

@app.route('/roast', methods=['POST'])
def roast():
    if not roaster:
        return jsonify({"error": "Model failed to load. Check server logs."}), 500

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
            return jsonify({"error": "Could not read text from this PDF. Is it a scanned image?"}), 400

        # 2. Build Prompt
        prompt = generate_roast_prompt(resume_text)

        # 3. Generate Response
        # On CPU, this might take 30-60 seconds.
        outputs = roaster(
            prompt,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.8, # Slightly higher for creativity
        )

        # 4. Parse Output
        raw_output = outputs[0]["generated_text"].split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
        
        # Remove markdown code blocks if present
        if raw_output.startswith("```json"):
            raw_output = raw_output.replace("```json", "").replace("```", "")
        
        # Parse JSON
        json_response = json.loads(raw_output)
        
        return jsonify(json_response)

    except Exception as e:
        print(f"Processing Error: {e}")
        # Return the raw output for debugging if JSON parsing fails
        return jsonify({"error": "Failed to generate valid JSON.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)