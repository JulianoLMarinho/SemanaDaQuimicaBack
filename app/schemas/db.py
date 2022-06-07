# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, LargeBinary, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class EdicaoSemana(Base):
    __tablename__ = 'edicao_semana'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('edicao_semana_id_seq'::regclass)"))
    tema = Column(String(255), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    ativa = Column(Boolean, nullable=False, server_default=text("false"))


class PerfilUsuario(Base):
    __tablename__ = 'perfil_usuario'

    id = Column(BigInteger, primary_key=True, server_default=text(
        "nextval('perfil_usuario_id_seq'::regclass)"))
    nome_perfil = Column(String(50), nullable=False)
    codigo_perfil = Column(String(50), nullable=False)

    permissao = relationship('Permissao', secondary='perfil_permissao')


class Permissao(Base):
    __tablename__ = 'permissao'

    id = Column(BigInteger, primary_key=True, server_default=text(
        "nextval('permissao_id_seq'::regclass)"))
    nome_permissao = Column(String(50), nullable=False)
    codigo_permissao = Column(String(50), nullable=False)


class ResponsavelAtividade(Base):
    __tablename__ = 'responsavel'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('responsavel_atividade_id_seq'::regclass)"))
    nome_responsavel = Column(String(100), nullable=False)
    descricao_responsavel = Column(String(1000))
    id_lattes = Column(String(255))


class TipoAtividade(Base):
    __tablename__ = 'tipo_atividade'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tipo_atividade_id_seq'::regclass)"))
    nome_tipo = Column(String(100), nullable=False)
    descricao_tipo = Column(String(1000), nullable=False)
    cod_tipo = Column(String(50), nullable=False)


class AtividadeEdicao(Base):
    __tablename__ = 'atividade'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('atividade_edicao_id_seq'::regclass)"))
    edicao_semana_id = Column(ForeignKey('edicao_semana.id'), nullable=False)
    ativa = Column(Boolean, nullable=False, server_default=text("true"))
    tipo_atividade = Column(ForeignKey('tipo_atividade.id'))
    descricao_atividade = Column(String, nullable=False)
    vagas = Column(Integer, nullable=False, server_default=text("0"))
    titulo = Column(String(255), nullable=False)

    edicao_semana = relationship('EdicaoSemana')
    tipo_atividade1 = relationship('TipoAtividade')
    responsavel_atividade = relationship(
        'ResponsavelAtividade', secondary='atividade_responsavel')
    turnos = relationship('Turno', secondary='atividade_turno')


class CarousselHeader(Base):
    __tablename__ = 'caroussel_header'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('caroussel_header_id_seq'::regclass)"))
    edicao_semana_id = Column(ForeignKey('edicao_semana.id'), nullable=False)
    imagem = Column(LargeBinary, nullable=False)

    edicao_semana = relationship('EdicaoSemana')


class DetalheEdicao(Base):
    __tablename__ = 'detalhe_edicao'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('detalhe_edicao_id_seq'::regclass)"))
    edicao_semana_id = Column(ForeignKey('edicao_semana.id'), nullable=False)
    descricao_tema = Column(String, nullable=False)

    edicao_semana = relationship('EdicaoSemana')


t_perfil_permissao = Table(
    'perfil_permissao', metadata,
    Column('id_perfil', ForeignKey('perfil_usuario.id'), nullable=False),
    Column('id_permissao', ForeignKey('permissao.id'), nullable=False)
)


class Turno(Base):
    __tablename__ = 'turno'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('turnos_id_seq'::regclass)"))
    nome_turno = Column(String(255), nullable=False)
    edicao_semana_id = Column(ForeignKey('edicao_semana.id'), nullable=False)

    edicao_semana = relationship('EdicaoSemana')


class Usuario(Base):
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


t_atividade_responsavel = Table(
    'atividade_responsavel', metadata,
    Column('id_atividade', ForeignKey('atividade_edicao.id'), nullable=False),
    Column('id_responsavel', ForeignKey(
        'responsavel_atividade.id'), nullable=False)
)


t_atividade_turno = Table(
    'atividade_turno', metadata,
    Column('atividade_id', ForeignKey(
        'atividade_edicao.id', ondelete='CASCADE'), nullable=False),
    Column('turno_id', ForeignKey('turno.id', ondelete='CASCADE'), nullable=False)
)


class DiaHoraAtividade(Base):
    __tablename__ = 'dia_hora_atividade'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('dia_hora_atividade_id_seq'::regclass)"))
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    atividade_edicao_id = Column(ForeignKey(
        'atividade_edicao.id', ondelete='CASCADE', onupdate='CASCADE'))
    turno_id = Column(ForeignKey(
        'turno.id', ondelete='CASCADE', onupdate='CASCADE'))
    dia = Column(Integer, nullable=False)

    atividade_edicao = relationship('AtividadeEdicao')
    turno = relationship('Turno')
