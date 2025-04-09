# **Barbearia Elegância - Sistema de Agendamentos**

## **Descrição**
O **Barbearia Elegância - Sistema de Agendamentos** é uma aplicação desenvolvida para facilitar o gerenciamento de horários em uma barbearia. Permite que os clientes escolham seus horários preferidos com profissionais de confiança, utilizando uma interface intuitiva e uma API documentada com Swagger.

---

## **Funcionalidades**
- **Cadastro de Usuários**: Registre clientes.
- **Agendamento de Horários**: Selecione a data, o horário e o profissional desejado.
- **Listagem de Agendamentos**: Consulte todos os agendamentos realizados.
- **Cancelamento de Agendamentos**: Remova agendamentos indesejados.
- **Verificação de Horários Disponíveis**: Encontre horários livres com base na data e no profissional.
- **Documentação da API**: Endpoints documentados com Swagger para facilitar a integração.

---

## **Tecnologias Utilizadas**
### **Backend**
- **Linguagem**: Python
- **Framework**: Flask
- **Banco de Dados**: SQLite
- **Documentação**: Flasgger (Swagger para Flask)

### **Frontend**
- **HTML/CSS**: Estruturado com Bootstrap para um design responsivo.
- **JavaScript**: Dinamismo com `fetch` para integração com a API.

---

## **Configuração e Execução**

### **Pré-requisitos**
- Python 3.9 ou superior
- Gerenciador de pacotes `pip`

### **Instalação**
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/barbearia-elegancia.git
   cd barbearia-elegancia
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv meu_ambiente
   source meu_ambiente/bin/activate  # Para Linux/Mac
   meu_ambiente\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a aplicação:
   ```bash
   python app.py
   ```

### **Acessando o Sistema**
- Backend: Acesse a API documentada em [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs).
- Frontend: Abra o arquivo `index.html` no navegador.

---

## **Endpoints da API**
### **Usuários**
- `POST /cadastrar_usuario` - Cadastra um novo usuário.
- `GET /buscar_usuarios` - Lista todos os usuários.
- `DELETE /deletar_usuario/<int:id>` - Exclui um usuário.

### **Agendamentos**
- `POST /cadastrar_agendamento` - Cria um novo agendamento.
- `GET /buscar_agendamentos` - Lista todos os agendamentos.
- `DELETE /deletar_agendamento/<int:id>` - Cancela um agendamento.
- `POST /horarios_disponiveis` - Consulta horários disponíveis.

---

## **Próximos Passos**
- Implementar autenticação de usuários.
- Adicionar notificações por e-mail para lembretes de agendamentos.
- Otimizar o design e a usabilidade do frontend.
- Implantar o sistema em produção.
