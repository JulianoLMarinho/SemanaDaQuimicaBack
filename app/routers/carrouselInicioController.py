from typing import List
from xmlrpc.client import boolean
from fastapi import APIRouter, Depends
from sqlalchemy import true
from app.dependencies import get_current_active_user
from app.model.carrouselInicio import CarrouselInicio
from app.model.usuario import Usuario
from app.services.carrouselInicioService import CarrouselInicioService
from app.services.userService import UserService

router = APIRouter()
prefix = '/carrousel'
tags = ["Início"]


@router.get("", response_model=List[CarrouselInicio])
def get(
    service: CarrouselInicioService = Depends()
):
    return service.getImages()
