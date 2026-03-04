import os
import requests
from anthropic import Anthropic

# 1. Fetch Bloomberg headlines via NewsAPI
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
url = f"https://newsapi.org/v2/everything?domains=bloomberg.com&apiKey={NEWS_API_KEY}"
news_data = requests.get(url).json()

articles = news_data.get("articles", [])[:5]
if not articles:
    raise ValueError(f"No articles returned. API response: {news_data}")

# 2. Feed to Claude
client = Anthropic()  # reads ANTHROPIC_API_KEY from environment
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"Analyze these recent Bloomberg headlines:\n\n{articles}",
        }
    ],
)

print(response.content[0].text)
