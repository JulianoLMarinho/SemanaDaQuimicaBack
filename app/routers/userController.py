from xmlrpc.client import boolean
from fastapi import APIRouter, Depends
from sqlalchemy import true
from app.dependencies import get_current_active_user
from app.model.usuario import Usuario
from app.services.userService import UserService

router = APIRouter()
prefix = '/usuario'
tags = ['Usuários']


@router.get("", response_model=Usuario)
async def get_user(
    service: UserService = Depends(),
    usuario: Usuario = Depends(get_current_active_user)
):
    return service.getUserById(usuario['id'])


@router.get("/getAll", response_model=Usuario)
async def get_all(service: UserService = Depends()):
    return service.get_all()


@router.get("/getUserByEmail", response_model=Usuario)
async def get_all(service: UserService = Depends()):
    return service.getUserByEmail('j.delimamarinho@gmail.com')


@router.post("")
async def addUser(
    usuario: Usuario,
    service: UserService = Depends()
):
    return service.addUser(usuario)


@router.put("")
async def updateUser(
    usuario: Usuario,
    service: UserService = Depends(),
    usuarioLogado: Usuario = Depends(get_current_active_user)
) -> bool:
    return service.updateUser(usuario)
