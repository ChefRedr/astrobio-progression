from flask import Flask

app = Flask(__name__)

@app.route('/api/health')
def get_current_time():
    return {'health': 200}

@app.route('/api/')