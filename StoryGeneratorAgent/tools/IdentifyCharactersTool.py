# IdentifyCharactersTool.py

from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from openai import OpenAI

class IdentifyCharactersTool(BaseTool):
    story: str = Field(..., description="The generated story")

    def run(self):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant that identifies main characters in a story and provides detailed visual descriptions for each."},
                {"role": "user", "content": f"Identify the main characters in the following story and provide a detailed visual description for each, including their appearance, clothing, and any notable features. Format the output as a JSON object where each key is a character's name and the value is their description. If there are no distinct characters, create a description for the main elements or concepts in the story.\n\nStory:\n{self.story}"}
            ]
        )
        
        content = response.choices[0].message.content
        
        try:
            characters = json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, attempt to create a structured output manually
            characters = self.parse_non_json_response(content)
        
        return characters

    def parse_non_json_response(self, content):
        characters = {}
        lines = content.split('\n')
        current_character = None
        current_description = []

        for line in lines:
            if ':' in line and not current_character:
                parts = line.split(':', 1)
                current_character = parts[0].strip()
                current_description = [parts[1].strip()]
            elif current_character:
                if line.strip():
                    current_description.append(line.strip())
                else:
                    characters[current_character] = ' '.join(current_description)
                    current_character = None
                    current_description = []

        if current_character:
            characters[current_character] = ' '.join(current_description)

        return characters