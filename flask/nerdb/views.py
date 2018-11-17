from .models import Character, Corporation, Alliance
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/character/<character_id>')
def character(character_id):
    character = Character(character_id, True)
    return render_template('character.html', character=character)

@app.route('/corporation/<corporation_id>')
def corporation(corporation_id):
    corporation = Corporation(corporation_id)
    return render_template('corporation.html', corporation=corporation)

@app.route('/alliance/<alliance_id>')
def alliance(alliance_id):
    alliance = Alliance(alliance_id)
    return render_template('alliance.html', alliance=alliance)
