import os
from openai import OpenAI
from pathlib import Path

# Load the API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def translate_audio_to_text(audio_filename):
    """
    Translates the provided Spanish audio file to English text using OpenAI's Whisper model.

    Args:
    audio_filename (str): The file name of the audio file to translate.
    
    Returns:
    None: Outputs the translated text to a file in the same directory.
    """
    directory_path = "/Users/jam/S2T"  # Define the directory path explicitly
    file_path = os.path.join(directory_path, audio_filename)  # Construct the file path using os.path.join for better compatibility

    # Check if the directory exists, create if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        # Open the audio file in read-binary mode
        with open(file_path, "rb") as audio_file:
            # Call the Whisper API to translate the audio to English
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
    except Exception as e:
        print(f"Failed to process the audio file: {e}")
        return

    # Construct the output file name based on the input file name
    output_file_name = os.path.join(directory_path, f"{audio_filename.split('.')[0]}_translated.txt")

    try:
        # Write the translated text to a new file in the same directory
        with open(output_file_name, "w") as text_file:
            text_file.write(translation.text)
        print(f"Translation completed: {output_file_name}")
    except Exception as e:
        print(f"Failed to write to file: {output_file_name}. Error: {e}")

# Example usage
if __name__ == "__main__":
    # Specify the name of your audio file here
    audio_filename = "reading6.m4a"  # Make sure to replace 'reading1.mp4' with your actual audio file name
    translate_audio_to_text(audio_filename)
