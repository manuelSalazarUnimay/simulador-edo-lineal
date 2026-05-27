# Simulador de Ecuación Diferencial Lineal – Producción y Decaimiento del Yodo-131

## 📘 Descripción del proyecto

Este proyecto implementa un simulador matemático para resolver y analizar una **ecuación diferencial lineal de primer orden no homogénea**, aplicada al estudio de la **producción y decaimiento radiactivo del Yodo-131 (I-131)**.

El fenómeno modela un sistema donde existe:

- **Producción constante** de material radiactivo.
- **Decaimiento proporcional** a la cantidad presente.

Este comportamiento permite representar un problema real de medicina nuclear mediante herramientas matemáticas y computacionales. El modelo describe cómo cambia la cantidad de Yodo-131 en el tiempo hasta alcanzar un estado de equilibrio. 

---

## 🎯 Objetivo

Desarrollar una aplicación capaz de:

- Resolver paso a paso una **ecuación diferencial lineal no homogénea de primer orden**.
- Modelar matemáticamente la acumulación y desintegración del **Yodo-131**.
- Calcular la evolución temporal de la sustancia bajo una producción constante.
- Analizar el comportamiento del sistema hasta su **estado estacionario**.
- Visualizar resultados numéricos y gráficos del fenómeno. 

---

## ⚙️ Modelo matemático

El sistema estudiado se modela mediante la ecuación diferencial:

dQ/dt+P(t)Q=f(t)

Donde:

- **Q(t)** → Cantidad de Yodo-131 en el tiempo.
- **a** → Producción constante de material.
- **kQ** → Decaimiento radiactivo proporcional a la cantidad presente.
- **k** → Constante de desintegración radiactiva.

El modelo corresponde a una **ecuación diferencial lineal de primer orden no homogénea**, cuya solución permite estudiar tanto el comportamiento transitorio como el equilibrio del sistema.

---

## 🧠 ¿Qué hace el código?

La aplicación realiza el proceso completo de resolución de la ecuación diferencial:

1. **Plantea el modelo matemático** del problema.
2. **Calcula la constante de decaimiento** usando la vida media del Yodo-131.
3. **Resuelve simbólicamente** la ecuación diferencial.
4. **Aplica condiciones iniciales**.
5. **Obtiene la solución particular del sistema**.
6. **Evalúa resultados numéricos** en tiempos específicos.
7. **Calcula el estado estacionario** cuando \(t \to \infty\).
8. **Genera visualizaciones gráficas** del comportamiento temporal del sistema. 

---

## 📈 Resultados del modelo

El simulador permite obtener resultados como:

- Constante de decaimiento:

k=0.08642 〖días〗^(-1)

- Cantidad aproximada de Yodo-131 después de **24 días**:

Q(24)=20.23 gramos

- Valor de equilibrio del sistema:

Q_∞=  a/k=23.14 gramos

Esto demuestra cómo la producción y el decaimiento terminan equilibrándose con el paso del tiempo. 

---

## 🛠️ Tecnologías utilizadas

#front-end
- HTML5 & CSS3
- JavaScript
- Plotly.js
- KaTeX

#back-end
- Python
- SymPy (matemática simbólica)
- NumPy
- Matplotlib
- Flask 

---

## 🚀 Ejecución del proyecto

Clonar el repositorio:

```bash
git clone git@github.com:manuelSalazarUnimay/simulador-edo-lineal.git

#Ingresar al proyecto:
cd simulador-edo-lineal

#Ejecutar:
py api.py || python api.py

