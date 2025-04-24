# Polls

This is a simple polling application built with Django, initially based on the official Django Tutorial.

While the core functionality follows the original guide, this version includes several custom improvements and enhancements.

> ⚠️ This project is for educational purposes and intended to demonstrate Django basics and independent problem-solving.

## What's different from the original tutorial?

- 💅 Added Bootstrap styling for improved UI/UX
- 🔐 Implemented session-based protection to prevent repeated voting
- 🔁 Replaced the “Vote Again” button with a “Change Vote” feature
- 🧪 Added custom unit tests beyond the tutorial examples

## Stack

- [Python 3.10.11](https://www.python.org/downloads/release/python-31011/)
- [Django 4.2.10](https://docs.djangoproject.com/en/4.2/)

## Local Development

All commands should be run from the root directory of the project.  
Make sure you have Python 3.10.11 installed, and all required packages are installed inside a virtual environment.

### 1. Create and activate a virtual environment:
<details>
<summary>Depending on your setup:</summary>

```bash
python -m venv ./venv           # Default
py -3.10 -m venv ./venv         # If Python 3.10 is installed separately
.\venv\Scripts\activate         # Windows
source venv/bin/activate        # Linux/macOS
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

If you make changes to the polls or choices in the admin panel and want to save that data as a fixture for later use:

```bash
python manage.py dumpdata polls.Question polls.Choice --indent 2 > polls/fixtures/polls.json
```

## License

This project is licensed for **educational and portfolio review purposes only**.  
Commercial or personal use, distribution, or modification is **not permitted**.

See the [LICENSE](./LICENSE) file for more details.