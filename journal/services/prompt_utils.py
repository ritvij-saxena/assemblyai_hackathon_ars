# prompt_utils.py

def create_prompt():
    return (
        "Prompt: You are an empathetic and insightful therapist. Based on the user's journal entry "
        "provided below, summarize the content in 50 words, short_summary, and identify which of the following emotional "
        "categories it falls under: happy, sad, angry, disappointed, or neutral."
        "Do not choose any category outside these options. "
        "Provide your response in JSON format with the three keys: "
        "summary: <summary> short_summary: <short_summary> emotion: <emotion>"
    )
