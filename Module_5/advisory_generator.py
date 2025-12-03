"""
advisory_generator.py — works with openai>=1.0.0

Run:
    source venv/bin/activate
    export OPENAI_API_KEY="your_key"
    python advisory_generator.py
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta
from openai import OpenAI   # NEW client interface

# --------------------------------
# CONFIG
# --------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set. Run: export OPENAI_API_KEY=\"your_key\"")

MODEL = "gpt-4o-mini"  # set the model you have access to

PROMPT_TEMPLATE_FILE = "prompt_template.txt"
SCENARIO_FILE = "scenario_config.json"


# --------------------------------
# HELPERS
# --------------------------------
def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, scenario: dict) -> str:
    """
    Replace only known placeholders — prevents JSON braces errors
    """
    mapping = {
        "total_area_acres": scenario.get("total_area_acres", 200),
        "plots_total": scenario.get("plots_total", 50),
        "water_cut_pct": scenario.get("water_cut_pct", 30),
        "drones_available": scenario.get("drones_available", 2),
        "agv_available": scenario.get("agv_available", 1),
        "battery_minutes": scenario.get("battery_minutes", 22),
        "risk_plots": scenario.get("risk_plots", []),
        "weather_brief": scenario.get("weather_brief", "")
    }

    out = template
    out = out.replace("{risk_plots}", str(mapping["risk_plots"]))

    for key in ("total_area_acres", "plots_total", "water_cut_pct",
                "drones_available", "agv_available", "battery_minutes", "weather_brief"):
        out = out.replace("{" + key + "}", str(mapping[key]))

    return out


def call_llm(prompt: str) -> str:
    """
    Robust extractor for the new OpenAI client chat completions response shape.
    Returns the assistant text (string). Tries several common access patterns.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes clear, practical farmer advisories."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=900,
        temperature=0.1
    )

    # response.choices[0] may have different shapes depending on client version.
    choice = response.choices[0]

    # Try common access patterns in order
    # 1) choice.message.content  (object with attribute)
    try:
        return choice.message.content
    except Exception:
        pass

    # 2) choice.message["content"] (mapping-like)
    try:
        return choice.message["content"]
    except Exception:
        pass

    # 3) choice.text (older style)
    try:
        return choice.text
    except Exception:
        pass

    # 4) as a last resort, stringify the whole choice
    return str(choice)

def extract_json(text: str):
    """
    Try to extract the first JSON object from model output.
    """
    fence = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", text)
    if fence:
        raw = fence.group(1)
        try:
            return json.loads(raw)
        except:
            pass

    match = re.search(r"({[\s\S]*})", text)
    if match:
        raw = match.group(1)
        try:
            return json.loads(raw)
        except:
            pass

    return None


# --------------------------------
# MAIN
# --------------------------------
def main():
    template = load_file(PROMPT_TEMPLATE_FILE)
    scenario = json.loads(load_file(SCENARIO_FILE))

    prompt = build_prompt(template, scenario)

    print("Calling LLM — please wait...")
    advisory_text = call_llm(prompt)

    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    ts = now.strftime("%Y%m%dT%H%M%S%z")

    txt_file = f"advisory_{ts}.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(advisory_text)

    print(f"Saved text advisory to {txt_file}")

    parsed = extract_json(advisory_text)
    if parsed:
        json_file = f"advisory_{ts}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print(f"Saved parsed JSON to {json_file}")
    else:
        print("Warning: No JSON block found in model output.")

    print("\n--- Preview ---\n")
    print(advisory_text[:1200])
    print("\n--- End Preview ---")


if __name__ == "__main__":
    main()
