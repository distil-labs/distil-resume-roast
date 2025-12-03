import sys
import json
import fitz  
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# --- 1. ADDED: Prompt Generator (The missing instruction layer) ---
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

    # 3. Call Ollama (Local)
    with Progress(
        SpinnerColumn("dots", style="red"),
        TextColumn("[bold red]Roasting this poor soul...[/bold red]"),
        transient=True,
    ) as progress:
        progress.add_task("roasting", total=None)
        
        # --- 2. ADDED: Wrap the text in the prompt instructions ---
        final_prompt = generate_roast_prompt(resume_text)

        try:
            response = ollama.generate(
                model='roast_master', 
                prompt=final_prompt,  
                format='json',    
                stream=False,
                options={
                    'num_ctx': 8192,   
                    'temperature': 0.8
                }
            )
        except Exception as e:
            console.print(f"[bold red]❌ Ollama Error:[/bold red] Is Ollama running? ({e})")
            sys.exit(1)

    # 4. Parse & Display
    try:
        data = json.loads(response['response'])
        
        # RATING
        rating = data.get('rating', 0)
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
        console.print("[bold red]❌ Error:[/bold red] The model burped and didn't output valid JSON.")
        console.print(response['response'])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("Usage: python roast.py [path_to_resume.pdf]")
    else:
        roast_resume(sys.argv[1])