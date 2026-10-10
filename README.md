# Tablero de Control e Indicadores Financieros - Empresa Andina S.A.

Dashboard ejecutivo interactivo desarrollado con **Python**, **Streamlit** y **Plotly** para el análisis, diagnóstico y visualización de la salud financiera de la **Empresa Andina S.A.** durante el periodo 2021 – 2025.

---

## 📌 Contenido y Funcionalidades

1. **🌟 Resumen Ejecutivo:**
   - KPIs clave: Ingresos Totales, EBITDA, Utilidad Neta, ROE, Flujo de Operación (CFO).
   - Tendencias anuales de ventas vs. márgenes operativos.
   - Diagnóstico automatizado del analista financiero.

2. **📈 Rentabilidad y Modelo DuPont:**
   - Cascada de Resultados (Gráfico Waterfall de ingresos a utilidad neta).
   - Descomposición DuPont de 3 factores (Margen Neto × Rotación de Activos × Multiplicador de Capital).

3. **💧 Liquidez y Capital de Trabajo:**
   - Razón Corriente y Prueba Ácida frente a umbrales de seguridad.
   - Capital de Trabajo Neto (KTNO) y desglose de la estructura del Activo Corriente.

4. **⚖️ Endeudamiento y Solvencia:**
   - Apalancamiento financiero (D/E) y nivel de endeudamiento sobre activos.
   - Ratio de cobertura de intereses (EBIT / Gastos Financieros).

5. **💵 Flujo de Caja:**
   - Desglose por actividades: Operación (CFO), Inversión / CAPEX (CFI) y Financiación / Dividendos (CFF).
   - Evolución de la posición de caja y equivalentes.

6. **📑 Estados Financieros Detallados:**
   - Tablas completas auditables del Balance General, Estado de Resultados, Flujo de Efectivo y Matriz de Ratios.

---

## 🚀 Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/mariaaliciaparraguzman-ops/andina-finanzas.git
cd andina-finanzas
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Levantar la aplicación
```bash
streamlit run app.py
```
Accede en tu navegador a: `http://localhost:8501`
