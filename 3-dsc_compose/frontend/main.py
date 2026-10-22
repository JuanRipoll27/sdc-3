"""Streamlit frontend for the two-container StyleLab demo."""

import hashlib
import io
import os
from urllib.parse import quote

import requests
import streamlit as st
from PIL import Image, UnidentifiedImageError


BACKEND_URL = os.getenv("APP_BACKEND_URL", "http://localhost:8080").rstrip("/")

st.set_page_config(
    page_title="StyleLab | AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS changes only the visual presentation, not the Streamlit behavior.
st.markdown(
    """
    <style>
    .block-container {max-width: 1150px; padding-top: 2.2rem;}
    .hero {padding: 1.3rem 1.6rem; border-radius: 18px;
           background: linear-gradient(110deg, #152238, #304a68);
           color: #fff; margin-bottom: 1.5rem;}
    .hero h1 {color: white; margin: 0; font-size: 2.5rem;}
    .hero p {color: #dbe9f5; margin: .5rem 0 0 0;}
    .eyebrow {letter-spacing: .15em; text-transform: uppercase;
              font-size: .75rem; color: #9cccf0;}
    .section-label {font-size: 1rem; font-weight: 700; margin-bottom: .6rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Solution Deployment &amp; Communication · Lab 3</div>
      <h1>StyleLab</h1>
      <p>Give your photos a new artistic look using pre-trained neural style models.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def load_styles():
    """Ask FastAPI for styles; return an error message if it is offline."""
    try:
        response = requests.get(BACKEND_URL + "/styles", timeout=5)
        response.raise_for_status()
        styles = response.json()["styles"]
        if not isinstance(styles, list) or not styles:
            raise ValueError("The backend returned no styles")
        return styles, None
    except (requests.RequestException, ValueError, KeyError) as exc:
        return [], str(exc)


styles, backend_error = load_styles()
backend_online = backend_error is None

with st.sidebar:
    st.title("How it works")
    st.write("**1. Frontend:** Streamlit uploads your photo and settings.")
    st.write("**2. Backend:** FastAPI runs the selected OpenCV style model.")
    st.write("**3. Result:** The backend sends a PNG back to Streamlit.")
    st.divider()
    if backend_online:
        st.success("Backend connected")
    else:
        st.error("Backend unavailable")
        st.caption(backend_error)
    st.caption("Docker Compose connects both services on an internal network.")
    st.code("docker compose up -d --build", language="bash")
    st.markdown("[FastAPI interactive docs](http://localhost:8080/docs)")

st.subheader("Create your artwork")
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-label">01 · Upload a photo</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose a JPG or PNG", type=["jpg", "jpeg", "png"]
    )

with right:
    st.markdown('<div class="section-label">02 · Choose a style</div>', unsafe_allow_html=True)
    selected_style = st.selectbox(
        "Artistic model",
        options=styles,
        format_func=lambda name: name.replace("_", " ").title(),
        disabled=not backend_online,
    )
    strength_percent = st.slider(
        "Style intensity",
        min_value=0,
        max_value=100,
        value=85,
        step=5,
        help="0% preserves the original; 100% uses the full artistic transformation.",
    )
    st.caption("The intensity blends the original photo with the model output.")
    generate = st.button(
        "Generate artwork",
        type="primary",
        disabled=uploaded is None or not backend_online,
    )

# Save the generated PNG between Streamlit reruns.
if "result_png" not in st.session_state:
    st.session_state["result_png"] = None

input_bytes = uploaded.getvalue() if uploaded is not None else None
input_id = hashlib.sha256(input_bytes).hexdigest() if input_bytes else None
if st.session_state.get("input_id") != input_id:
    st.session_state["input_id"] = input_id
    st.session_state["result_png"] = None

original_preview = None
if input_bytes:
    try:
        original_preview = Image.open(io.BytesIO(input_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("The selected file is not a valid image.")

if generate and original_preview is not None:
    try:
        with st.spinner("Applying the artistic style..."):
            response = requests.post(
                BACKEND_URL + "/" + quote(selected_style, safe=""),
                files={
                    "file": (
                        uploaded.name,
                        input_bytes,
                        uploaded.type or "application/octet-stream",
                    )
                },
                data={"strength": str(strength_percent / 100.0)},
                timeout=180,
            )
            response.raise_for_status()
            # Verify that the API returned an actual image.
            Image.open(io.BytesIO(response.content)).verify()
            st.session_state["result_png"] = response.content
            st.session_state["last_settings"] = (
                selected_style.replace("_", " ").title(),
                strength_percent,
            )
    except (requests.RequestException, UnidentifiedImageError, OSError) as exc:
        st.error("Could not generate the image: {}".format(exc))

st.divider()
st.subheader("Compare results")
original_col, output_col = st.columns(2, gap="large")

with original_col:
    st.markdown("**Original**")
    if original_preview is not None:
        st.image(original_preview, use_container_width=True)
    else:
        st.info("Upload a photo to see the original here.")

with output_col:
    st.markdown("**Stylized**")
    if st.session_state["result_png"]:
        st.image(st.session_state["result_png"], use_container_width=True)
        style_name, last_strength = st.session_state["last_settings"]
        st.caption("{} · {}% intensity".format(style_name, last_strength))
        st.download_button(
            "Download PNG",
            data=st.session_state["result_png"],
            file_name="stylelab-result.png",
            mime="image/png",
        )
    else:
        st.info("Click Generate artwork to see your result here.")

st.caption("StyleLab · Streamlit frontend → FastAPI backend → OpenCV neural style transfer")
