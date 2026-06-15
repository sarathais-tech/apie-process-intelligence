from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.database.session import create_database
from app.interfaces.api.routes import events, flowcharts, health, narratives, processes, sops


def create_app() -> FastAPI:
    app = FastAPI(
        title="APIE - Adaptive Process Intelligence Engine",
        version="0.1.0",
        description="Captura eventos do Windows e reconstrui processos automaticamente.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(events.router, prefix="/api/v1")
    app.include_router(processes.router, prefix="/api/v1")
    app.include_router(flowcharts.router, prefix="/api/v1")
    app.include_router(sops.router, prefix="/api/v1")
    app.include_router(narratives.router, prefix="/api/v1")

    @app.on_event("startup")
    def on_startup() -> None:
        create_database()

    return app


app = create_app()
