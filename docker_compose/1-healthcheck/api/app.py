# 0-first_stack/api/app.py
from flask import Flask, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app) 

cache = redis.Redis(host='db', port=6379)

@app.route('/api')
def hello():
    # Incrémente le compteur dans Redis à chaque appel
    count = cache.incr('hits')
    return jsonify({"message": "Hello from the Python API!", "hits": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)