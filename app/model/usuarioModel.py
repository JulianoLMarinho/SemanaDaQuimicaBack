from app.model.baseModel import *


class Usuario(BaseModel):
    __tablename__ = 'usuario'

    id = Column(BigInteger, primary_key=True, server_default=text(
        "nextval('usuario_id_seq'::regclass)"))
    nome = Column(String(100), nullable=False)
    url_foto_perfil = Column(String(500))
    estado = Column(String(50))
    cidade = Column(String(50))
    email = Column(String(255), nullable=False)
    id_google = Column(String(50))
    universidade = Column(String(150))
    curso = Column(String(150))
    nivel = Column(String(50))
    tamanho_camisa = Column(String(10))
    genero = Column(String(20))
    perfil_usuario = Column(ForeignKey('perfil_usuario.id'), nullable=False)

    perfil_usuario1 = relationship('PerfilUsuario')
