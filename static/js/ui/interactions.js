// ==========================
// PANEL DERECHO PRINCIPAL
// ==========================
const btnMotor = document.getElementById("btnMotor");
const btnGraficas = document.getElementById("btnGraficas");

const panelMotor = document.getElementById("panelMotor");
const panelGraficas = document.getElementById("panelGraficas");

btnMotor?.addEventListener("click", () => {

    panelMotor.classList.remove("hidden");
    panelGraficas.classList.add("hidden");

    btnMotor.classList.add("bg-blue-600", "text-white");
    btnMotor.classList.remove("bg-slate-100");

    btnGraficas.classList.remove("bg-blue-600", "text-white");
    btnGraficas.classList.add("bg-slate-100");
});

btnGraficas?.addEventListener("click", () => {

    panelGraficas.classList.remove("hidden");
    panelMotor.classList.add("hidden");

    btnGraficas.classList.add("bg-blue-600", "text-white");
    btnGraficas.classList.remove("bg-slate-100");

    btnMotor.classList.remove("bg-blue-600", "text-white");
    btnMotor.classList.add("bg-slate-100");
});


// ==========================
// VISUALIZACIÓN DINÁMICA
// ==========================
const btn2D = document.getElementById("btn2D");
const btn3D = document.getElementById("btn3D");

const container2D = document.getElementById("container2D");
const container3D = document.getElementById("container3D");

btn2D?.addEventListener("click", () => {

    // Mostrar 2D
    container2D.classList.remove("hidden");
    container3D.classList.add("hidden");

    // Estado visual botones
    btn2D.classList.add("bg-blue-600", "text-white");
    btn2D.classList.remove("bg-slate-100");

    btn3D.classList.remove("bg-blue-600", "text-white");
    btn3D.classList.add("bg-slate-100");

    // Reajustar tamaño Plotly
    setTimeout(() => {
        Plotly.Plots.resize("plot2dCanvas");
        Plotly.Plots.resize("plot3dCanvas");
    }, 100);
});


btn3D?.addEventListener("click", () => {

    // Mostrar 3D
    container3D.classList.remove("hidden");
    container2D.classList.add("hidden");

    // Estado visual botones
    btn3D.classList.add("bg-blue-600", "text-white");
    btn3D.classList.remove("bg-slate-100");

    btn2D.classList.remove("bg-blue-600", "text-white");
    btn2D.classList.add("bg-slate-100");

    // Reajustar tamaño Plotly
    setTimeout(() => {
        Plotly.Plots.resize("plot2dCanvas");
        Plotly.Plots.resize("plot3dCanvas");
    }, 100);
});

btnGraficas?.addEventListener("click", () => {

    panelGraficas.classList.remove("hidden");
    panelMotor.classList.add("hidden");

    btnGraficas.classList.add("bg-blue-600", "text-white");
    btnGraficas.classList.remove("bg-slate-100");

    btnMotor.classList.remove("bg-blue-600", "text-white");
    btnMotor.classList.add("bg-slate-100");

    // Recalcular tamaño Plotly
    setTimeout(() => {
        Plotly.Plots.resize("plot2dCanvas");
        Plotly.Plots.resize("plot3dCanvas");
    }, 100);
});