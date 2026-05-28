from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import json
import pandas as pd

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

    dq_evaluacion = float(np.asarray(simulador.dQ_dt_func(simulador.dia_evaluacion)).item())

    # Preparar trazados de gráficas
    t_fino = np.linspace(0, simulador.dias_simulacion, 500)
    q_fino = simulador.Q_num_func(t_fino).tolist()
    dq_fino = [float(simulador.dQ_dt_func(t)) for t in t_fino]
    t_lista = t_fino.tolist()
    #aañde horas a la grafica 2D
    # 1. Creamos una fecha "base" ficticia (ej. 1 de Enero) para simular el inicio
    fecha_base = pd.to_datetime("2024-01-01 00:00:00")

    # 2. Convertimos tu lista de días numéricos a un formato de tiempo real.
    # Si t = 1.5 días, esto lo convierte automáticamente al 2 de Enero a las 12:00 PM.
    t_dinamico = fecha_base + pd.to_timedelta(t_lista, unit='D')

    # Gráfica 2D
    """fig2d = go.Figure()
    fig2d.add_trace(go.Scatter(x=t_lista, y=q_fino, mode='lines', name='Masa Q(t)', line=dict(color='#0a4e7a', width=3)))
    fig2d.add_trace(go.Scatter(x=t_lista, y=dq_fino, mode='lines', name='Tasa dQ/dt', line=dict(color='#1b7835', width=3)))
    fig2d.update_layout(title='Dinámica del Sistema', xaxis_title='Días', template='plotly_white')"""
    # Gráfica 2D
# Eje de tiempo dinámico
    fecha_base = pd.to_datetime("2024-01-01 00:00:00")
    t_dinamico = fecha_base + pd.to_timedelta(t_lista, unit='D')
    fecha_evaluacion = fecha_base + pd.to_timedelta(simulador.dia_evaluacion, unit='D')


    # Gráfica 2D
    fig2d = go.Figure()
    fig2d.add_trace(go.Scatter(x=t_dinamico, y=q_fino, mode='lines', name='Masa Q(t)', line=dict(color='#0a4e7a', width=3)))
    fig2d.add_trace(go.Scatter(x=t_dinamico, y=dq_fino, mode='lines', name='Tasa dQ/dt', line=dict(color='#1b7835', width=3)))
    
    # =========================================================================
    # NUEVAS ADICIONES: LÍNEA DE EQUILIBRIO Y PUNTO DE EVALUACIÓN
    # =========================================================================
    
    # 1. Añadir línea roja horizontal para el Punto de Equilibrio
    fig2d.add_hline(
        y=saturacion, 
        line_dash="dash",       # Hace que la línea sea discontinua/punteada
        line_color="red",       # Línea roja
        line_width=2,
        annotation_text=f"Equilibrio ({round(saturacion, 2)})", # Texto de ayuda en la línea
        annotation_position="bottom right"
    )

    # 2. Convertir el día de evaluación (ej. 24) a la fecha correspondiente del eje X
    fecha_evaluacion = fecha_base + pd.to_timedelta(simulador.dia_evaluacion, unit='D')

    # 3. Añadir el punto exacto donde se encuentra el sistema ese día
    fig2d.add_trace(go.Scatter(
        x=[fecha_evaluacion],
        y=[masa],
        mode='markers+text',    # Dibuja el marcador y además una etiqueta de texto
        name=f'Evaluación (Día {simulador.dia_evaluacion})',
        marker=dict(
            color='#e65c00',    # Color naranja llamativo
            size=12,            # Tamaño grande para que resalte
            symbol='diamond'    # Forma de diamante
        ),
        text=[f"Día {simulador.dia_evaluacion}: {round(masa, 2)}"], # Texto que aparecerá junto al punto
        textposition="top center"                                    # Posición del texto sobre el punto
    ))
    
    # =========================================================================

    fig2d.update_layout(
        title='Dinámica del Sistema (Zoom Inteligente)', 
        xaxis_title='Tiempo', 
        template='plotly_white'
    )
    
    fig2d.update_xaxes(
        tickformatstops=[
            dict(dtickrange=[None, 86400000], value="%H:%M horas"),
            dict(dtickrange=[86400000, None], value="Día %d")    
        ]
    )

# =========================================================================
    # CONSTRUCCIÓN DE LA GRÁFICA 3D (BLINDADA CONTRA ERRORES DE TIPADO)
    # =========================================================================
    fig3d = go.Figure()

    # 1. Trayectoria continua
    fig3d.add_trace(go.Scatter3d(
        x=t_lista, 
        y=q_fino, 
        z=dq_fino, 
        mode='lines', 
        name='Trayectoria',
        line=dict(color=q_fino, colorscale='Turbid', width=5)
    ))

    # 2. Línea de Equilibrio (Valores numéricos puros en listas estándares)
    fig3d.add_trace(go.Scatter3d(
        x=[0.0, float(simulador.dias_simulacion)],  
        y=[saturacion, saturacion],        
        z=[0.0, 0.0],                          
        mode='lines',
        name='Línea de Equilibrio',
        line=dict(color='red', width=4)
    ))

    # 3. Punto de evaluación (Aseguramos colecciones con datos primitivos float)
    fig3d.add_trace(go.Scatter3d(
        x=[float(simulador.dia_evaluacion)],
        y=[masa],
        z=[dq_evaluacion],
        mode='markers+text',
        name=f'Evaluación (Día {simulador.dia_evaluacion})',
        marker=dict(color='#e65c00', size=8, symbol='diamond'),
        text=[f"Día {simulador.dia_evaluacion}"],
        textposition="top center"
    ))

    fig3d.update_layout(
        title='Espacio de Fases 3D', 
        scene=dict(
            xaxis_title='Tiempo (Días)', 
            yaxis_title='Q(t) (Masa)', 
            zaxis_title='dQ/dt (Tasa)'
        ), 
        template='plotly_white'
    )
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