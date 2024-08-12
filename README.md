
# Comic Book Character Image Generation

This project allows you to generate images for comic book characters using a set of agents and tools. The generated images and their corresponding metadata are saved locally.

## Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)
- `virtualenv` (optional but recommended)
- OpenAI API key
- GoAPI MidJourney API key

## Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -U agency-swarm
   pip install requests pillow python-dotenv
   ```

4. **Create a `.env` file** in the root directory of the project and add your OpenAI API and Midjourney key:
   ```ini
   OPENAI_API_KEY=your_openai_api_key_here
   MIDJOURNEY_API_KEY=your_goapi_midjourney_key_here
   ```


## Usage

### Generating Comic Book Character Images

1. **Run the main script to generate character images**:
   ```bash
   python comic_book_agency.py
   ```

   - You will be prompted to enter your story prompt.
   - The script will generate a story, identify characters, and initiate image generation for each character.
   - The images and their metadata will be saved in the `generated_images` directory.

### Checking Task Status and Saving Images

1. **Run the status checking script**:
   ```bash
   python check_status.py
   ```

   - This script reads task IDs from `task_ids.txt` and checks their status.
   - If the task is finished, the script saves the image and metadata to the `generated_images` directory.

## Script Details

### `comic_book_agency.py`

- **Purpose**: Generates comic book character images based on a story prompt.
- **Functionality**:
  - Initializes agents for story generation, character image generation, and panel creation.
  - Generates a story from the user's prompt.
  - Identifies characters from the story.
  - Initiates image generation for each character.
  - Saves generated images and their metadata.

### `check_status.py`

- **Purpose**: Checks the status of image generation tasks and saves completed images and their metadata.
- **Functionality**:
  - Reads task IDs from `task_ids.txt`.
  - Checks the status of each task.
  - Saves the image and metadata if the task is finished.

### Utility Functions

- **`save_image(url, filename)`**: Downloads and saves an image from a URL.
- **`save_metadata(metadata, filename)`**: Saves metadata to a JSON file.

## Directory Structure

```
.
├── comic_book_agency.py        # Main script to generate character images
├── check_status.py             # Script to check task status and save images
├── requirements.txt            # List of required Python packages
├── generated_images/           # Directory where generated images and metadata are saved
└── .env                        # Environment file containing API keys
```

## Example

1. **Running `comic_book_agency.py`**:
   ```
   Enter your story prompt: A superhero named Titan fights against the evil Dr. Chaos in a futuristic city.
   Generating image for: Titan
   Image generation initiated for Titan. Task ID: abcdef123456
   Generating image for: Dr. Chaos
   Image generation initiated for Dr. Chaos. Task ID: ghijkl789012
   ```

2. **Running `check_status.py`**:
   ```
   Checking status for Titan:
   Status for Titan: processing (attempt 1/5)
   Status for Titan: finished (attempt 2/5)
   Image for Titan saved as generated_images/Titan.png
   Metadata for Titan saved as generated_images/Titan_metadata.json
   
   Checking status for Dr. Chaos:
   Status for Dr. Chaos: finished (attempt 1/5)
   Image for Dr. Chaos saved as generated_images/Dr_Chaos.png
   Metadata for Dr. Chaos saved as generated_images/Dr_Chaos_metadata.json
   ```

