from typing import List
from xmlrpc.client import boolean
from fastapi import APIRouter, Depends
from sqlalchemy import true
from app.dependencies import current_user_is_admin, get_current_active_user
from app.model.usuario import Usuario
from app.services.userService import UserService

router = APIRouter()
prefix = '/usuario'
tags = ['Usuários']


@router.get("", response_model=Usuario)
def get_user(
    service: UserService = Depends(),
    usuario: Usuario = Depends(get_current_active_user)
):
    return service.getUserById(usuario['id'])


@router.get("/get-all", response_model=List[Usuario], dependencies=[Depends(current_user_is_admin)])
def get_all(service: UserService = Depends()):
    return service.getAll()


@router.get("/getUserByEmail", response_model=Usuario)
def get_all(service: UserService = Depends()):
    return service.getUserByEmail('j.delimamarinho@gmail.com')


@router.post("")
def addUser(
    usuario: Usuario,
    service: UserService = Depends()
):
    return service.addUser(usuario)


@router.put("")
def updateUser(
    usuario: Usuario,
    service: UserService = Depends(),
    usuarioLogado: Usuario = Depends(get_current_active_user)
) -> bool:
    return service.updateUser(usuario)


@router.put("/perfil/{usuarioId}/{perfilId}", dependencies=[Depends(current_user_is_admin)])
def alterarPerfilUsuario(
    usuarioId: int,
    perfilId: int,
    service: UserService = Depends()
):
    service.alterarPerfilUsuario(usuarioId, perfilId)
