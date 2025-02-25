#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, render_template, make_response, send_from_directory
from flask import redirect, request, jsonify, url_for

from imagehandler import PictoImageHandler
from interface import PictoInterface
from language import PictoLanguage
from card import PictoCard


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.debug = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index2.html')

@app.route('/editor', methods=['GET'])
def editor():
    return render_template('editor.html')


@app.route('/textpost', methods = ['POST'])
def post_text():
    text = request.form['text']
    cards = interface.get_cards(text)
    cards_json = []
    for c in cards:
        print(c.to_json())
        cards_json.append(c.to_json())
    
    return jsonify({'cards': cards_json})


@app.route('/generate/img', methods = ['POST'])
def get_img():
    cards_get = request.form['info']
    cards = []
    for c in cards_get:
        cards.append(PictoCard(c))
    
    file = interface.to_img(cards)
    return send_from_directory("/static/generated", filename=file, as_attachment=True)


@app.route('/generate/zip', methods = ['POST'])
def get_zip():
    cards_get = request.form['info']
    cards = []
    for c in cards_get:
        cards.append(PictoCard(c))
    
    file = interface.to_img(cards)
    return send_from_directory("/static/generated", filename=file, as_attachment=True)

@app.route('/generate/test')
def get_test():
    print("Method entered")
    return send_from_directory("/static/color", filename="¿.png", as_attachment=True)


if __name__ == '__main__':
    image_handler = PictoImageHandler(
        font = "./static/escolar_bold.ttf",
        text_size = 90,
        card_dimensions = (600,750),
        image_margin = 50
    )
    print("Starting language toolkit...")
    language = PictoLanguage()
    print("Language toolkit started")
    interface = PictoInterface(language, image_handler)
    app.run(host='0.0.0.0', port=5000)
