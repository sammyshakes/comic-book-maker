import requests
from agency_swarm.tools import BaseTool
from pydantic import Field
import json

class GenerateCharacterImageTool(BaseTool):
    character_name: str = Field(..., description="The name of the character")
    character_description: str = Field(..., description="The description of the character")

    def run(self):
        api_key = "37e209ef799f547d4363ac2a190ef723eff260f8353c3ef9c1ffb2021a75fa43"  # Replace with your actual API key
        endpoint = "https://api.midjourneyapi.xyz/mj/v2/imagine"
        headers = {
            "X-API-KEY": api_key
        }
        
        # Simplify the prompt to its bare essentials
        prompt = f"{self.character_name}, comic book character, portrait"
        
        data = {
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "process_mode": "relax"
        }

        try:
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_info = {
                "error": str(e),
                "status_code": response.status_code if 'response' in locals() else None,
                "response_text": response.text if 'response' in locals() else None
            }
            try:
                error_info["json_response"] = response.json() if 'response' in locals() else None
            except json.JSONDecodeError:
                error_info["json_response"] = None
            return error_info
        
    def check_task_status(self, task_id: str):
        endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"
        headers = {
            "X-API-KEY": "37e209ef799f547d4363ac2a190ef723eff260f8353c3ef9c1ffb2021a75fa43"
        }
        data = {
            "task_id": task_id
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            # Add detailed logging
            # print(f"Task status response for task_id {task_id}: {response_data}")
            return response_data
        except requests.RequestException as e:
            error_info = {
                "error": str(e),
                "status_code": response.status_code if 'response' in locals() else None,
                "response_text": response.text if 'response' in locals() else None
            }
            print(f"Task status error for task_id {task_id}: {error_info}")
            return error_info
