import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="Tablero Financiero Andina",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #1E88E5;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .metric-delta-pos {
        color: #2e7d32;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .metric-delta-neg {
        color: #d32f2f;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0D47A1;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #546e7a;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Cargar y estructurar datos directamente
@st.cache_data
def get_data():
    years = [2021, 2022, 2023, 2024, 2025]
    
    # 1. Balance General (en miles de $)
    bg_data = {
        'Efectivo': [740, 3233, 5866, 8882, 12450],
        'Cuentas por Cobrar': [10959, 11573, 12225, 13315, 14137],
        'Inventarios': [10685, 11392, 12358, 13315, 14301],
        'Otros Activos Corrientes': [1200, 1200, 1200, 1200, 1200],
        'Activo Corriente': [23584, 27398, 31649, 36712, 42088],
        'Propiedad Planta y Equipo': [13300, 14800, 16400, 18100, 20000],
        'Intangibles': [1500, 1500, 1500, 1500, 1500],
        'Total Activos': [38384, 43698, 49549, 56312, 63588],
        
        'Deuda CP': [4385, 4905, 5483, 6048, 6615],
        'Proveedores': [6575, 7595, 8571, 9986, 11096],
        'Otras Cuentas por Pagar': [1043, 1119, 1203, 1296, 1392],
        'Impuestos por Pagar': [256, 306, 376, 468, 573],
        'Pasivo Corriente': [12259, 13925, 15633, 17798, 19676],
        'Deuda LP': [8143, 9109, 10183, 11232, 12285],
        'Total Pasivos': [20402, 23034, 25816, 29030, 31961],
        
        'Capital Social': [10000, 10000, 10000, 10000, 10000],
        'Reservas': [2000, 2000, 2000, 2000, 2000],
        'Resultados Acumulados': [5982, 8664, 11733, 15282, 19627],
        'Total Patrimonio': [17982, 20664, 23733, 27282, 31627]
    }
    df_bg = pd.DataFrame(bg_data, index=years)
    
    # 2. Estado de Resultados (en miles de $)
    er_data = {
        'Ventas': [80000, 88000, 97000, 108000, 120000],
        'Costo Ventas': [60000, 66000, 72750, 81000, 90000],
        'Utilidad Bruta': [20000, 22000, 24250, 27000, 30000],
        'Gastos Admin': [6000, 6424, 6887, 7344, 7800],
        'Gastos Ventas': [7040, 7568, 8148, 8856, 9600],
        'Depreciacion': [1200, 1300, 1400, 1500, 1600],
        'EBIT': [5760, 6708, 7815, 9300, 11000],
        'Gastos Financieros': [1500, 1600, 1550, 1500, 1450],
        'UAI': [4260, 5108, 6265, 7800, 9550],
        'Impuestos': [1278, 1532, 1880, 2340, 2865],
        'Utilidad Neta': [2982, 3576, 4385, 5460, 6685]
    }
    df_er = pd.DataFrame(er_data, index=years)
    
    # 3. Flujo de Efectivo (en miles de $)
    fe_data = {
        'CFO': [2212, 4701, 5297, 6513, 7788],
        'CAPEX': [-2500, -2800, -3000, -3200, -3500],
        'CFI': [-2500, -2800, -3000, -3200, -3500],
        'Financiamiento Neto': [-1472, 1486, 1652, 1614, 1620],
        'Dividendos': [0, -894, -1316, -1911, -2340],
        'CFF': [-1472, 592, 336, -297, -720],
        'Flujo Neto': [-1760, 2493, 2633, 3016, 3568],
        'Saldo Inicial': [2500, 740, 3233, 5866, 8882],
        'Saldo Final': [740, 3233, 5866, 8882, 12450]
    }
    df_fe = pd.DataFrame(fe_data, index=years)
    
    # Ratios Financieros
    df_ratios = pd.DataFrame(index=years)
    # Liquidez
    df_ratios['Razon Corriente'] = df_bg['Activo Corriente'] / df_bg['Pasivo Corriente']
    df_ratios['Prueba Acida'] = (df_bg['Activo Corriente'] - df_bg['Inventarios']) / df_bg['Pasivo Corriente']
    df_ratios['Capital de Trabajo'] = df_bg['Activo Corriente'] - df_bg['Pasivo Corriente']
    # Rentabilidad
    df_ratios['Margen Bruto (%)'] = (df_er['Utilidad Bruta'] / df_er['Ventas']) * 100
    df_ratios['Margen Operacional (%)'] = (df_er['EBIT'] / df_er['Ventas']) * 100
    df_ratios['Margen Neto (%)'] = (df_er['Utilidad Neta'] / df_er['Ventas']) * 100
    df_ratios['ROA (%)'] = (df_er['Utilidad Neta'] / df_bg['Total Activos']) * 100
    df_ratios['ROE (%)'] = (df_er['Utilidad Neta'] / df_bg['Total Patrimonio']) * 100
    # Endeudamiento
    df_ratios['Endeudamiento Total (%)'] = (df_bg['Total Pasivos'] / df_bg['Total Activos']) * 100
    df_ratios['Apalancamiento (D/E)'] = df_bg['Total Pasivos'] / df_bg['Total Patrimonio']
    df_ratios['Cobertura Intereses (x)'] = df_er['EBIT'] / df_er['Gastos Financieros']
    # Operación
    df_ratios['EBITDA'] = df_er['EBIT'] + df_er['Depreciacion']
    df_ratios['Margen EBITDA (%)'] = (df_ratios['EBITDA'] / df_er['Ventas']) * 100
    
    return df_bg, df_er, df_fe, df_ratios

