from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    localizacao = db.Column(db.String(200), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    gratuito = db.Column(db.Boolean, nullable=False, default=True)
    preco = db.Column(db.Float, nullable=True)
    idade_minima = db.Column(db.Integer, nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    atualizado_em = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Eventos {self.titulo}>'
