from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

import json
import os

# ========= Config Loads ==========

if os.getenv("IS_TEST_ENV"):
    config_path_1 = "tests/config/auth.json"
else:
    config_path_1 = "config/auth.json"

with open(config_path_1, 'r') as f:
    auth = json.load(f)
    auth_data = auth['auth_data']
    SECRET_KEY = auth_data["secret_key"]
    ALGORITHM = auth_data["algorithm"]


# ========= REST-Api Creation ==========

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ========= Web Pages ==========


@app.get("/favicon.ico",
         summary="Favicon Link",
         description="This endpoint returns the favicon for the webapp",
         tags=["Webpages"])
def read_favicon():
    return FileResponse("static/images/favicon.ico")


# Health
@app.get("/api/v1/health",
         summary="Health Check",
         description="This endpoint is used to check the health of the server",
         tags=["Public"])
def health():
    return {"message": "ok"}


# Home Page
@app.get("/",
         summary="Home Page?",
         description="Am I Blind?",
         tags=["Webpages"])
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/heehee",
         summary="Hee Hee",
         description="Hee Hee",
         tags=["Public"])
def heehee():
    return {"message": "8====D"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=25463,
        log_level="debug",
        reload=True,
        # ssl_keyfile="config/keyfile.key",
        # ssl_certfile="config/certfile.crt",
        )