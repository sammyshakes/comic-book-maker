def load_setup_prompt(file_path='setup_prompt.txt'):
    with open(file_path, 'r') as file:
        return file.read()

def create_full_prompt(setup_prompt, user_input):
    return f"{setup_prompt}\n\nNow, create a story based on this prompt: {user_input}"

def get_user_feedback():
    likes = input("What did you like about the story? ")
    dislikes = input("What did you dislike about the story? ")
    return likes, dislikes

def get_user_edits():
    edit_prompt = "What would you like to edit in the story? Please specify the section and the new content: "
    edits = input(edit_prompt)
    return edits
