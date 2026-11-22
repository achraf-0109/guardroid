from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import MODEL_PATH 
from routes.routes import router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(MODEL_PATH)
    app.state.features = joblib.load(MODEL_PATH).feature_names_in_.tolist()
    yield

my_app = FastAPI(
    title="Guardroid API",
    version="1.0.0",
    lifespan=lifespan,
)

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

my_app.include_router(router)