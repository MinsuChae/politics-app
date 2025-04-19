from flask import render_template
import json

with open('data/sample_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def index():
    return render_template('index.html', parties=data["parties"])