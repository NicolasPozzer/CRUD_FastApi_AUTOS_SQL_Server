from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import autoController
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los dominios. Cambia "*" a ["http://localhost:3000"] o el dominio específico si prefieres restringir.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# implement endpoints
app.include_router(autoController.router)

# endpoint test
@app.get("/")
def message():
    return "Hello world"
