from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router
from .database import init_db
from app.routes import code_runner

app = FastAPI(title="DevDojo API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include our routers
app.include_router(router, prefix="/api/v1")
app.include_router(code_runner.router, prefix="/code-runner", tags=["code-runner"])

@app.get("/")
async def root():
    return {"message": "Welcome to DevDojo API"}
