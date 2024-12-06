import streamlit as st
from datetime import datetime
import calendar
import sounddevice as sd
import os

from app import runner


# Placeholder for your LLM function

def llm_function(file_path):
    # Implement LLM logic here with the file path
    response = runner(file_path)
    st.write(f"Response: {response}")

# Record Audio function
def record_audio():
    st.info("Press 'Start Recording' to record audio. Press 'Stop Recording' to stop.")

    if "recording" not in st.session_state:
        st.session_state["recording"] = False
        st.session_state["audio_data"] = None

    if st.session_state["recording"]:
        stop_button = st.button("Stop Recording")
        if stop_button:
            st.session_state["recording"] = False
            audio_file_path = save_audio(st.session_state["audio_data"])
            st.success(f"Recording stopped and saved as {audio_file_path}")
            st.session_state["audio_data"] = None  # Reset audio data after saving
    else:
        start_button = st.button("Start Recording")
        if start_button:
            st.session_state["recording"] = True
            st.session_state["audio_data"] = start_recording()

def start_recording():
    """Start recording audio."""
    p = sd.PyAudio()
    stream = p.open(format=sd.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
    frames = []
    while st.session_state["recording"]:
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return b"".join(frames)

def upload_audio():
    """Upload an audio file, save it with a timestamp and return the file path."""
    st.info("Click below to upload an audio file from your local storage.")
    audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

    if audio_file:
        # Display success message with file name
        st.success(f"File uploaded: {audio_file.name}")
        # Ensure the 'audio/' directory exists
        if not os.path.exists('audio'):
            os.makedirs('audio')
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Define the file path with the timestamp and .mp3 extension
        temp_audio_path = os.path.join('audio', f'uploaded_audio_{timestamp}.mp3')
        # Save the audio content to the file with .mp3 extension
        with open(temp_audio_path, 'wb') as f:
            f.write(audio_file.read())
        return temp_audio_path

    return None
# Upload Audio function
def save_audio(audio_data):
    """Save recorded audio to a file in the 'audio/' directory with a timestamp and mp3 extension."""
    # Ensure the 'audio/' directory exists
    if not os.path.exists('audio'):
        os.makedirs('audio')

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a file path with the timestamp and mp3 extension
    temp_file_path = os.path.join('audio', f'recorded_audio_{timestamp}.mp3')

    # Save the audio data to the file
    with open(temp_file_path, 'wb') as f:
        f.write(audio_data)

    return temp_file_path
# Submit Audio and Log the Path
def submit_audio(audio_file_path):
    st.info("Submitting the audio file.")
    st.write(f"Audio file submitted: {audio_file_path}")
    llm_function(audio_file_path)  # Pass the file path to your LLM function

# Render Calendar
def render_calendar():
    current_date = datetime.now()
    year, month = current_date.year, current_date.month
    cal = calendar.Calendar()

    st.subheader(f"{calendar.month_name[month]} {year}")

    weeks = cal.monthdayscalendar(year, month)
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].text(" ")
            else:
                if cols[i].button(str(day)):
                    st.session_state["popup_date"] = f"{day}/{month}/{year}"
                    st.session_state["popup_open"] = True

# Main Streamlit App
st.title("Interactive Calendar")

# Session state initialization
if "popup_open" not in st.session_state:
    st.session_state["popup_open"] = False
if "popup_date" not in st.session_state:
    st.session_state["popup_date"] = ""


# Pop-up Dialog
if st.session_state["popup_open"]:
    with st.sidebar:  # Display the dialog as a sidebar
        st.markdown(f"### Dialog for {st.session_state['popup_date']}")
        st.info("Choose one option below:")
        option = st.radio("Select an option:", ["Record Audio", "Upload Audio"])

        if option == "Record Audio":
            record_audio()
        elif option == "Upload Audio":
            uploaded_file_path = upload_audio()

        if st.button("Submit"):
            if st.session_state["audio_data"]:
                audio_file_path = save_audio(st.session_state["audio_data"])
                submit_audio(audio_file_path)
            elif uploaded_file_path:
                submit_audio(uploaded_file_path)

        if st.button("Close"):
            st.session_state["popup_open"] = False

render_calendar()