import os
import argparse 
from dotenv import load_dotenv
from google import genai


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
    args = parser.parse_args()
    # Now we can access `args.user_prompt`


    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=args.user_prompt
        )
    if response.usage_metadata == None:
        raise   RuntimeError("failed Google gemini API request")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
