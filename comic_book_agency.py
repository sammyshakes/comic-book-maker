import os
from dotenv import load_dotenv
from agency_swarm import set_openai_key, Agency
from StoryGeneratorAgent.StoryGeneratorAgent import StoryGeneratorAgent
from CharacterImageGeneratorAgent.CharacterImageGeneratorAgent import CharacterImageGeneratorAgent, GenerateCharacterImageTool
from PanelCreatorAgent.PanelCreatorAgent import PanelCreatorAgent
from utils import load_setup_prompt, create_full_prompt
import json
import logging
import time
import requests
from PIL import Image
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        return True
    return False

def save_metadata(metadata, filename):
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def generate_character_image(character_generator, character_name, character_description):
    character_image_tool = GenerateCharacterImageTool(
        character_name=character_name,
        character_description=character_description
    )
    return character_image_tool.run()

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        set_openai_key(openai_api_key)
    else:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    # Initialize agents
    try:
        story_generator = StoryGeneratorAgent()
        character_generator = CharacterImageGeneratorAgent()
        panel_creator = PanelCreatorAgent()
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")
        return

    # Load the setup prompt
    setup_prompt = load_setup_prompt()

    # User input for the story prompt
    user_input = input("Enter your story prompt: ")

    # Combine setup part and user input to form the complete prompt
    full_prompt = create_full_prompt(setup_prompt, user_input)

    # Generate the story
    story_tool = story_generator.tools[0](prompt=full_prompt)
    story = story_tool.run()
    logger.info("Generated Story:")
    logger.info(story)

    # Identify characters
    identify_characters_tool = story_generator.tools[1](story=story)
    characters = identify_characters_tool.run()
    logger.info("\nIdentified Characters:")
    logger.info(json.dumps(characters, indent=2))

    # Create a directory to save images
    os.makedirs("generated_images", exist_ok=True)

    # Generate images for each character or main element
    character_images = {}
    for name, description in characters.items():
        print(f"Generating image for: {name}")
        image_response = generate_character_image(character_generator, name, description)
        
        if isinstance(image_response, dict) and image_response.get('success') == True:
            generated_task_id = image_response.get('task_id')
            if generated_task_id:
                character_images[name] = generated_task_id
                print(f"Image generation initiated for {name}. Task ID: {generated_task_id}")
            else:
                logger.error(f"Failed to get task_id for {name}. Response: {image_response}")
        else:
            logger.error(f"Failed to initiate image generation for {name}. Response: {image_response}")

    # Check status of tasks and save images
    max_attempts = 30
    for name, stored_task_id in character_images.items():
        character_image_tool = GenerateCharacterImageTool(
            character_name=name,
            character_description=characters[name]
        )
        for attempt in range(max_attempts):
            status_response = character_image_tool.check_task_status(stored_task_id)
            status = status_response.get('status')
            print(f"Status for {name}: {status} (attempt {attempt + 1}/{max_attempts})")
            
            if status == 'finished':
                image_url = status_response['task_result']['image_url']
                filename = f"generated_images/{name.replace(' ', '_')}.png"
                if save_image(image_url, filename):
                    print(f"Image for {name} saved as {filename}")
                    # Save metadata
                    metadata = {
                        "task_id": stored_task_id,
                        "name": name,
                        "prompt": description,
                        "status_response": status_response
                    }
                    metadata_filename = f"generated_images/{name.replace(' ', '_')}_metadata.json"
                    save_metadata(metadata, metadata_filename)
                    print(f"Metadata for {name} saved as {metadata_filename}")
                else:
                    logger.error(f"Failed to save image for {name}")
                break
            elif status in ['failed', 'error']:
                logger.error(f"Image generation for {name} failed: {status_response.get('message', 'Unknown error')}")
                break
            elif status in ['pending', 'processing']:
                print(f"Image for {name} is still processing. Waiting...")
                time.sleep(20)
            else:
                logger.warning(f"Unexpected status for {name}: {status}")
                time.sleep(20)

    logger.info("\nGenerated Images:")
    for name in character_images.keys():
        filename = f"generated_images/{name.replace(' ', '_')}.png"
        if os.path.exists(filename):
            logger.info(f"{name}: {filename}")
        else:
            logger.info(f"{name}: Image generation failed or not completed")

    with open('task_ids.txt', 'w') as f:
        for name, task_id in character_images.items():
            f.write(f"{name}: {task_id}\n")

    print("Task IDs have been saved to task_ids.txt")

if __name__ == "__main__":
    main()