df_bg, df_er, df_fe, df_ratios = get_data()

# SIDEBAR
st.sidebar.image("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=300&q=80", use_container_width=True)
st.sidebar.title("🏢 Empresa Andina S.A.")
st.sidebar.markdown("**Módulo de Control y Diagnóstico Financiero**")
st.sidebar.markdown("---")

selected_year = st.sidebar.select_slider(
    "Seleccionar Año para Análisis Detallado:",
    options=[2021, 2022, 2023, 2024, 2025],
    value=2025
)

tab_option = st.sidebar.radio(
    "Navegación:",
    ["🌟 Resumen Ejecutivo", "📈 Rentabilidad y Rendimiento", "💧 Liquidez y Capital de Trabajo", "⚖️ Endeudamiento y Solvencia", "💵 Flujos de Caja y Efectivo", "📑 Estados Detallados"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Auditoría y Modelado:**
- Moneda: Miles de USD / COP
- Periodo histórico: 2021 - 2025
- Métricas calculadas según NIIF / IFRS
""")

# ENCABEZADO
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="main-header">Tablero Integral de Indicadores Financieros</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Evaluación Financiera Multianual y Diagnóstico Estratégico | Año de Enfoque: <b>{selected_year}</b></div>', unsafe_allow_html=True)
with col_h2:
    st.metric(label="Crecimiento de Ventas (CAGR 21-25)", value="+10.67%", delta="Saludable")

# ================= TAB: RESUMEN EJECUTIVO =================
if tab_option == "🌟 Resumen Ejecutivo":
    prev_year = selected_year - 1 if selected_year > 2021 else 2021
    
    # Tarjetas Principales KPI
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    ventas_val = df_er.loc[selected_year, 'Ventas']
    ventas_delta = ((ventas_val / df_er.loc[prev_year, 'Ventas']) - 1) * 100 if selected_year > 2021 else 0
    kpi1.metric("Ingresos Totales", f"${ventas_val:,.0f}", f"{ventas_delta:+.1f}% vs {prev_year}")
    
    ebitda_val = df_ratios.loc[selected_year, 'EBITDA']
    ebitda_delta = ((ebitda_val / df_ratios.loc[prev_year, 'EBITDA']) - 1) * 100 if selected_year > 2021 else 0
    kpi2.metric("EBITDA Operativo", f"${ebitda_val:,.0f}", f"{ebitda_delta:+.1f}% vs {prev_year}")
    
    net_val = df_er.loc[selected_year, 'Utilidad Neta']
    net_delta = ((net_val / df_er.loc[prev_year, 'Utilidad Neta']) - 1) * 100 if selected_year > 2021 else 0
    kpi3.metric("Utilidad Neta", f"${net_val:,.0f}", f"{net_delta:+.1f}% vs {prev_year}")
    
    roe_val = df_ratios.loc[selected_year, 'ROE (%)']
    roe_prev = df_ratios.loc[prev_year, 'ROE (%)']
    kpi4.metric("ROE (Retorno Patrimonio)", f"{roe_val:.2f}%", f"{roe_val - roe_prev:+.2f} pts")
    
    cfo_val = df_fe.loc[selected_year, 'CFO']
    cfo_delta = ((cfo_val / df_fe.loc[prev_year, 'CFO']) - 1) * 100 if selected_year > 2021 else 0
    kpi5.metric("Flujo Operativo (CFO)", f"${cfo_val:,.0f}", f"{cfo_delta:+.1f}% vs {prev_year}")

    st.markdown("---")
    
    # Gráficos de tendencias primarias
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Evolución de Ingresos y Márgenes de Ganancia")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=df_er.index, y=df_er['Ventas'], name='Ventas Netas', marker_color='#1976D2', yaxis='y1'))
        fig1.add_trace(go.Scatter(x=df_er.index, y=df_ratios['Margen EBITDA (%)'], name='Margen EBITDA %', line=dict(color='#FF9800', width=3), yaxis='y2'))
        fig1.add_trace(go.Scatter(x=df_er.index, y=df_ratios['Margen Neto (%)'], name='Margen Neto %', line=dict(color='#4CAF50', width=3), yaxis='y2'))
        fig1.update_layout(
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Ventas (Miles de $)"),
            yaxis2=dict(title="Margen (%)", overlaying='y', side='right', ticksuffix="%"),
            height=380,
            margin=dict(l=10, r=10, t=30, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Evolución de Retorno sobre Capital (ROE vs ROA)")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios['ROE (%)'], name='ROE (%)', mode='lines+markers+text',
                                  text=[f"{v:.1f}%" for v in df_ratios['ROE (%)']], textposition='top center',
                                  line=dict(color='#7B1FA2', width=3)))
        fig2.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios['ROA (%)'], name='ROA (%)', mode='lines+markers+text',
                                  text=[f"{v:.1f}%" for v in df_ratios['ROA (%)']], textposition='bottom center',
                                  line=dict(color='#00897B', width=3)))
        fig2.update_layout(
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Porcentaje (%)", ticksuffix="%"),
            height=380,
            margin=dict(l=10, r=10, t=30, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Diagnóstico del Analista
    st.markdown("### 💡 Diagnóstico del Analista Financiero Senior")
    st.success(f"""
    - **Solidez Operativa:** Los ingresos crecieron de $80,000 en 2021 a $120,000 en 2025 (+50.0%), apalancados con un incremento del Margen Operacional del 7.2% al 9.2%.
    - **Apalancamiento Saludable:** El endeudamiento total se redujo del 53.15% en 2021 al 50.26% en 2025, mientras que la cobertura de intereses aumentó drásticamente de **3.84x a 7.59x**.
    - **Generación de Caja Robusta:** La caja y equivalentes saltó de **$740 a $12,450** gracias a un CFO sostenido que cubre con holgura el CAPEX anual (inversiones de planta por ~$3,500).
    """)

# ================= TAB: RENTABILIDAD =================
elif tab_option == "📈 Rentabilidad y Rendimiento":
    st.subheader("Análisis Integral de Rentabilidad y Descomposición Dupont")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Margen Bruto", f"{df_ratios.loc[selected_year, 'Margen Bruto (%)']:.1f}%", "Estable en 25%")
    col2.metric("Margen Operacional (EBIT)", f"{df_ratios.loc[selected_year, 'Margen Operacional (%)']:.2f}%", "+2.0 pts vs 2021")
    col3.metric("Margen Neto", f"{df_ratios.loc[selected_year, 'Margen Neto (%)']:.2f}%", "+1.8 pts vs 2021")
    col4.metric("EBITDA", f"${df_ratios.loc[selected_year, 'EBITDA']:,.0f}", f"{df_ratios.loc[selected_year, 'Margen EBITDA (%)']:.1f}% de las ventas")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Estructura de Cascada de Resultados (Año {})".format(selected_year))
        er_y = df_er.loc[selected_year]
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Resultados",
            orientation = "v",
            measure = ["relative", "relative", "total", "relative", "relative", "total", "relative", "relative", "total"],
            x = ["Ventas", "Costo Ventas", "Utilidad Bruta", "Gastos Admin", "Gastos Ventas", "EBIT", "Gastos Fin.", "Impuestos", "Utilidad Neta"],
            textposition = "outside",
            text = [f"${v/1000:.1f}k" for v in [er_y['Ventas'], -er_y['Costo Ventas'], er_y['Utilidad Bruta'], -er_y['Gastos Admin'], -er_y['Gastos Ventas'], er_y['EBIT'], -er_y['Gastos Financieros'], -er_y['Impuestos'], er_y['Utilidad Neta']]],
            y = [er_y['Ventas'], -er_y['Costo Ventas'], 0, -er_y['Gastos Admin'], -er_y['Gastos Ventas'], 0, -er_y['Gastos Financieros'], -er_y['Impuestos'], 0],
            connector = {"line":{"color":"#90A4AE"}},
            decreasing = {"marker":{"color":"#E53935"}},
            increasing = {"marker":{"color":"#1E88E5"}},
            totals = {"marker":{"color":"#43A047"}}
        ))
        fig_waterfall.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with c2:
        st.markdown("#### Análisis DuPont (Descomposición del ROE)")
        # Dupont: Margen Neto * Rotacion Activos * Multiplicador Capital
        dupont_df = pd.DataFrame(index=df_bg.index)
        dupont_df['Margen Neto'] = df_er['Utilidad Neta'] / df_er['Ventas']
        dupont_df['Rotacion Activos'] = df_er['Ventas'] / df_bg['Total Activos']
        dupont_df['Apalancamiento Fin.'] = df_bg['Total Activos'] / df_bg['Total Patrimonio']
        dupont_df['ROE Calculado (%)'] = dupont_df['Margen Neto'] * dupont_df['Rotacion Activos'] * dupont_df['Apalancamiento Fin.'] * 100
        
        fig_dup = go.Figure()
        fig_dup.add_trace(go.Scatter(x=dupont_df.index, y=dupont_df['Rotacion Activos'], name='Rotación Activos (Vtas/Activo)', line=dict(color='#3949AB', width=2.5)))
        fig_dup.add_trace(go.Scatter(x=dupont_df.index, y=dupont_df['Apalancamiento Fin.'], name='Multiplicador Apalancamiento (Activo/Pat)', line=dict(color='#E53935', width=2.5)))
        fig_dup.update_layout(
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Veces (x)"),
            height=420
        )
        st.plotly_chart(fig_dup, use_container_width=True)
        
        dy = dupont_df.loc[selected_year]
        st.caption(f"**Desglose DuPont ({selected_year}):** Margen Neto ({dy['Margen Neto']*100:.2f}%) × Rotación ({dy['Rotacion Activos']:.2f}x) × Multiplicador ({dy['Apalancamiento Fin.']:.2f}x) = **ROE {dy['ROE Calculado (%)']:.2f}%**")

# ================= TAB: LIQUIDEZ =================
elif tab_option == "💧 Liquidez y Capital de Trabajo":
    st.subheader("Diagnóstico de Liquidez y Gestión de Capital de Trabajo (KTNO)")
    
    col1, col2, col3, col4 = st.columns(4)
    cr = df_ratios.loc[selected_year, 'Razon Corriente']
    pa = df_ratios.loc[selected_year, 'Prueba Acida']
    wc = df_ratios.loc[selected_year, 'Capital de Trabajo']
    efectivo = df_bg.loc[selected_year, 'Efectivo']
    
    col1.metric("Razón Corriente", f"{cr:.2f}x", "Meta > 1.5x", delta_color="normal")
    col2.metric("Prueba Ácida", f"{pa:.2f}x", "Meta > 1.0x", delta_color="normal")
    col3.metric("Capital de Trabajo Neto", f"${wc:,.0f}", f"+${wc - df_ratios.loc[2021, 'Capital de Trabajo']:,.0f} vs 2021")
    col4.metric("Posición de Efectivo", f"${efectivo:,.0f}", "16.8x vs 2021")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Evolución de Indicadores de Solvencia Corto Plazo")
        fig_liq = go.Figure()
        fig_liq.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios['Razon Corriente'], name='Razón Corriente (AC/PC)', line=dict(color='#1E88E5', width=3)))
        fig_liq.add_trace(go.Scatter(x=df_ratios.index, y=df_ratios['Prueba Acida'], name='Prueba Ácida ((AC-Inv)/PC)', line=dict(color='#43A047', width=3)))
        fig_liq.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Punto Crítico (1.0x)")
        fig_liq.update_layout(template="plotly_white", yaxis=dict(title="Veces (x)"), height=380)
        st.plotly_chart(fig_liq, use_container_width=True)
        
    with c2:
        st.markdown("#### Composición del Activo Corriente")
        df_ac_comp = df_bg[['Efectivo', 'Cuentas por Cobrar', 'Inventarios', 'Otros Activos Corrientes']]
        fig_ac = px.bar(
            df_ac_comp, 
            barmode='stack',
            labels={'value': 'Miles de $', 'index': 'Año'},
            color_discrete_sequence=['#2E7D32', '#1976D2', '#FB8C00', '#78909C']
        )
        fig_ac.update_layout(template="plotly_white", height=380, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_ac, use_container_width=True)
        
    st.info(f"""
    **Análisis de Tesorería ({selected_year}):**
    La empresa ha consolidado un nivel extraordinario de holgura de liquidez. La razón corriente pasó de **1.92x en 2021 a 2.14x en 2025**. La prueba ácida superó la barrera de 1.0x desde 2022 y alcanza **1.41x en 2025**, garantizando total cobertura de obligaciones sin depender de la realización de inventarios.
    """)

# ================= TAB: ENDEUDAMIENTO =================
elif tab_option == "⚖️ Endeudamiento y Solvencia":
    st.subheader("Estructura de Capital, Perfil de Endeudamiento y Cobertura")
    
    col1, col2, col3, col4 = st.columns(4)
    end_tot = df_ratios.loc[selected_year, 'Endeudamiento Total (%)']
    d_e = df_ratios.loc[selected_year, 'Apalancamiento (D/E)']
    cob_int = df_ratios.loc[selected_year, 'Cobertura Intereses (x)']
    deuda_fin = df_bg.loc[selected_year, 'Deuda CP'] + df_bg.loc[selected_year, 'Deuda LP']
    
    col1.metric("Endeudamiento Total", f"{end_tot:.1f}%", f"{end_tot - df_ratios.loc[2021, 'Endeudamiento Total (%)']:.1f} pts vs 2021")
    col2.metric("Leverage (Pasivo / Patrimonio)", f"{d_e:.2f}x", "Descenso saludable")
    col3.metric("Cobertura de Intereses", f"{cob_int:.2f}x", "Excelente capacidad de pago")
    col4.metric("Deuda Financiera Total", f"${deuda_fin:,.0f}", f"CP: {df_bg.loc[selected_year, 'Deuda CP']} | LP: {df_bg.loc[selected_year, 'Deuda LP']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Estructura de Financiación (Pasivo vs Patrimonio)")
        df_fin_mix = pd.DataFrame({
            'Pasivo Corriente': df_bg['Pasivo Corriente'],
            'Pasivo Largo Plazo': df_bg['Deuda LP'],
            'Patrimonio': df_bg['Total Patrimonio']
        }, index=df_bg.index)
        
        fig_mix = px.bar(
            df_fin_mix,
            barmode='relative',
            labels={'value': 'Monto ($)', 'index': 'Año'},
            color_discrete_sequence=['#E53935', '#FB8C00', '#1E88E5']
        )
        fig_mix.update_layout(template="plotly_white", height=380, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_mix, use_container_width=True)
        
    with c2:
        st.markdown("#### Cobertura de Intereses (EBIT / Gastos Financieros)")
        fig_cob = px.line(
            df_ratios,
            y='Cobertura Intereses (x)',
            markers=True,
            labels={'Cobertura Intereses (x)': 'Cobertura (x)', 'index': 'Año'},
            color_discrete_sequence=['#43A047']
        )
        fig_cob.add_hline(y=2.5, line_dash="dash", line_color="orange", annotation_text="Límite Prudencial (2.5x)")
        fig_cob.update_layout(template="plotly_white", height=380)
        st.plotly_chart(fig_cob, use_container_width=True)

# ================= TAB: FLUJOS DE EFECTIVO =================
elif tab_option == "💵 Flujos de Caja y Efectivo":
    st.subheader("Dinámica del Flujo de Caja Libre y Conciliación de Tesorería")
    
    col1, col2, col3, col4 = st.columns(4)
    cfo = df_fe.loc[selected_year, 'CFO']
    cfi = df_fe.loc[selected_year, 'CFI']
    cff = df_fe.loc[selected_year, 'CFF']
    fcf = cfo + cfi # Flujo de caja libre aproximado
    
    col1.metric("Flujo Operativo (CFO)", f"${cfo:,.0f}", "+252% desde 2021")
    col2.metric("Inversión de Capital (CAPEX)", f"${abs(cfi):,.0f}", "Reinversión continua")
    col3.metric("Flujo de Caja Libre (FCF)", f"${fcf:,.0f}", "Capacidad de distribución")
    col4.metric("Dividendos Pagados", f"${abs(df_fe.loc[selected_year, 'Dividendos']):,.0f}", "Política de retorno al accionista")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Desglose de Flujos por Actividad")
        fig_flujos = go.Figure()
        fig_flujos.add_trace(go.Bar(x=df_fe.index, y=df_fe['CFO'], name='Operación (CFO)', marker_color='#2E7D32'))
        fig_flujos.add_trace(go.Bar(x=df_fe.index, y=df_fe['CFI'], name='Inversión (CFI)', marker_color='#E53935'))
        fig_flujos.add_trace(go.Bar(x=df_fe.index, y=df_fe['CFF'], name='Financiación (CFF)', marker_color='#1E88E5'))
        fig_flujos.update_layout(template="plotly_white", barmode='group', height=400,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_flujos, use_container_width=True)
        
    with c2:
        st.markdown("#### Evolución de Posición Final de Caja")
        fig_cash = go.Figure()
        fig_cash.add_trace(go.Scatter(x=df_fe.index, y=df_fe['Saldo Final'], fill='tozeroy',
                                      mode='lines+markers+text',
                                      text=[f"${v:,.0f}" for v in df_fe['Saldo Final']],
                                      textposition='top left',
                                      line=dict(color='#00897B', width=3),
                                      name='Saldo Final Caja'))
        fig_cash.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_cash, use_container_width=True)

# ================= TAB: ESTADOS DETALLADOS =================
elif tab_option == "📑 Estados Detallados":
    st.subheader("Tablas Maestras de Estados Financieros y Métricas")
    
    st.markdown("### 1. Estado de Resultados Integral")
    st.dataframe(df_er.T.style.format("${:,.0f}"), use_container_width=True)
    
    st.markdown("### 2. Balance General Clasificado")
    st.dataframe(df_bg.T.style.format("${:,.0f}"), use_container_width=True)
    
    st.markdown("### 3. Estado de Flujos de Efectivo")
    st.dataframe(df_fe.T.style.format("${:,.0f}"), use_container_width=True)
    
    st.markdown("### 4. Matriz de Ratios Financieros Clave")
    st.dataframe(df_ratios.T.style.format("{:.2f}"), use_container_width=True)

st.markdown("---")
st.caption("Dashboard desarrollado con Streamlit & Plotly | Datos fuente: Estados Financieros Auditados Empresa Andina.")
