# Python In-built packages
import streamlit as st
from pathlib import Path
import PIL
import subprocess
import numpy as np
import datetime
import os

from twilio.rest import Client

# Local Modules
import settings
import helper
import time

output_file = "detection_results.txt"

def run_script_in_new_command_prompt(script_name):
    # Get the current directory
    current_dir = os.getcwd()
    # Open a new command prompt in the same directory
    subprocess.Popen('start cmd /K cd /d "{}"'.format(current_dir), shell=True)
    # Run the Python script in the new command prompt
    subprocess.Popen('start cmd /K python "{}"'.format(script_name), shell=True)

def save_predictions(predictions, output_file):
    # Convert predictions tensor to a NumPy array
    now = datetime.datetime.now()
    current_time = now.strftime("%B %d, %Y %H:%M:%S")
    print(current_time)
    predictions_array = predictions.detach().cpu().numpy()

    # Reshape the array if needed
    if predictions_array.ndim < 2:
        predictions_array = np.expand_dims(predictions_array, axis=0)

    # Append the predictions array to the text file
    with open(output_file, 'a') as file:
        if predictions_array==0:
            file.write('Elephant detected at\t'+current_time+'\n')
            run_script_in_new_command_prompt('elephant_alert.py')
            
        else:
            file.write('Tiger detected at\t\t'+current_time+'\n')
            run_script_in_new_command_prompt('tiger_alert.py')
            

# Setting page layout
st.set_page_config(
    page_title="AIDS",
    page_icon="🐅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Animal Intrusion Detection System")

# Sidebar
st.sidebar.header("Choose Model Configuration")

# Model Options
model_type = 'Detection'

confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                
                for box in boxes:
                    save_predictions(box.data[0][5], output_file)

                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

else:
    st.error("Please select a valid source type!")
