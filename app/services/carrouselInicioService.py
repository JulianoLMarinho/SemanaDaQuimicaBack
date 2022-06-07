from typing import List

from fastapi import Depends
from app.model.carrouselInicio import CarrouselInicio
from app.repository.carrouselInicioRepository import CarrouselInicioRepository


class CarrouselInicioService():
    def __init__(self, repository: CarrouselInicioRepository = Depends()):
        self.repo = repository

    def getImages(self) -> List[CarrouselInicio]:
        return self.repo.getImages()
