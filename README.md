# chatbot_generic
Generic template for chatbot using Django Rest Framework and PostgreSQL.

## Folder structure
```
chatbot_generic
├── chatbot
│  ├── migrations
│  │  └── __init__.py
│  ├── admin.py
│  ├── apps.py
│  ├── models.py
│  ├── serializers.py
│  ├── tests.py
│  ├── urls.py
│  ├── views.py
│  └── __init__.py
├── chatbot_generic
│  ├── asgi.py
│  ├── settings.py
│  ├── urls.py
│  ├── wsgi.py
│  └── __init__.py
├── utils
│  ├── chat.py
│  └── files_processing.py
├── config.py
├── docker-compose.yml
├── Dockerfile
├── logging_config.py
├── manage.py
├── README.md
└── requirements.txt

```

- The **chatbot_generic** is the project folder while **chatbot** contains all the code related to the chatbot app.
- The **utils** contains all the code related to the utility functions e.g. switching llm, chat using llama-index framework and file processing, etc.
- The **config** contains all the constants from the environment and the **logging_config** is to generate logs.
- **Dockerfile** is for Django image building.
- **docker-compose.yml** is used to containerize all the frameworks used - Django + PostgreSQL.
- Note that there's no need to create a separate container inside Docker for PostgreSQL if Amazon RDS is used...
- Refer the image for the configuration of the PostgreSQL.
- <img width="1341" height="748" alt="image" src="https://github.com/user-attachments/assets/12639bb1-f796-42a5-bb1b-2e7487f14406" />

## Installation

Go to the cloned repository & create the virtual enviroment in python
```bash
  cd oakdrf
```

```bash
  python venv myvenv
```

Activate the virtual enviroment.

```bash
  myvenv\Scripts\activate
```

Install the requirements
```bash
  pip install -r "requirements.txt"
```
 Since the data will be stored in PostgreSQL, we will have to run migrations to set up the tables in the database.
ENter username and password in settings.py before running migrations


 ```bash
  python manage.py makemigrations
  python manage.py migrate
```
The two tables will be created and they will have a relationship like this...
<img width="1288" height="615" alt="image" src="https://github.com/user-attachments/assets/18b180b1-aec2-4fdf-852d-3274689f24a5" />



## API Reference

### Chatbot

```http
  POST /chatbot/chat/
```

| Body Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| text | str | name of the document context  |
| query | str | query  |
| llm_name | str | name of the LLM that will be used for querying  |
| session_id | uuid | Optional. id of the session. if not given will create a new session id  |

