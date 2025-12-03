# Farmer Advisory Generator

Files:
- advisory_generator.py  -> main script
- prompt_template.txt    -> prompt template
- scenario_config.json   -> scenario values (edit to simulate cases)
- requirements.txt       -> python deps

Setup:
1. Create a virtual environment (recommended).
2. Install dependencies:
   pip install -r requirements.txt

3. Set your OpenAI API key in environment variable:
   Linux/Mac:
     export OPENAI_API_KEY="sk-..."
   Windows PowerShell:
     $env:OPENAI_API_KEY="sk-..."

4. Run:
   python advisory_generator.py

Output:
- A timestamped text file `advisory_YYYYMMDDTHHMMSS+0530.txt` will be created with the advisory.

Notes:
- Change MODEL in `advisory_generator.py` to match your available model.
- Do NOT hardcode the API key in code for security.
