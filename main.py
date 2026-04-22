import os
import argparse 
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from prompts import system_prompt
from call_function import available_functions, call_function


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

    for _ in range(20):

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=system_prompt,
                        temperature=0,
                    ),
                )
                break  # success, exit the retry loop
            except errors.ServerError as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2 ** attempt)  # 1s, 2s, 4s — exponential backoff
        else:
            # all 3 attempts failed
            print("Gemini API is unavailable. Try again later.")
            sys.exit(1)

        if response.usage_metadata == None:
            raise   RuntimeError("failed Google gemini API request")
        for candidate in response.candidates: #or types.generateContent.candidates?
            messages.append(candidate.content)
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if not response.function_calls:
            print(response.text)
            break
        else:
            function_result = []
            for call in response.function_calls:
                #print(f"Calling function: {call.name}({call.args})")
                function_call_result = call_function(call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Return object of function_call is empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception("First item is not a FunctionResponse")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function response is None")
                function_result.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_result))
    else:
        exit(1)

if __name__ == "__main__":
    main()