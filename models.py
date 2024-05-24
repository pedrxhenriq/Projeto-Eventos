from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    gratuito = db.Column(db.Boolean, nullable=False, default=True)
    preco = db.Column(db.Float, nullable=True)
    idade_minima = db.Column(db.Integer, nullable=True)
    condicoes_climaticas = db.Column(db.String(1000), nullable=True)
    cep = db.Column(db.String(10), nullable=False)
    logradouro = db.Column(db.String(200), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(10), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    atualizado_em = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Eventos {self.titulo}>'
