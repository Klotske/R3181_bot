from flask import Flask, request, json
import json as js
import telegram, settings, vk_api, tg_api

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World"