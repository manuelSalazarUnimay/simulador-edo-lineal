import numpy as np
import sympy as sp

class SimuladorEDOLineal:
    def __init__(self):
        """Variables de estado iniciales"""
        self.a_val = 2.0
        self.vida_media = 8.02
        self.q_inicial = 0.0
        self.dias_simulacion = 80
        self.dia_evaluacion = 24.0
        
        self.k_val = 0.0
        self.Q_num_func = None
        self.dQ_dt_func = None
        self.Q_equilibrio = 0.0
        self.pasos_latex = {}  # Almacén de ecuaciones seguras para JSON

    def fase_2_motor_matematico(self):
        """Motor SymPy libre de errores de tipado y optimizado para transporte Web"""
        # 1. Cálculo de constante de decaimiento
        self.k_val = float(np.log(2) / self.vida_media)
        
        # 2. Configuración de símbolos algebraicos (Inmune a advertencias de linters)
        t = sp.Symbol('t', real=True, nonnegative=True)
        Q = sp.symbols('Q', cls=sp.Function)
        a_sym, k_sym = sp.symbols('a k', real=True, positive=True)
        C = sp.Symbol('C', real=True)
        mu_sym = sp.Symbol(r'\mu(t)')  # Uso de raw-string para evitar conflictos
        
        # --- DESARROLLO ANALÍTICO PASO A PASO ---
        # Paso 1: Forma Estándar
        forma_estandar = sp.Eq(Q(t).diff(t) + k_sym * Q(t), a_sym)
        
        # Paso 2: Factor Integrante
        mu = sp.exp(k_sym * t)
        
        # Paso 3: Multiplicación (Derivada del producto)
        derivada_producto = sp.Derivative(Q(t) * mu, t)
        edo_factor_integrante = sp.Eq(derivada_producto, a_sym * mu)
        
        # Paso 4: Integración y Solución General
        integral_rhs = (a_sym / k_sym) * mu + C
        solucion_general = sp.Eq(Q(t), (integral_rhs / mu).expand())
        
        # Paso 5: Condición Inicial y Solución Particular
        eq_C = sp.Eq(self.q_inicial, solucion_general.rhs.subs(t, 0))
        C_val = sp.solve(eq_C, C)[0]
        solucion_particular_simb = solucion_general.subs(C, C_val)
        
        # Ejecución numérica para vectores NumPy
        solucion_particular_num = solucion_particular_simb.subs({a_sym: self.a_val, k_sym: self.k_val})
        self.Q_num_func = sp.lambdify(t, solucion_particular_num.rhs, 'numpy')
        self.dQ_dt_func = lambda t_val: self.a_val - self.k_val * self.Q_num_func(t_val)
        self.Q_equilibrio = self.a_val / self.k_val
        
        # --- EXTRACCIÓN DE FÓRMULAS USANDO STRINGS CRUDOS (PREVIENE DAÑOS POR \t o \f) ---
        valores_num = {a_sym: round(self.a_val, 4), k_sym: round(self.k_val, 5)}
        
        edo_paso3_num = sp.Eq(
            sp.Derivative(Q(t) * sp.exp(round(self.k_val, 5) * t), t), 
            round(self.a_val, 4) * sp.exp(round(self.k_val, 5) * t)
        )
        
        C_evaluado = float(C_val.subs(valores_num))
        solucion_particular_num_limpia = solucion_particular_simb.subs(valores_num).expand()

        # Compilación explícita a cadenas de texto LaTeX puras
        self.pasos_latex = {
            'paso1_simb': str(sp.latex(forma_estandar)),
            'paso1_num': str(sp.latex(forma_estandar.subs(valores_num))),
            'paso2_simb': str(sp.latex(sp.Eq(mu_sym, mu))),
            'paso2_num': str(sp.latex(sp.Eq(mu_sym, mu.subs(valores_num)))),
            'paso3_simb': str(sp.latex(edo_factor_integrante)),
            'paso3_num': str(sp.latex(edo_paso3_num)),
            'paso4_simb': str(sp.latex(solucion_general)),
            'paso4_num': str(sp.latex(solucion_general.subs(valores_num))),
            'paso5_simb': str(sp.latex(solucion_particular_simb)),
            'paso5_c': str(sp.latex(sp.Eq(C, round(C_evaluado, 5)))),
            'paso5_num': str(sp.latex(solucion_particular_num_limpia)),
            'paso6_simb': r'\lim_{t \to \infty} Q(t) = \frac{a}{k}',
            'paso6_num': r'Q_\infty = ' + f'{self.Q_equilibrio:.4f}' + r'\text{ gramos}'
        }
        
        return self.pasos_latex  # Soluciona el error de asignación sin retorno