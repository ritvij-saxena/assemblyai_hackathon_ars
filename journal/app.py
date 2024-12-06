# app.py

from dotenv import load_dotenv
from services.assembly_ai import AssemblyAIProcessor
from services.prompt_utils import create_prompt, suggestion_prompt
from utils.text_to_json import convert_text_to_json

# Load environment variables from .env file
load_dotenv()

processor = AssemblyAIProcessor()
def runner(audio_file_path = ""):
    """Main runner function that handles the transcription and emotional summary."""

    # Transcribe the audio
    transcript = processor.transcribe_audio(audio_file_path)
    if not transcript:
        print("Error: Could not transcribe the audio.")
        return

    # Create the prompt
    prompt = create_prompt()

    # Generate emotional summary
    result = processor.generate_emotional_summary(transcript, prompt)
    json_data = None
    if result:
        json_data = convert_text_to_json(result)
        print(json_data)
    return json_data if json_data else None

def runner_suggested_actions(llm_response):

    prompt = suggestion_prompt()
    result = processor.suggested_actions_for_emotion(short_summary=llm_response['short_summary'], emotions=llm_response['emotion'], prompt=prompt)
    json_data = None
    if result:
        json_data = convert_text_to_json(result)
        print(json_data)
    return json_data if json_data else None

if __name__ == "__main__":
    runner()
