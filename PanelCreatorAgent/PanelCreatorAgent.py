from agency_swarm.agents import Agent
from .tools.CreatePanelTool import CreatePanelTool

class PanelCreatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PanelCreatorAgent",
            description="Creates comic book panels using generated story and images",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CreatePanelTool],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message