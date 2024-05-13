import os
from pathlib import Path
from openai import OpenAI

# Load the API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def translate_audio_to_text(audio_filename):
    """
    Translates the provided Spanish audio file to English text using OpenAI's Whisper model and saves the output in a text file.
    Also, prints the number of tokens used for input and output.

    Args:
    audio_filename (str): The file name of the audio file to translate.

    Returns:
    str: The path to the output text file containing the translated text, or None if an error occurred.
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
        return None

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
        return None

    # Construct the output file name based on the input file name
    output_file_name = os.path.join(directory_path, f"{audio_filename.split('.')[0]}_translated.txt")

    try:
        # Write the translated text to a new file in the same directory
        with open(output_file_name, "w") as text_file:
            text_file.write(translation.text)
        print(f"Translation completed: {output_file_name}")
        return output_file_name
    except Exception as e:
        print(f"Failed to write to file: {output_file_name}. Error: {e}")
        return None


def text_to_speech(text_file_path):
    """
    Converts text from a given file to speech using OpenAI's Text-to-Speech model and saves it as an MP4 file.

    Args:
    text_file_path (str): Path to the text file containing the text to be converted.

    Returns:
    None: The function streams the audio to the specified file and prints the file path.
    """
    output_audio_path = Path(text_file_path.replace('_translated.txt', '_audio.mp4'))

    # Read the text from the file
    try:
        with open(text_file_path, 'r') as file:
            text_content = file.read()
    except FileNotFoundError:
        print(f"The text file {text_file_path} was not found.")
        return
    except Exception as e:
        print(f"Failed to read the text file: {e}")
        return

    try:
        # Create audio from text
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text_content
        )
        # Stream the audio to the specified file path
        response.stream_to_file(output_audio_path)
        print(f"Audio created successfully and saved to {output_audio_path}")
    except Exception as e:
        print(f"Failed to create audio from text. Error: {e}")

# Example usage
if __name__ == "__main__":
    # Specify the name of your audio file here
    audio_filename = "reading8.m4a"  # Adjust the filename as necessary
    text_file_path = translate_audio_to_text(audio_filename)
    if text_file_path:  # Proceed only if text file was created successfully
        text_to_speech(text_file_path)
