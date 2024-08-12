# StoryGeneratorAgent.py

from agency_swarm.agents import Agent
from .tools.GenerateStoryTool import GenerateStoryTool
from .tools.IdentifyCharactersTool import IdentifyCharactersTool

class StoryGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="StoryGeneratorAgent",
            description="Generates comic book stories and identifies characters",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[GenerateStoryTool, IdentifyCharactersTool],
            tools_folder="./tools",
            temperature=0.7,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        if "Error generating story:" in message:
            raise ValueError(message)
        return message