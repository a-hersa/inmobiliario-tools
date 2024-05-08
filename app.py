from flask import Flask, request, render_template
from src.scraper import scraper

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/calculadora', methods=['GET','POST'])
def calculadora():
    if request.method=='GET': 
        return render_template('calculadora.html')

    else:
        url=request.form['url']
        datos = scraper(url)
        return render_template('calculadora.html', url=url, datos=datos)

if __name__=='__main__':
    # app.run(host='0.0.0.0',debug=True)
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)