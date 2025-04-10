# Polls

This is a simple polling application built with Django as part of the official Django Tutorial.
It allows users to vote on questions, view results, and manage polls via the admin panel.
> ⚠️ This project is primarily educational and designed to demonstrate the basics of working with Django.

## Stack:

- [Python 3.10.11](https://www.python.org/downloads/release/python-31011/)
- [Django 4.2.10](https://docs.djangoproject.com/en/4.2/)

## Local Development

All commands should be run from the root directory of the project.
Make sure you have Python 3.10.11 installed, and all required packages are installed inside a virtual environment.

### 1. Create and activate a virtual environment:
<details>
<summary>Depending on your setup:</summary>

```bash
python -m venv ./venv # if Python 3.10 is your default version
py -3.10 -m venv ./venv # if Python 3.10 is installed as a secondary version
.\venv\Scripts\activate # on Windows
source venv/bin/activate # on Linux/macOS
```
</details>

### 2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Apply migrations and create a superuser:

```bash
cd ./polls_site/
python manage.py migrate
python manage.py createsuperuser
```
   
### 4. Load initial test data (fixtures):

```bash
python manage.py loaddata polls/fixtures/polls.json
```

### 5. Run the development server:

```bash
python manage.py runserver
```

## Extra

If you make changes to the database and want to save new fixtures:

```bash
python manage.py dumpdata polls.Question polls.Choice --indent 2 > polls/fixtures/polls.json
```