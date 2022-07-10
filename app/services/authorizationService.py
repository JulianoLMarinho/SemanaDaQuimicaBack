from datetime import datetime, timedelta
from app.jwt.decode import decode
from app.model.authRequestBody import AuthRequestBody
from app.model.authResponseBody import AuthResponseBody
from app.model.usuario import Usuario
from app.repository.authorizationRepository import AuthorizationRepository
from app.services.userService import UserService
from app.sql.connections import MainConnection
from fastapi import Depends
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
import os


class AuthorizationService:
    def __init__(self, repository: AuthorizationRepository = Depends(), userService: UserService = Depends()):
        self.repo = repository
        self.userService = userService

    def test(self):
        return self.repo.test()

    def authorize(self, authRequest: AuthRequestBody):
        if authRequest.source == 'GOOGLE':
            return self.authorizeFirebase(authRequest)

    def authorizeFirebase(self, authRequest: AuthRequestBody) -> AuthResponseBody:
        idinfo = decode(authRequest.token)
        userGoogleId = idinfo['user_id']
        userEmail = idinfo['email']
        user = self.userService.getUserByEmailAndGoogleUser(
            userEmail, userGoogleId)
        if user == None:
            user = Usuario(id=0, nome=idinfo['name'], email=idinfo['email'],
                           url_foto_perfil=idinfo['picture'], id_google=userGoogleId)
            user.perfil = 'adm'
            user.permissoes = []
            response = AuthResponseBody(
                usuario=user, responseType='USUARIO_NAO_EXISTE')
            return response
        else:
            user.permissoes = []
            user.url_foto_perfil = idinfo['picture']
            user.permissoes = self.userService.getPermissaoUsuario(
                user.id)
            key = os.getenv("JWT_KEY")
            payloadUser = user.dict()
            payloadUser['sub'] = user.email
            expirationDate = datetime.utcnow() + timedelta(minutes=60)
            payloadUser['exp'] = expirationDate
            jwtToken = jwt.encode(payloadUser, key)
            return AuthResponseBody(usuario=user, responseType='OK', access_token=jwtToken)

    def authorizeGoogle(self, authRequest: AuthRequestBody) -> AuthResponseBody:
        idinfo = id_token.verify_oauth2_token(authRequest.token, requests.Request(
        ), os.getenv("GOOGLE_KEY"), 50)
        userGoogleId = idinfo['sub']
        userEmail = idinfo['email']
        user = self.userService.getUserByEmail(userEmail)
        if user == None:
            user = Usuario(id=0, nome=idinfo['name'], email=idinfo['email'],
                           url_foto_perfil=idinfo['picture'], id_google=userGoogleId)
            user.perfil = 'adm'
            user.permissoes = []
            response = AuthResponseBody(
                usuario=user, responseType='USUARIO_NAO_EXISTE')
            return response
        else:
            user.permissoes = []
            if (user.id_google == None):
                return AuthResponseBody(user, 'GOOGLE_NAO_ASSOCIADO', authRequest.token)
            elif (user.id_google != userGoogleId):
                raise HTTPException(403, 'CONFLITO_GOOGLE')
            else:
                user.url_foto_perfil = idinfo['picture']
                user.permissoes = self.userService.getPermissaoUsuario(
                    user.id)
                key = os.getenv("JWT_KEY")
                payloadUser = user.dict()
                payloadUser['sub'] = user.email
                expirationDate = datetime.utcnow() + timedelta(minutes=60)
                payloadUser['exp'] = expirationDate
                jwtToken = jwt.encode(payloadUser, key)
                return AuthResponseBody(usuario=user, responseType='OK', access_token=jwtToken)
