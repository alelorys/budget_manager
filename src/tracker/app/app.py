from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn

from tracker.db.utils import SessionLocal, initialize_db

from tracker.app.routes import services, operations

engine = initialize_db(echo=False)
SessionLocal.configure(bind=engine, expire_on_commit=False, future=True)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(services.route)
app.include_router(operations.route)
if __name__ == "__main__":
    uvicorn.run('app:app',
                host='127.0.0.1',
                port=2345,
                reload=True)