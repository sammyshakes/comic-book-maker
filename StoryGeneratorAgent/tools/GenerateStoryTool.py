from openai import OpenAI
from agency_swarm.tools import BaseTool
from pydantic import Field

class GenerateStoryTool(BaseTool):
    prompt: str = Field(..., description="The prompt for generating the story")

    def run(self):
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use the appropriate model name
                messages=[{"role": "user", "content": self.prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating story: {str(e)}"
