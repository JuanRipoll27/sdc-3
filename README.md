# SDC Lab 3 — StyleLab AI Image Studio

A small Docker learning project for **Solution Deployment and Communication (FH Technikum Wien)**.

This repository preserves the three original lab exercises and adds **StyleLab**, a personalized demo in `3-dsc_compose`.

## What changed from the course starter

- A clearer **Streamlit** interface with before/after images and a PNG download.
- A **style intensity** slider (0–100%).
- **FastAPI** now exposes `GET /health` and `GET /styles`, in addition to image processing.
- The frontend retrieves the style list directly from FastAPI.
- `docker-compose.yml` launches both containers on a shared network.
- Explicit frontend dependencies and a Windows PowerShell model setup script.

The AI models and original inference method were provided by the course. StyleLab does **not train** a new model. It blends the original photo and the pre-trained model's output.

## Architecture

```text
Browser
  |
  | http://localhost:8501
  v
Streamlit (frontend container)
  |
  | POST http://backend:80/{style} + file + strength
  | GET  http://backend:80/styles
  v
FastAPI (backend container)
  |
  v
OpenCV + pre-trained .t7 models
  |
  +-- returns image/png to Streamlit
```

Docker Compose creates the internal network automatically. The host uses port **8501** for Streamlit and **8080** for FastAPI.

## Requirements

- Docker Desktop running (WSL2 on Windows).
- PowerShell for the included Windows model download helper.
- Internet access on first installation if the models were not downloaded earlier.

## Quick start (Windows PowerShell)

Open a terminal at the **repository root**.

**1. Obtain the original course models** (the approximately 200 MB of model files are intentionally not tracked in Git):

```powershell
powershell -ExecutionPolicy Bypass -File .\3-dsc_compose\download_models.ps1
```

The script reuses `2-dsc_streamlit/streamlit/models` if available; otherwise it downloads the files from the Stanford fast-neural-style model collection.

**2. Build and start both services:**

```powershell
cd .\3-dsc_compose
docker compose up -d --build
docker compose ps
```

**3. Open the apps:**

- Streamlit: http://localhost:8501
- FastAPI Swagger UI: http://localhost:8080/docs
- Health check: http://localhost:8080/health

**4. Use StyleLab:** upload a JPG/PNG, choose a style, set intensity, click **Generate artwork**, and download the result.

**5. See the logs and stop both services:**

```powershell
docker compose logs -f
# Press Ctrl+C to stop following logs (containers stay running).
docker compose down
```

## API reference

| Method | Path | Returns |
| --- | --- | --- |
| GET | `/` | Welcome message |
| GET | `/health` | Service status JSON |
| GET | `/styles` | List of supported styles |
| POST | `/{style}` | Generated PNG image |

The POST request uses `multipart/form-data` with:
- `file`: JPG/PNG upload (required)
- `strength`: decimal from `0.0` to `1.0` (optional; default `1.0`)

At strength `0`, the output is the resized original; at `1` it is the fully stylized output. Intermediate values use `cv2.addWeighted` to blend the two. Example: `0.85` = 85% stylized image and 15% original.

**Test the API from PowerShell:**

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/styles
```

For a manual POST upload, use the interactive Swagger UI: choose a style endpoint, click **Try it out**, add a file and intensity, then **Execute**.

## Files worth explaining in class

- `3-dsc_compose/frontend/main.py` — interface, upload, HTTP call, preview and PNG download.
- `3-dsc_compose/backend/main.py` — API endpoints, OpenCV conversion, model call and blending.
- `3-dsc_compose/backend/inference.py` — original course inference with pre-trained models.
- `3-dsc_compose/backend/config.py` — maps displayed style names to `.t7` files.
- `3-dsc_compose/docker-compose.yml` — builds the services, maps host ports and connects the internal network.

## Five-minute live demo

1. Explain why the frontend and backend are separate containers.
2. Run `docker compose up -d --build` and `docker compose ps`.
3. Check `/health` and `/styles` in Swagger.
4. Upload a photo in Streamlit and generate two intensities to compare.
5. Show `docker compose logs --tail=30` to illustrate an HTTP request.
6. Run `docker compose down`.

## Original lab progression

1. `1-docker-hello-world`: containerize and run a FastAPI hello-world service.
2. `2-dsc_streamlit`: run a Streamlit style-transfer app with Docker and Compose.
3. `3-dsc_compose`: run frontend and backend separately, connect them through Docker networking, and orchestrate them with Compose.

The original .t7 files belong to their respective creators; this repository does not redistribute them. The original educational Azure/GitHub Actions examples under exercise subfolders are not part of the StyleLab local deployment and should not be reused without checking their settings and credentials.
