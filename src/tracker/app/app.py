from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from tracker.db.utils import SessionLocal, initialize_db

from tracker.app.routes import services, operations
from tracker.consts import Consts

engine = initialize_db(echo=False)
SessionLocal.configure(bind=engine, expire_on_commit=False, future=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Uwaga: w produkcji określ konkretne źródła
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
app.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")

app.include_router(services.route)
app.include_router(operations.route)
if __name__ == "__main__":
    uvicorn.run('app:app',
                host='127.0.0.1',
                port=2345,
                reload=True)