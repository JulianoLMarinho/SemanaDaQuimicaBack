from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.model.authRequestBody import AuthRequestBody
from app.route_setup import bind_routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from app.services.authorizationService import AuthorizationService
from app.sql.database import close_connection_pools, open_connection_pools


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI(
    on_startup=[open_connection_pools],
    on_shutdown=[close_connection_pools]
)


origins = [
    "http://localhost:4200",
    "https://localhost:4200",
    "http://julianomarinho.provisorio.ws",
    "https://greattestapp.azurewebsites.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
app.include_router(userController.router, prefix='/usuario', tags=['Usuários'])
app.include_router(carrouselInicioController.router,
                   prefix='/carrousel', tags=["Início"])
app.include_router(edicaoSemanaController.router,
                   prefix='/edicaoSemana', tags=['Edição Semana'])
app.include_router(atividadesController.router,
                   prefix='/atividades', tags=['Atividades'])
"""

bind_routers(app)


@ app.post("/authenticate")
def authenticate(
    token: AuthRequestBody,
    service: AuthorizationService = Depends()
):
    return service.authorize(token)
