# Setup instructions

## Create venv, activate and install dependencies:

1. cd into `/api`
2. `python -m venv .venv`
3. `pip install -r requirements.txt`
4. `source .venv/Scripts/activate`
5. run `flask run` to activate flask
   - You can verify it's running by doing a GET request to `http://127.0.0.1:5000/api/health` => should return 200 ok