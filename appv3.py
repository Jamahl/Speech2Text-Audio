import os
from pathlib import Path
from openai import OpenAI

# Hardcoded OpenAI API key (for local/dev use only)
api_key = "insert key"
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
    directory_path = "input"  # Updated to use the input folder in the project directory
    file_path = os.path.join(directory_path, audio_filename)  # Construct the file path using os.path.join for better compatibility

    print(f"[DEBUG] Looking for audio file at: {file_path}")

    # Check if the directory exists, create if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"[ERROR] File does not exist: {file_path}")
        return None

    try:
        # Open the audio file in read-binary mode
        with open(file_path, "rb") as audio_file:
            print(f"[DEBUG] File opened successfully: {file_path}")
            # Call the Whisper API to translate the audio to English
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            print(f"[DEBUG] Whisper translation API call successful.")
    except Exception as e:
        print(f"[ERROR] Failed to process the audio file: {e}")
        return None

    # Construct the output file name based on the input file name
    output_file_name = os.path.join(directory_path, f"{audio_filename.split('.')[0]}_translated.txt")

    try:
        # Write the translated text to a new file in the same directory
        with open(output_file_name, "w") as text_file:
            # translation is a string when response_format='text'
            text_file.write(translation)
        print(f"[DEBUG] Translation completed: {output_file_name}")
        return output_file_name
    except Exception as e:
        print(f"[ERROR] Failed to write to file: {output_file_name}. Error: {e}")
        return None


if __name__ == "__main__":
    # Call the function with your specific file
    audio_filename = "WhatsApp Audio 2025-06-20 at 15.38.21.mp3"
    result = translate_audio_to_text(audio_filename)
    print(f"Translation output saved to: {result}")
