from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, json
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
    for evento in eventos:
        evento.condicoes_climaticas = json.loads(evento.condicoes_climaticas)
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

        datas = obter_datas(data_inicio, data_fim)
        tempo = apiRequests.api_condicoes_climaticas(f"{cidade},BR")
        
        condicoes_climaticas = json.dumps(combinar_arrays(datas, tempo))

        novo_evento = Eventos(
            titulo=titulo,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            capacidade=capacidade,
            gratuito=gratuito,
            preco=preco,
            idade_minima=idade_minima,
            condicoes_climaticas= condicoes_climaticas,
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
        evento.cep = request.form['cep']
        evento.logradouro = request.form['logradouro']
        evento.bairro = request.form['bairro']
        evento.cidade = request.form['cidade']
        evento.uf = request.form['uf']
        evento.numero = request.form['numero']

        datas = obter_datas(evento.data_inicio, evento.data_fim)
        tempo = apiRequests.api_condicoes_climaticas(f"{evento.cidade},BR")
        
        evento.condicoes_climaticas = json.dumps(combinar_arrays(datas, tempo))

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', evento=evento)

def obter_datas(data_inicial, data_final):
    datas = []
    data_atual = data_inicial
    datas.append(data_atual.strftime('%Y-%m-%d'))

    if data_inicial.strftime('%Y-%m-%d') == data_final.strftime('%Y-%m-%d'):
        return datas

    while data_atual < data_final:
        data_atual += timedelta(days=1)
        if data_atual <= data_final:
            datas.append(data_atual.strftime('%Y-%m-%d'))

    return datas

def combinar_arrays(array_datas, array_informacoes):
    resultado = {}
        
    for data in array_datas:
        encontrado = False
        for info in array_informacoes:
            if data in info:
                data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                resultado[data_formatada] = info[data]
                encontrado = True
                break
            
        if not encontrado:
            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            resultado[data_formatada] = f"API OpenWeather não tem informações sobre a data {data_formatada}"
        
    return resultado  

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
