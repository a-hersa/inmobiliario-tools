from flask import Flask, send_file, request, render_template
from src.scraper import scraper
from src.calculadora import DatosCalculadora
import tempfile
from openpyxl import load_workbook
from dotenv import load_dotenv

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/calculadora', methods=['POST'])
def calculadora():
    url=request.form['url']
    scrape = scraper(url)
    datos = DatosCalculadora(scrape[0], scrape[1], scrape[2], scrape[3])
    return render_template('calculadora.html', url=url, datos=datos)

@app.route('/descargar', methods=['POST'])
def descargar():
    wb = load_workbook('src/plantilla.xlsx')
    ws = wb.active
    ws['D5'] = request.form['nombre']
    ws['D6'] = request.form['url']
    ws['D10'] = int(request.form['p_compra'])
    ws['D11'] = int(request.form['itp'])
    ws['D12'] = int(request.form['reforma'])
    ws['D13'] = int(request.form['notaria'])
    ws['D14'] = int(request.form['registro'])
    ws['D15'] = int(request.form['agencia'])
    ws['D16'] = int(request.form['tasacion'])
    ws['E20'] = int(request.form['ibi'])
    ws['E21'] = int(request.form['basuras'])
    ws['E22'] = int(request.form['comunidad'])
    ws['E23'] = int(request.form['seguros'])
    ws['E24'] = 0
    ws['H5'] = int(request.form['alquiler'])
    ws['H8'] = float(float(request.form['financiado'])/100)
    ws['H11'] = int(request.form['plazo'])
    ws['H12'] = float(float(request.form['intereses_anuales'])/100)
    temp_excel_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    wb.save(temp_excel_file.name)
    # path = "src/plantilla.xlsx"
    return send_file(temp_excel_file.name, as_attachment=True)

if __name__=='__main__':
    load_dotenv()
    # app.run(host='0.0.0.0',debug=True)
    # app.run(host='0.0.0.0',port=8080)
    app.run(debug = False, host='0.0.0.0', port=5000)