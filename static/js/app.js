const form = document.getElementById('simulatorForm');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Captura de datos desde la UI usando los IDs del index original
    const parametros = {
        a_val: parseFloat(document.getElementById('produccion').value),
        vida_media: parseFloat(document.getElementById('vidaMedia').value),
        q_inicial: parseFloat(document.getElementById('cantidadInicial').value),
        dias_simulacion: parseInt(document.getElementById('diasSimulacion').value),
        dia_evaluacion: parseFloat(document.getElementById('diaEvaluacion').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/simular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(parametros)
        });

        if (!response.ok) throw new Error('Error en la respuesta del servidor API.');
        
        const data = await response.json();

        // 1. Inyección de valores numéricos en las tarjetas de estado
        document.getElementById('masaResultado').textContent = `${data.masa} g`;
        document.getElementById('saturacionResultado').textContent = `${data.saturacion} g`;

        // 2. Renderizado Analítico de Ecuaciones (KaTeX en modo display)
        const pasos = data.pasos_latex;
        
        katex.render(pasos.paso1_simb, document.getElementById('p1_simb'), { displayMode: true });
        katex.render(pasos.paso1_num, document.getElementById('p1_num'), { displayMode: true });
        
        katex.render(pasos.paso2_simb, document.getElementById('p2_simb'), { displayMode: true });
        katex.render(pasos.paso2_num, document.getElementById('p2_num'), { displayMode: true });
        
        katex.render(pasos.paso3_simb, document.getElementById('p3_simb'), { displayMode: true });
        katex.render(pasos.paso3_num, document.getElementById('p3_num'), { displayMode: true });
        
        katex.render(pasos.paso4_simb, document.getElementById('p4_simb'), { displayMode: true });
        katex.render(pasos.paso4_num, document.getElementById('p4_num'), { displayMode: true });
        
        katex.render(pasos.paso5_simb, document.getElementById('p5_simb'), { displayMode: true });
        katex.render(pasos.paso5_c, document.getElementById('p5_c'), { displayMode: true });
        katex.render(pasos.paso5_num, document.getElementById('p5_num'), { displayMode: true });
        
        katex.render(pasos.paso6_simb, document.getElementById('p6_simb'), { displayMode: true });
        katex.render(pasos.paso6_num, document.getElementById('p6_num'), { displayMode: true });

        // 3. Renderizado de Gráficos Interactivos de Plotly
        Plotly.newPlot('plot2dCanvas', data.grafica2d.data, data.grafica2d.layout, { responsive: true });
        Plotly.newPlot('plot3dCanvas', data.grafica3d.data, data.grafica3d.layout, { responsive: true });

    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al procesar la simulación o al renderizar las fórmulas matemáticas.');
    }
});