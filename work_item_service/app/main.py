
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models
from .schemas import WorkItemCreate, WorkItemResponse
from .services import (
    create_work_item,
    get_work_items,
    get_work_item_by_id
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Work Item Service",
    description="Microservice for managing employee work items",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "Work Item Service is running"}


@app.post("/work-items", response_model=WorkItemResponse, status_code=201)
def create_work_item_api(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    return create_work_item(db, work_item)


@app.get("/work-items", response_model=list[WorkItemResponse])
def read_work_items(db: Session = Depends(get_db)):
    return get_work_items(db)


@app.get("/work-items/{work_item_id}", response_model=WorkItemResponse)
def read_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    work_item = get_work_item_by_id(db, work_item_id)

    if not work_item:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return work_item
