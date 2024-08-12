# CharacterImageGeneratorAgent.py

from agency_swarm.agents import Agent
from .tools.GenerateCharacterImageTool import GenerateCharacterImageTool

class CharacterImageGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CharacterImageGeneratorAgent",
            description="Generates character images for comic books",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[GenerateCharacterImageTool],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        # Add any specific validation logic here if needed
        return message