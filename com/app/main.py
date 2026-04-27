from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from com.app.config.config import Config
from com.app.database.db_connection.db_connection import Base, engine
from com.app.services.chat.chat_router import router as chat_router
from com.app.services.listings.listings_router import router as listings_router

config = Config()

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StayEase AI Agent",
    description="Conversational booking agent for StayEase — a short-term accommodation rental platform in Bangladesh.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat_router)
app.include_router(listings_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "StayEase AI Agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("com.app.main:app", host=config.APP_HOST, port=config.APP_PORT, reload=config.DEBUG)