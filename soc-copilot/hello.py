from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()


resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=[{"role":"user", "content":"In one sentence, what is SOC?"}],
)
print(resp.content[0].text)