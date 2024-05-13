from flask import Flask, request, render_template
from src.scraper import scraper
from src.calculadora import DatosCalculadora

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/calculadora', methods=['POST'])
def calculadora():
    url=request.form['url']
    scrape = scraper(url)
    datos = DatosCalculadora(scrape[0], scrape[1], scrape[2])
    return render_template('calculadora.html', url=url, datos=datos)

if __name__=='__main__':
    # app.run(host='0.0.0.0',debug=True)
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)