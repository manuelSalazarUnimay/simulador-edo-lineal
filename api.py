from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import json

from backend import SimuladorEDOLineal

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/simular', methods=['POST'])
def simular():
    datos = request.json
    simulador = SimuladorEDOLineal()

    simulador.a_val = float(datos.get('a_val', 2.0))
    simulador.vida_media = float(datos.get('vida_media', 8.02))
    simulador.q_inicial = float(datos.get('q_inicial', 0.0))
    simulador.dias_simulacion = int(datos.get('dias_simulacion', 80))
    simulador.dia_evaluacion = float(datos.get('dia_evaluacion', 24.0))

    # Computar motor analítico
    simulador.fase_2_motor_matematico()

    masa = float(simulador.Q_num_func(simulador.dia_evaluacion))
    saturacion = float(simulador.Q_equilibrio)

    # Preparar trazados de gráficas
    t_fino = np.linspace(0, simulador.dias_simulacion, 500)
    q_fino = simulador.Q_num_func(t_fino).tolist()
    dq_fino = [float(simulador.dQ_dt_func(t)) for t in t_fino]
    t_lista = t_fino.tolist()

    # Gráfica 2D
    fig2d = go.Figure()
    fig2d.add_trace(go.Scatter(x=t_lista, y=q_fino, mode='lines', name='Masa Q(t)', line=dict(color='#0a4e7a', width=3)))
    fig2d.add_trace(go.Scatter(x=t_lista, y=dq_fino, mode='lines', name='Tasa dQ/dt', line=dict(color='#1b7835', width=3)))
    fig2d.update_layout(title='Dinámica del Sistema', xaxis_title='Días', template='plotly_white')

    # Gráfica 3D
    fig3d = go.Figure(data=[go.Scatter3d(x=t_lista, y=q_fino, z=dq_fino, mode='lines', line=dict(color=q_fino, colorscale='Turbid', width=5))])
    fig3d.update_layout(title='Espacio de Fases 3D', scene=dict(xaxis_title='Tiempo', yaxis_title='Q(t)', zaxis_title='dQ/dt'), template='plotly_white')

    # Retornar datos numéricos, gráficos e informe matemático completo
    return jsonify({
        'masa': round(masa, 4),
        'saturacion': round(saturacion, 4),
        'pasos_latex': simulador.pasos_latex,
        'grafica2d': json.loads(pio.to_json(fig2d)),
        'grafica3d': json.loads(pio.to_json(fig3d))
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)