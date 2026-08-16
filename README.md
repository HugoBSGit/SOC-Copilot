git add .
git commit -m "Week 1: setup + log summarizer"
# create an empty repo on github.com, then:
git remote add origin https://github.com/HugoBSGit/soc-copilot.git
git branch -M main
git push -u origin main


Project Checklist
- ✅Foundations and setup
    - ✅ Project scafold (project venv, git)
    - ✅ First API call (beginning-API-Call.py)
    - ✅ Sample data (sample_alerts.json + explore.py)
    - ✅ Summary from log (summarize.py)
    - ✅ Clean-up, README (First README.md)
- ☐ Triage Engine
    - ✅ Triage Prompt (triage.py)
    - ✅ JSON Parsing (added parse_json definition + prefill in triage.py)
    - ☐ Validate with Pydantic
    - ☐ Accuracy boost via more exmaples and prompt iteration
    - ☐ Wrap up in CLI