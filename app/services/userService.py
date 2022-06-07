from msilib.schema import Error
from typing import List, Tuple
from fastapi import Depends
from app.repository.userRepository import UserRepository
from app.model.usuario import Usuario


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repo = repository

    def getUserByEmail(self, email: str) -> Usuario:
        return self.repo.getUserByEmail(email)

    def getUserByEmailAndGoogleUser(self, email: str, googleUserId: str):
        return self.repo.getUserByEmailAndGoogleUser(email, googleUserId)

    def addUser(self, usuario: Usuario):
        return self.repo.addUser(usuario)

    def getUserById(self, userId: int) -> Usuario:
        return self.repo.getUserById(userId)

    def updateUser(self, user: Usuario) -> bool:
        try:
            self.repo.updateUser(user)
        except:
            return False
        else:
            return True

    def getPermissaoUsuario(self, userId: int) -> List[str]:
        return self.repo.getPermissaoUsuario(userId)
