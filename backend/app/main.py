"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine, init_db
from app.routes import chat
from app.config import get_settings

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="AI CRM HCP Module",
    description="Healthcare Professional CRM with AI-driven interaction logging",
    version="1.0.0"
)

# Configure CORS (allow frontend to connect)
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # Alternative React port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI CRM HCP Module API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    init_db()
    print("\n" + "="*50)
    print("🚀 AI CRM HCP Module Backend Started!")
    print("📖 API Docs: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/health")
    print("="*50 + "\n")
