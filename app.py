# app.py

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
incidents = []
incident_id_counter = 1

@app.route('/')
def index():
    """Ruta principal: Muestra la lista de incidencias."""
    return render_template('index.html', incidents=incidents)

@app.route('/report', methods=['GET', 'POST'])
def report_incident():
    """Ruta para reportar una nueva incidencia."""
    global incident_id_counter
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        new_incident = {
            'id': incident_id_counter,
            'title': title,
            'description': description,
            'status': 'Abierto',
            'change_id': None, # Vinculación con ANSI–EIA–649 (CM)
            'source_code_file': 'app.py', # Vinculación con ISO/IEC 12207 (Mantenimiento y Trazabilidad)
            'commit_hash': None,
            'resolution_time_days': None # Métrica de mantenimiento (ISO 12207)
        }
        incidents.append(new_incident)
        incident_id_counter += 1
        return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/vulnerable_search')
def vulnerable_search():
    """Punto de control: Simula una función que podría ser marcada por SAST."""
    user_input = request.args.get('query', '')
    results = [i for i in incidents if user_input.lower() in i['title'].lower() or user_input.lower() in i['description'].lower()]
    return render_template('search_results.html', results=results, query=user_input)

if __name__ == '__main__':
    app.run(debug=True)