# app.py
from flask import Flask
import redis

app = Flask(__name__)

# Configuração do Redis
r = redis.Redis(host='localhost', port=6379, db=0)
