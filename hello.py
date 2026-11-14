from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()        # reads .env and makes the key available
client = OpenAI()    # creates the connection; finds the key automatically

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello in five words."}],
)

print(response.choices[0].message.content)