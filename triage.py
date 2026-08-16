import json 
from dotenv import load_dotenv
import anthropic

load_dotenv()
client=anthropic.Anthropic()

TRIAGE_PROMPT = """You are a SOC triage assistant. Analyze the security event and \
respond with ONLY a JSON object (on prose, no markdown fences) with exactly these keys:
- "severity": one of "low", "medium", "high", "critical"
- "verdict": one of "true_positive", "false_positive", "needs_review"
- "suspected_techniques": array of MITRE ATT&CK technique names (strings)
- "reasoning": one short paragraph

Event:
{event}"""

def triage_raw(alert):
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens = 500,
        messages = [
            {
                "role":"user",
                "content":TRIAGE_PROMPT.format(event=json.dumps(alert, indent=2))
            },
            {"role": "assistant", "content": "{"
            } #forces JSON
            ]            
    )
    return "{" + resp.content[0].text

#parser
def parse_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].removeprefix("json").strip()
    return json.loads(raw)

if __name__ == "__main__":
    with open("sample_alerts.json") as f:
        alerts = json.load(f)
    raw = triage_raw(alerts[0])

    print ("RAW: ")
    print (raw)

    result = parse_json(raw)

    print("\nPARSED: ")
    print(result)



