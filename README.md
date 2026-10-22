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

Docker Compose creates the internal network automatically. The host uses port **8501** for Streamlit and **8080** for FastAPI. Inside the frontend container, the backend is reached via `http://backend:80`. This is the **Compose service name and its container port**, not the host URL. The `depends_on` configuration controls startup order, not whether the API is ready to answer.

## Requirements

- Docker Desktop running (WSL2 on Windows).
- PowerShell for the included Windows model download helper.
- Internet access on first installation if the models were not downloaded earlier.

## Quick start (Windows PowerShell)

For a **fresh clone**, start with:

~~~powershell
git clone --branch feature/stylelab-ai-studio https://github.com/JuanRipoll27/sdc-3.git
cd sdc-3
~~~

If the repository is already on your computer, skip cloning. Use `git switch feature/stylelab-ai-studio` (or `git switch --track origin/feature/stylelab-ai-studio` if needed), followed by `git pull`. Run the following commands at the **repository root**.

**1. Obtain the original course models** (the approximately 200 MB of model files are intentionally not tracked in Git):

```powershell
powershell -ExecutionPolicy Bypass -File .\3-dsc_compose\download_models.ps1
```

The script reuses `2-dsc_streamlit/streamlit/models` if available; otherwise it downloads the files from the Stanford fast-neural-style model collection. The model files are **not in Git** and must be prepared before the first Docker build. You do not need to install Python locally.

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

When `strength=0`, the output is the resized original; `strength=1` is the full neural style output. OpenCV's `cv2.addWeighted` performs the blend after ensuring that the model output and original image have matching dimensions and 8-bit pixel values.

**Test the API from PowerShell:**

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/styles
```

To test image processing directly, put a file named `photo.jpg` in the current PowerShell folder and run:

~~~powershell
curl.exe -f -X POST -F "file=@photo.jpg" -F "strength=0.5" http://localhost:8080/candy -o stylelab-result.png
~~~

Alternatively, use the interactive Swagger UI: expand **POST /{style}**, click **Try it out**, enter a style (for example `candy`), attach an image, set the intensity and select **Execute**. Invalid styles return HTTP 404; invalid images return HTTP 400; intensity values outside 0–1 return HTTP 422.

## Files worth explaining in class

- `3-dsc_compose/frontend/main.py` — interface, upload, HTTP call, preview and PNG download.
- `3-dsc_compose/backend/main.py` — API endpoints, OpenCV conversion, model call and blending.
- `3-dsc_compose/backend/inference.py` — original course inference with pre-trained models.
- `3-dsc_compose/backend/config.py` — maps displayed style names to `.t7` files.
- `3-dsc_compose/docker-compose.yml` — builds the services, maps host ports and connects the internal network.

## Five-minute live demo

A complete **spoken presentation script in English**, including code walkthrough, commands, expected results and likely questions, is available in **[docs/CLASS_DEMO.md](docs/CLASS_DEMO.md)**.


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

### Troubleshooting

| Problem | What to check |
| --- | --- |
| Frontend reports a disconnected backend | `docker compose ps` and `docker compose logs backend --tail=50` |
| Processing returns HTTP 500 | `docker compose logs backend --tail=60`; check `backend/models` contains the downloaded models |
| Port 8501 or 8080 is busy | Use `docker ps` and stop the other app using that host port |
| Changes are not visible | Rebuild with `docker compose up -d --build` and refresh the page |
| A fresh clone cannot process images | Run `download_models.ps1` first; model binaries are excluded from Git |

### Scope and credits

This is a **local educational demo**, not a public cloud deployment. It has no database, authentication or persistent image storage. The original .t7 files belong to their respective creators; this repository does not redistribute them. The original educational Azure/GitHub Actions examples under exercise subfolders are not part of the StyleLab local deployment and should not be reused without checking their settings and credentials.
