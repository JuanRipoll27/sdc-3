import time

import cv2
import numpy as np
import config
import streamlit as st
import inference
from PIL import Image
import io

STYLES = config.STYLES

st.title("Style transfer web app")

file = st.file_uploader("Choose an image")

style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

if st.button("Style Transfer") \
    and file is not None and style is not None:
        model = STYLES[style]
        image = np.array(Image.open(file))
        output, resized = inference.inference(model, image)

        res, img = cv2.imencode(".png", output)
        image_bytes = io.BytesIO(img)
        st.image(Image.open(image_bytes))
