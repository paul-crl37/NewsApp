from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as news_router

app = FastAPI(title="News App avec Résumé")

# Autoriser le frontend (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pour dev local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter les routes
app.include_router(news_router, prefix="/news")
