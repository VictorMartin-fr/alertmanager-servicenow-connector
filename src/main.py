from fastapi import FastAPI
from src.api import webhook
from src.core.database import connect_to_mongo,close_mongo_connection

async def lifespan(app: FastAPI):
    print("ASC API starting...")
    await connect_to_mongo()
    yield
    print("ASC API ending...")
    close_mongo_connection()

app = FastAPI(
    title = "ASC",
    description = "API to connect AlertManager to ServiceNow while reduce noise",
    version = "0.0.1",
    lifespan=lifespan
)

app.include_router(webhook.router)

@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Bridge is running"}