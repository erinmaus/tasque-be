from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tasque.constants import TASQUE_ORIGINS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=TASQUE_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from tasque.model import (
    account,
    content,
    label,
    organization,
    project,
    status,
    ticket,
    ticket_to_ticket,
    token,
)
from .view import authentication, project, status, label

router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(authentication.router)
router_v1.include_router(project.router)
router_v1.include_router(status.router)
router_v1.include_router(label.router)

app.include_router(router_v1)
