from fastapi import FastAPI
from app.model.authRequestBody import AuthRequestBody
from app.route_setup import bind_routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import Depends
from app.services.authorizationService import AuthorizationService
from app.sql.database import dbEngine

app = FastAPI(
    on_startup=[dbEngine.open_connection_pools],
    on_shutdown=[dbEngine.close_connection_pools]
)


origins = [
    "http://localhost:4200",
    "https://localhost:4200",
    "http://julianomarinho.provisorio.ws",
    "https://teste.semanadaquimicaufrj.com.br",
    "https://semanadaquimicaufrj.com.br",
    "https://www.semanadaquimicaufrj.com.br"
]

app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bind_routers(app)


@ app.post("/authenticate")
def authenticate(
    token: AuthRequestBody,
    service: AuthorizationService = Depends()
):
    return service.authorize(token)
