import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
try:
    api_key = os.environ.get("GEMINI_API_KEY")
except RuntimeError:{"Key GEMINI_API_KEY does not exist  in .env."}


def main():
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents='"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."?'
    )
    if response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError ("Usage metadata not available for this response.")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
