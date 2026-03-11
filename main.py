import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,
    temperature=0
    ),
    )
    if response.function_calls:
        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)
            if not result.parts:
                raise RuntimeError("Empty parts")
            if result.parts[0].function_response is None:
                raise RuntimeError("No function response")
            if result.parts[0].function_response.response is None:
                raise RuntimeError("No response data")
            function_responses.append(result.parts[0])
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")

    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
