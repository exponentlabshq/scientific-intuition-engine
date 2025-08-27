import os
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (v0.28.x style)
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set; cannot run analysis.")
openai.api_key = OPENAI_API_KEY

def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from a PDF."""
    return extract_text(pdf_path)

def load_prompt(prompt_path: str) -> str:
    """Load the UMPF system prompt."""
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def run_umfp_analysis(system_prompt: str, paper_text: str) -> str:
    """Run the UMPF analysis using ChatCompletion (v0.28-compatible)."""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": paper_text},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message["content"]

if __name__ == "__main__":
    inputs_dir = "inputs"
    prompts_dir = "prompts"
    outputs_dir = "outputs"

    # Auto-pick first PDF in inputs/
    pdf_candidates = [f for f in os.listdir(inputs_dir) if f.lower().endswith(".pdf")]
    if not pdf_candidates:
        raise SystemExit("No PDFs found in inputs/")
    pdf_file = os.path.join(inputs_dir, sorted(pdf_candidates)[0])

    # Use md prompt file if present
    prompt_path_md = os.path.join(prompts_dir, "umpf_system_prompt.md")
    prompt_path_txt = os.path.join(prompts_dir, "umpf_system_prompt.txt")
    prompt_file = prompt_path_md if os.path.exists(prompt_path_md) else prompt_path_txt
    if not os.path.exists(prompt_file):
        raise SystemExit("No prompt file found (umpf_system_prompt.md or .txt) in prompts/")

    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = os.path.join(outputs_dir, base_name + ".md")

    # Step 1: Extract PDF text
    print("📖 Extracting PDF text...")
    paper_text = extract_pdf_text(pdf_file)

    # Step 2: Load system prompt
    print("⚙️ Loading UMPF system prompt...")
    system_prompt = load_prompt(prompt_file)

    # Step 3: Run UMPF analysis
    print("🤖 Running analysis with ChatCompletion...")
    markdown_output = run_umfp_analysis(system_prompt, paper_text)

    # Step 4: Save result
    os.makedirs(outputs_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"✅ Analysis saved to {output_file}")
