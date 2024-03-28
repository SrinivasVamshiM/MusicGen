import streamlit as st
import replicate

st.set_page_config(
    page_title="Music Generation",
    page_icon='🎵',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Music Generation Tool")

input_prompt = st.text_input("Describe the music you want to generate")

# Allow user to set the duration limit
duration_limit = st.slider("Set duration limit (seconds)", min_value=8, max_value=30, value=20)

# Allow user to select model version
model_version = st.selectbox("Select model version",
                             options=["stereo-melody-large", "stereo-large", "melody-large", "large"],
                             index=1)

# Allow user to upload a music file
uploaded_file = st.file_uploader("Upload a music file (WAV or MP3) to extract melody", type=["wav", "mp3"])

# Enable continuation option only if a song is uploaded
if uploaded_file:
    continuation_option = st.radio("Enable continuation?", ("True", "False"), index=1)
    continuation = (continuation_option == "True")
else:
    continuation = False

submit = st.button("Generate Music")

if submit:
    # Check if the prompt length is appropriate
    if len(input_prompt) > duration_limit * 4:
        st.error("Prompt is too long for the selected duration limit. Please provide a shorter prompt.")
    else:
        # Generate music
        if uploaded_file:
            output = replicate.run(
                "meta/musicgen:b05b1dff1d8c6dc63d14b0cdb42135378dcb87f6373b0d3d341ede46e59e2b38",
                input={
                    "top_k": 250,
                    "top_p": 0,
                    "prompt": input_prompt,
                    "input_audio": uploaded_file,
                    "duration": duration_limit,
                    "temperature": 1,
                    "continuation": continuation,
                    "model_version": model_version,
                    "output_format": "wav",
                    "continuation_start": 0,
                    "multi_band_diffusion": False,
                    "normalization_strategy": "peak",
                    "classifier_free_guidance": 3
                }
            )
        else:
            output = replicate.run(
                "meta/musicgen:b05b1dff1d8c6dc63d14b0cdb42135378dcb87f6373b0d3d341ede46e59e2b38",
                input={
                    "top_k": 250,
                    "top_p": 0,
                    "prompt": input_prompt,
                    "duration": duration_limit,
                    "temperature": 1,
                    "continuation": continuation,
                    "model_version": model_version,
                    "output_format": "wav",
                    "continuation_start": 0,
                    "multi_band_diffusion": False,
                    "normalization_strategy": "peak",
                    "classifier_free_guidance": 3
                }
            )

        st.audio(output, format='audio/wav')