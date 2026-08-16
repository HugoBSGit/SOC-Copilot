# asks claude to summarize the alert

import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

def load_alerts(path):
    with open(path) as f:
        return json.load(f)

def summarize(alert):
    prompt = f"""You are a SOC analyst assistant.
    Summarize this security event in 2 sentences for a tier-1 analyst.

Event:
{json.dumps(alert, indent=2)}"""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role":"user", "content": prompt}],
    )
    return rep.content[0].text

if __name__ = "__main__":
    for a in load_alerts("sample_alerts.json"):
    print(summarize(a))
    print("-" * 40)