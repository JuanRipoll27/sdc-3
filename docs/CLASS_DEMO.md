# StyleLab — Five-Minute Class Demo

**Course:** Solution Deployment & Communication, Lab 3
**Presentation language:** English
**Working directory:** `3-dsc_compose`

## Before class

Make sure Docker Desktop is running, your `.t7` models exist in `backend/models`, and you have one JPG/PNG that you are allowed to show.

```powershell
cd "C:\Users\Juani\ITBA\UTSW\SDC\sdc-3"
powershell -ExecutionPolicy Bypass -File .\3-dsc_compose\download_models.ps1
cd .\3-dsc_compose
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://localhost:8080/health
```

Keep `http://localhost:8501` (StyleLab) and `http://localhost:8080/docs` (Swagger) open. For a short demo, start the containers before class so that builds do not interrupt your talk.

## 0:00–0:45 — Introduce StyleLab

> “StyleLab is my extension of our Docker lab. I reused the pre-trained neural style-transfer models from the exercise and developed a more complete interface with intensity control, side-by-side comparison and PNG downloads.”

> “The objective is to show how a frontend and an API can run in separate Docker containers and communicate through Docker Compose.”

**Show:** the StyleLab user interface.

## 0:45–1:30 — Explain the architecture

> “There are two services. Streamlit is the frontend: it lets the user upload a photo and select settings. FastAPI is the backend: it runs the image transformation with OpenCV and a pre-trained Torch model and returns a PNG.”

> “The frontend calls the backend over HTTP. Docker Compose creates their network, so the hostname `backend` resolves to the backend container. `localhost` inside the frontend container would not refer to the backend.”

**Show:** `3-dsc_compose/docker-compose.yml`. Point to `frontend`, `backend`, `ports`, `APP_BACKEND_URL` and `depends_on`. Clarify that `depends_on` controls startup order, not readiness.

## 1:30–2:10 — Demonstrate Docker

```powershell
docker compose ps
```

> “I start the system with `docker compose up -d --build`. Docker builds the two images, starts their containers in the background, and creates a shared network. This command shows both running services and their ports.”

**Explain:** host port 8501 goes to the Streamlit container, host port 8080 goes to FastAPI; the frontend internally uses `http://backend:80`.

## 2:10–2:45 — Show API endpoints

**Show:** `http://localhost:8080/docs`.

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/styles
```

> “FastAPI automatically generates this Swagger interface. I added `/health` so I can check that the service is online, and `/styles` so Streamlit can request the supported styles instead of keeping a separate list.”

**Expected health JSON:** `{"status": "ok", "service": "stylelab-backend"}`.

## 2:45–4:20 — Process a photo

**Show:** `http://localhost:8501`. Upload a JPG/PNG, choose Candy, set 50%, select **Generate artwork**, compare the two images and click **Download PNG**. Repeat at 100% only if time permits.

> “Streamlit sends the image and the intensity as a multipart HTTP POST. The backend converts the input to the color format expected by OpenCV, runs the pre-trained model, and then combines the styled output with the original.”

> “The intensity is a weighted average: zero percent produces the resized original image, fifty percent a mix, and one hundred percent the model output. Both images must have the same size for `cv2.addWeighted`, so I added resizing when needed. FastAPI sends back a PNG for the frontend to display and download.”

**Code references:**

- `frontend/main.py`: `st.slider`, `requests.post`, `st.image`, `st.download_button`.
- `backend/main.py`: `@app.get('/health')`, `@app.get('/styles')`, `@app.post('/{style}')`, `cv2.addWeighted`.
- `backend/inference.py`: `cv2.dnn.readNetFromTorch` and `model.forward` (starter implementation).
- `backend/config.py`: dictionary mapping UI labels to pre-trained `.t7` files.

## 4:20–5:00 — Logs and shutdown

```powershell
docker compose logs backend --tail=20
docker compose down
```

> “The backend logs show the POST request from Streamlit and its HTTP status. `docker compose down` stops and removes these containers and their network. The built images and downloaded models remain available for next time.”

## Questions you may get

| Question | Short answer |
| --- | --- |
| Why use two containers? | To separate presentation (Streamlit) and image processing (FastAPI). |
| What is an image versus a container? | An image packages the code and dependencies; a container runs that image. |
| What does Docker Compose add? | A YAML definition of services, builds, ports, networking and environment variables. |
| Why `backend:80` instead of `localhost:8080`? | Within Docker, service names resolve on the shared network; localhost refers to the current container. |
| What is `-d`? | Detached mode: the containers run in the background. |
| What does the intensity slider change? | The blend between the original and styled images after inference; it does not modify the model weights. |
| Why did you resize the result? | OpenCV needs equal image dimensions for element-wise blending. |
| Did you train an AI model? | No. The lab supplies pre-trained models; my work is deployment, API extensions and user experience. |
| What did you add? | Updated UI, download, intensity control, dynamic styles endpoint, health check, documentation and Compose cleanup. |
| Are model files in Git? | No; they are too large for the source repo and are downloaded by a script. |
| Is it hosted online? | No; this is a local Docker Compose demo, not a production cloud deployment. |
| How do you inspect an error? | `docker compose logs backend --tail=60` and `docker compose ps`. |

## Submission and demo checklist

- [ ] `docker compose up -d --build` completes.
- [ ] `docker compose ps` shows two running services.
- [ ] Swagger `/health` and `/styles` respond.
- [ ] Image processing succeeds at 50% and 100%.
- [ ] PNG download opens.
- [ ] `.t7` files are not committed to Git.
- [ ] README and this guide are on the intended Git branch.
- [ ] Confirm the course's required submission branch/link.

**Closing sentence:** “StyleLab demonstrates a working two-container architecture with a small, understandable extension to both the API and the user interface.”
