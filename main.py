import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
try:
    api_key = os.environ.get("GEMINI_API_KEY")
except RuntimeError:{"Key GEMINI_API_KEY does not exist  in .env."}


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
    )
    if args.verbose == True:
        if response.usage_metadata:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Response: {response.text}")
        else:
            raise RuntimeError ("Usage metadata not available for this response.")

    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
