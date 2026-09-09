"""
FastAPI backend for the Sovereign Agentic AI Workbench MVP.

This is the Phase 1 skeleton - the foundation for future phases.
"""

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Sovereign Agentic AI Workbench",
    description="Local AI workbench for industrial question answering",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Simple health check endpoint.

    Returns:
        HealthResponse: Status of the backend service.
    """
    return HealthResponse(status="ok")


@app.get("/")
async def root():
    """
    Root endpoint with basic API information.
    """
    return {
        "name": "Sovereign Agentic AI Workbench",
        "version": "0.1.0",
        "health": "/health",
        "docs": "/docs",
        "note": "MVP skeleton - more endpoints will be added in future phases.",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
