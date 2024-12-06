import assemblyai as aai
import os

class AssemblyAIProcessor:
    def __init__(self, api_key_env_var="API_KEY_2"):
        self.api_key = os.getenv(api_key_env_var)
        self.transcript = None
        if not self.api_key:
            raise ValueError("API key is missing. Please provide it in the environment variables.")
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()

    def transcribe_audio(self, audio_file_path):
        """Transcribe an audio file and return the transcript."""
        try:
            transcript = self.transcriber.transcribe(audio_file_path)
            if not transcript:
                raise ValueError("No transcript received")
            return transcript
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def suggested_actions_for_emotion(self, short_summary, emotions, prompt):
        prompt = prompt + f"the user has following emotions={emotions} and short_summary for their feelings={short_summary}"
        try:
            result = self.transcript.lemur.task(prompt, final_model=aai.LemurModel.claude3_5_sonnet)
            return result.response
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def generate_emotional_summary(self, transcript, prompt):
        """Generate emotional summary based on the transcript and prompt."""
        try:
            self.transcript = transcript
            result = transcript.lemur.task(prompt, final_model=aai.LemurModel.claude3_5_sonnet)
            return result.response
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
