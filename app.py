from flask import Flask, request, render_template

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/calculadora', methods=['GET','POST'])
def calculadora():
    if request.method=='GET': 
        return render_template('form.html')

    else:
        url=request.form['url']
        itp=int(int(50000)*0.1)
        return render_template('calculadora.html', itp=itp)

if __name__=='__main__':
    # app.run(host='0.0.0.0',debug=True)
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug=True)