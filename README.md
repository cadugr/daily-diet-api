# Daily Diet API

API para controle diário de dieta, a API de dieta diária.

## Arquitetura e Tecnologias

Este projeto é uma API RESTful desenvolvida em **Python** com o framework **Flask**. Ele utiliza **SQLAlchemy** como ORM para interagir com um banco de dados **MySQL**.

As principais tecnologias utilizadas são:

- **Linguagem:** Python 3
- **Framework:** Flask
- **ORM:** Flask-SQLAlchemy
- **Banco de Dados:** MySQL
- **Gerenciador de Dependências:** pip

## Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:

- [Python 3](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalação e Configuração

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/cadugr/daily-diet-api.git
    cd daily-diet-api
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências do Python:**

    ```bash
    pip3 install -r requirements.txt
    ```

## Executando a Aplicação

1.  **Inicie o banco de dados MySQL com Docker Compose:**

    Este comando irá iniciar um container Docker com o banco de dados MySQL em segundo plano.

    ```bash
    docker-compose up -d
    ```

2.  **Execute a aplicação Flask:**

    ```bash
    python3 app.py
    ```

    A API estará disponível em `http://127.0.0.1:5000`.

## Testando a API

Para testar os endpoints da API, você pode utilizar um cliente de API como o [Postman](https://www.postman.com/).

### Instalação do Postman

Você pode baixar e instalar o Postman a partir do [site oficial](https://www.postman.com/downloads/). Siga as instruções de instalação para o seu sistema operacional.

### Importando a Collection

O projeto inclui uma collection do Postman com exemplos de requisições para todos os endpoints. Para importá-la:

1.  Abra o Postman.
2.  Clique em **Import** no canto superior esquerdo.
3.  Selecione o arquivo `api/tests/Daily Diet API.postman_collection.json` do projeto.
4.  Após a importação, você verá uma nova collection chamada **Daily Diet API** no painel esquerdo.

### Variável de Ambiente

A collection utiliza uma variável `{{baseUrl}}` para o endereço da API. Para configurá-la:

1.  Clique no ícone de olho no canto superior direito para gerenciar os ambientes.
2.  Clique em **Add** para criar um novo ambiente.
3.  Dê um nome ao ambiente (ex: `Daily Diet Local`).
4.  Adicione uma variável chamada `baseUrl` com o valor `http://127.0.0.1:5000`.
5.  Salve o ambiente e certifique-se de que ele esteja selecionado no menu suspenso no canto superior direito.

### Importante

Para cadastrar uma refeição, é necessário primeiro cadastrar um usuário para obter um `user_id` válido. Utilize o endpoint `POST /users` para criar um usuário e, em seguida, use o ID retornado para cadastrar refeições para este usuário.

## Endpoints da API

### Usuários

-   `POST /users`: Cria um novo usuário.
    -   **Body:** `{ "name": "string" }`
-   `GET /users`: Lista todos os usuários.

### Refeições

-   `POST /meals`: Cria uma nova refeição para um usuário.
    -   **Body:** `{ "name": "string", "description": "string", "meal_date": "iso_format_string", "is_on_diet": boolean, "user_id": integer }`
-   `GET /meals/<int:meal_id>`: Retorna uma refeição específica.
-   `GET /users/<int:user_id>/meals`: Lista todas as refeições de um usuário.
-   `PUT /meals/<int:meal_id>`: Atualiza uma refeição.
    -   **Body:** `{ "name": "string", "description": "string", "meal_date": "iso_format_string", "is_on_diet": boolean }`
-   `DELETE /meals/<int:meal_id>`: Deleta uma refeição.

## Configuração do Banco de Dados

A configuração do banco de dados é feita no arquivo `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-db'
```

As variáveis de ambiente para o container do banco de dados estão definidas no arquivo `docker-compose.yml`:

-   `MYSQL_USER`: 'admin'
-   `MYSQL_PASSWORD`: 'admin123'
-   `MYSQL_DATABASE`: 'daily-diet-db'
-   `MYSQL_ROOT_PASSWORD`: 'admin123'

## Estrutura do Projeto

```
.
├── app.py                                # Arquivo principal da aplicação Flask
├── database.py                           # Configuração do SQLAlchemy
├── docker-compose.yml                    # Configuração do serviço de banco de dados
├── requirements.txt                      # Dependências do Python
├── api/
│   └── tests/
│       └── Daily Diet API.postman_collection.json  # Collection do Postman para testes
├── models/
│   ├── user.py           # Modelo de dados do usuário
│   └── meal.py           # Modelo de dados da refeição
├── README.md             # Este arquivo
└── .gitignore            # Arquivo referente ao git
```
