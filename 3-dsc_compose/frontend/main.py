import time

import requests
import streamlit as st
from PIL import Image
import io
import os

STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}

env_backend_url = os.environ['APP_BACKEND_URL']

st.title("Style transfer web app")

image = st.file_uploader("Choose an image")

style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

if st.button("Style Transfer"):
    if image is not None and style is not None:
        files = {"file": image.getvalue()}
        response = requests.post(f"{env_backend_url}/{style}", files=files)
        image_bytes = io.BytesIO(response.content)
        img = Image.open(image_bytes)
        st.image(img)