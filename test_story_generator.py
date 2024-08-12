import os
from dotenv import load_dotenv
from agency_swarm import set_openai_key
from StoryGeneratorAgent import StoryGeneratorAgent
from utils import load_setup_prompt, create_full_prompt

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        set_openai_key(openai_api_key)
    else:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    agent = StoryGeneratorAgent()
    
    # Load the setup prompt
    setup_prompt = load_setup_prompt()

    # User input for the story prompt
    user_input = input("Enter your story prompt: ")

    # Combine setup part and user input to form the complete prompt
    full_prompt = create_full_prompt(setup_prompt, user_input)

    # Instantiate the tool with the complete prompt
    tool = agent.tools[0](prompt=full_prompt)

    # Run the tool and print the result
    result = tool.run()
    print(result)

if __name__ == "__main__":
    main()
