from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Eventos
import apiRequests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    eventos = Eventos.query.all()
    return render_template('index.html', eventos=eventos)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_inicio = datetime.fromisoformat(request.form['data_inicio'])
        data_fim = datetime.fromisoformat(request.form['data_fim'])
        capacidade = request.form['capacidade']
        gratuito = 'gratuito' in request.form
        preco = request.form['preco'] if not gratuito else None
        idade_minima = request.form['idade_minima']
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        uf = request.form['uf']
        numero = request.form['numero']

        novo_evento = Eventos(
            titulo=titulo,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            capacidade=capacidade,
            gratuito=gratuito,
            preco=preco,
            idade_minima=idade_minima,
            condicoes_climaticas= "",
            cep=cep,
            logradouro=logradouro,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
            numero=numero
        )

        db.session.add(novo_evento)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    evento = db.session.query(Eventos).filter(Eventos.id == id).first()
    if request.method == 'POST':
        evento.titulo = request.form['titulo']
        evento.descricao = request.form['descricao']
        evento.data_inicio = datetime.fromisoformat(request.form['data_inicio'])
        evento.data_fim = datetime.fromisoformat(request.form['data_fim'])
        evento.capacidade = request.form['capacidade']
        evento.gratuito = 'gratuito' in request.form
        evento.preco = request.form['preco'] if not evento.gratuito else None
        evento.idade_minima = request.form['idade_minima']
        evento.condicoes_climaticas = ""
        evento.cep = request.form['cep']
        evento.logradouro = request.form['logradouro']
        evento.bairro = request.form['bairro']
        evento.cidade = request.form['cidade']
        evento.uf = request.form['uf']
        evento.numero = request.form['numero']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', evento=evento)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    evento = db.session.get(Eventos, id)
    if request.method == 'POST':
        db.session.delete(evento)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', evento=evento)

@app.route('/viacep/<cep>', methods=['GET'])
def viacep(cep):
    data = apiRequests.api_viacep(cep)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
