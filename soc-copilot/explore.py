import json

with open("sample_alerts.json") as f:
    alerts = json.load(f)
print(f"Loaded {len(alerts)} alerts")
for a in alerts:
    print(a["event_id"], "-", a["description"], "-", a["account"])
    