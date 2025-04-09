from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
import datetime

app = Flask(__name__)
CORS(app)

# Configuração do Swagger com autenticação e detalhes do projeto
template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Agendamentos - Barbearia Elegância",
        "description": "Documentação da API de agendamentos e usuários.",
        "version": "1.0.0"
    },
    "host": "127.0.0.1:5000",
    "basePath": "/",
    "schemes": ["http"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}
Swagger(app, template=template)

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbearia.db'
db = SQLAlchemy(app)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Modelo de Agendamento
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    profissional = db.Column(db.String(100), nullable=False)

# Criar Banco de Dados dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Rota para cadastrar usuário
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
    Cadastrar um novo usuário.
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - email
          properties:
            nome:
              type: string
              description: Nome do usuário.
              example: "Carlos Souza"
            email:
              type: string
              description: E-mail do usuário.
              example: "carlos@email.com"
    responses:
      200:
        description: Usuário cadastrado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Usuário cadastrado com sucesso!"
      400:
        description: Erro ao cadastrar usuário.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "E-mail já cadastrado!"
    """
    dados = request.json
    novo_usuario = Usuario(nome=dados['nome'], email=dados['email'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'})

# Rota para buscar usuários
@app.route('/buscar_usuarios', methods=['GET'])
def buscar_usuarios():
    """
    Listar todos os usuários cadastrados.
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários cadastrados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Carlos Souza"
              email:
                type: string
                example: "carlos@email.com"
    """
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nome': u.nome, 'email': u.email} for u in usuarios])

# Rota para deletar usuário
@app.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    """
    Deletar um usuário pelo ID.
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário.
    responses:
      200:
        description: Usuário deletado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Usuário deletado com sucesso!"
      404:
        description: Usuário não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Usuário não encontrado!"
    """
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'mensagem': 'Usuário deletado com sucesso!'}), 200
    return jsonify({'erro': 'Usuário não encontrado!'}), 404

# Rota para cadastrar um agendamento
@app.route('/cadastrar_agendamento', methods=['POST'])
def cadastrar_agendamento():
    """
    Cadastrar um novo agendamento.
    ---
    tags:
      - Agendamentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - data
            - horario
            - profissional
          properties:
            nome:
              type: string
              description: Nome do cliente.
              example: "Diego Silva"
            data:
              type: string
              description: Data do agendamento (formato YYYY-MM-DD).
              example: "2025-04-10"
            horario:
              type: string
              description: Horário do agendamento (formato HH:mm).
              example: "14:00"
            profissional:
              type: string
              description: Nome do profissional.
              example: "João"
    responses:
      200:
        description: Agendamento cadastrado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Agendamento cadastrado com sucesso!"
      400:
        description: Erro ao cadastrar agendamento.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Não é possível agendar para uma data retroativa!"
    """
    dados = request.json
    data_agendamento = datetime.datetime.strptime(dados['data'], '%Y-%m-%d').date()
    data_atual = datetime.date.today()

    if data_agendamento < data_atual:
        return jsonify({'erro': 'Não é possível agendar para uma data retroativa!'}), 400

    agendamento_existente = Agendamento.query.filter_by(
        data=dados['data'],
        horario=dados['horario'],
        profissional=dados['profissional']
    ).first()

    if agendamento_existente:
        return jsonify({'erro': 'Esse horário já está ocupado para o profissional escolhido!'}), 400

    novo_agendamento = Agendamento(
        nome=dados['nome'],
        data=dados['data'],
        horario=dados['horario'],
        profissional=dados['profissional']
    )
    db.session.add(novo_agendamento)
    db.session.commit()
    return jsonify({'mensagem': 'Agendamento cadastrado com sucesso!'})

# Rota para buscar agendamentos
@app.route('/buscar_agendamentos', methods=['GET'])
def buscar_agendamentos():
    """
    Listar todos os agendamentos.
    ---
    tags:
      - Agendamentos
    responses:
      200:
        description: Lista de agendamentos.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Diego Silva"
              data:
                type: string
                example: "2025-04-10"
              horario:
                type: string
                example: "14:00"
              profissional:
                type: string
                example: "João"
    """
    agendamentos = Agendamento.query.all()
    return jsonify([
        {'id': a.id, 'nome': a.nome, 'data': a.data, 'horario': a.horario, 'profissional': a.profissional}
        for a in agendamentos
    ])
# Rota para deletar agendamento
@app.route('/deletar_agendamento/<int:id>', methods=['DELETE'])
def deletar_agendamento(id):
    """
    Cancelar um agendamento pelo ID.
    ---
    tags:
      - Agendamentos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do agendamento.
    responses:
      200:
        description: Agendamento cancelado com sucesso.
      404:
        description: Agendamento não encontrado.
    """
    agendamento = Agendamento.query.get(id)
    if agendamento:
        db.session.delete(agendamento)
        db.session.commit()
        return jsonify({'mensagem': 'Agendamento cancelado com sucesso!'}), 200
    return jsonify({'erro': 'Agendamento não encontrado!'}), 404

# Rota para verificar horários disponíveis
@app.route('/horarios_disponiveis', methods=['POST'])
def horarios_disponiveis():
    """
    Consultar horários disponíveis para um profissional em uma data.
    ---
    tags:
      - Agendamentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - data
            - profissional
          properties:
            data:
              type: string
              description: Data para verificar os horários (formato YYYY-MM-DD).
              example: "2025-04-10"
            profissional:
              type: string
              description: Nome do profissional.
              example: "João"
    responses:
      200:
        description: Lista de horários disponíveis.
        schema:
          type: array
          items:
            type: string
            example: "14:00"
    """
    dados = request.json
    data = dados['data']
    profissional = dados['profissional']

    # Lista de horários padrão
    horarios_padrao = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00', '17:00']

    # Buscar horários já agendados para o profissional na data
    agendamentos = Agendamento.query.filter_by(data=data, profissional=profissional).all()
    horarios_ocupados = [a.horario for a in agendamentos]

    # Remover horários ocupados
    horarios_disponiveis = [h for h in horarios_padrao if h not in horarios_ocupados]

    return jsonify({'horarios_disponiveis': horarios_disponiveis})

if __name__ == '__main__':
    app.run(debug=True)