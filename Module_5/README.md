# Farmer Advisory Generator

Files:
- advisory_generator.py  -> main script
- prompt_template.txt    -> prompt template
- scenario_config.json   -> scenario values (edit to simulate cases)
- requirements.txt       -> python deps

Setup:
1. Create a virtual environment (recommended).

2. Install dependencies:
   `` pip install -r requirements.txt``

3. Set your OpenAI API key in environment variable:
<br>
   Linux/Mac:
    ``       export OPENAI_API_KEY="sk-..." ``
    <br>
   Windows PowerShell:
    `` $env:OPENAI_API_KEY="sk-..." ``

4. Run:
   `` python advisory_generator.py ``

Output:
- A timestamped text file `advisory_YYYYMMDDTHHMMSS+0530.txt` will be created with the advisory.
![alt text](<Screenshot from 2025-12-03 19-33-13.png>)