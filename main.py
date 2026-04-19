import os
import argparse 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("no Gemini API key found")
client = genai.Client(api_key=api_key)
model = 'gemini-2.5-flash'

contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def main():
#catch user prompt from console
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Please insert user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
# Now we can access `args.user_prompt`

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,temperature=0)
    )
    
    if response.usage_metadata == None:
        raise   RuntimeError("failed Google gemini API request")
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls == None:
        print(response.text)
    else:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")

if __name__ == "__main__":
    main()