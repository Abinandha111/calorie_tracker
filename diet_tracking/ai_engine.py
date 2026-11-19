import os 

from google import genai

google_api_key = os.getenv("gemini_api_key")

client = genai.Client(api_key=google_api_key)


prompt = "explain python in few words"

response = client.models.generate_content(

    model="gemini-2.5-flash",
    contents=[prompt]
)

print(response.text)