import sys
import json
import fitz  
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# --- IMPORT YOUR NEW CLIENT ---
from model_client import DistilLabsLLM

console = Console()
MODEL_NAME = "roast_master" 

def extract_text_from_pdf(pdf_path):
    """Reads the PDF and extracts raw text."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        console.print(f"[bold red]❌ Error reading PDF:[/bold red] {e}")
        sys.exit(1)

def roast_resume(pdf_path):
    # 1. Banner
    console.print(Panel.fit("[bold red]🔥 RESUME ROAST MASTER 🔥[/bold red]", border_style="red"))

    # 2. Extract
    resume_text = extract_text_from_pdf(pdf_path)
    if len(resume_text.strip()) < 50:
        console.print("[bold yellow]⚠️ Warning:[/bold yellow] This PDF looks empty or is a scanned image.")
        return

    # --- 3. INITIALIZE CLIENT (The Standard Way) ---
    try:
        client = DistilLabsLLM(model_name=MODEL_NAME)
    except Exception as e:
        console.print(f"[bold red]❌ Client Init Failed:[/bold red] {e}")
        sys.exit(1)

    # 4. Invoke Model
    with Progress(
        SpinnerColumn("dots", style="red"),
        TextColumn("[bold red]Roasting this poor soul...[/bold red]"),
        transient=True,
    ) as progress:
        progress.add_task("roasting", total=None)
        
        try:
            # Clean one-line call
            raw_response = client.invoke(resume_text)
        except Exception as e:
            console.print(f"[bold red]❌ Model Error:[/bold red] {e}")
            sys.exit(1)

    # 5. Parse & Display
    try:
        # Sanitize output (remove markdown blocks if present)
        clean_json = raw_response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        
        # RATING
        rating = data.get('rating', 0)
        if isinstance(rating, str):
            try: rating = int(rating.split('/')[0])
            except: rating = 0

        color = "green" if rating >= 8 else "yellow" if rating >= 5 else "red"
        console.print(f"\n[bold {color}]RATING: {rating}/10[/bold {color}]")
        
        # THE ROAST
        console.print(Panel(
            data.get('roast_critique', 'No roast generated.'),
            title="💀 The Critique",
            border_style="red",
            padding=(1, 2)
        ))
        
        # THE ADVICE
        console.print("\n[bold cyan]✨ Professional Fixes:[/bold cyan]")
        for tip in data.get('professional_suggestions', []):
            console.print(f" ✅ {tip}")
            
    except json.JSONDecodeError:
        console.print("[bold red]❌ Error:[/bold red] The model output invalid JSON.")
        console.print(f"Raw Output: {raw_response}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("Usage: python roast.py [path_to_resume.pdf]")
    else:
        roast_resume(sys.argv[1])