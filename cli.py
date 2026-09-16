import argparse, json
from triage import triage

parser = argparse.ArgumentParser(description = "Triage security alerts.")
parser.add_argument("alert_file", help="Path to a JSON file of alerts")
args = parser.parse_args()

with open(args.alert_file) as f:
    alerts = json.load(f)

for a in alerts:
    result = triage(a)
    print(result.model_dump_json(indent=2))
