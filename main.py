from fastapi import FastAPI

import models
from database import engine

from routers import (
    auth,
    assets,
    requests,
    assignment,
    reports
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT Helpdesk Asset Service Request System"
)

app.include_router(auth.router)
app.include_router(assets.router)
app.include_router(requests.router)
app.include_router(assignment.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to IT Helpdesk Asset Service Request System"
    }