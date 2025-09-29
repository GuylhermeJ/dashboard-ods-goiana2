import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🌍 Dashboard ODS Goiana-PE",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #2E8B57, #20B2AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 0.5rem 0;
    }
    
    .ods-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
@st.cache_data
def load_and_process_data():
    """Load and process the Excel data"""
    try:
        # Load ODS Municipios sheet
        ods_data = pd.read_excel('Projeto Goiana - PE.xlsx', sheet_name='ODS Municipios')
        ods_data = ods_data.dropna(how='all').dropna(axis=1, how='all')
        
        # Load other relevant sheets
        tabela_dados = pd.read_excel('Projeto Goiana - PE.xlsx', sheet_name='Tabela Dados')
        dados_tabela_din = pd.read_excel('Projeto Goiana - PE.xlsx', sheet_name='Dados Tabela Din')
        
        return ods_data, tabela_dados, dados_tabela_din
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

def get_ods_info():
    """Get comprehensive ODS information"""
    return {
        1: {"name": "Erradicação da Pobreza", "color": "#E5243B", "icon": "🏠"},
        2: {"name": "Fome Zero", "color": "#DDA63A", "icon": "🌾"},
        3: {"name": "Saúde e Bem-estar", "color": "#4C9F38", "icon": "❤️"},
        4: {"name": "Educação de Qualidade", "color": "#C5192D", "icon": "📚"},
        5: {"name": "Igualdade de Gênero", "color": "#FF3A21", "icon": "⚖️"},
        6: {"name": "Água Potável e Saneamento", "color": "#26BDE2", "icon": "💧"},
        7: {"name": "Energia Limpa", "color": "#FCC30B", "icon": "⚡"},
        8: {"name": "Trabalho Decente", "color": "#A21942", "icon": "💼"},
        9: {"name": "Inovação e Infraestrutura", "color": "#FD6925", "icon": "🏗️"},
        10: {"name": "Redução das Desigualdades", "color": "#DD1367", "icon": "📊"},
        11: {"name": "Cidades Sustentáveis", "color": "#FD9D24", "icon": "🏙️"},
        12: {"name": "Consumo Responsável", "color": "#BF8B2E", "icon": "♻️"},
        13: {"name": "Ação Climática", "color": "#3F7E44", "icon": "🌍"},
        14: {"name": "Vida na Água", "color": "#0A97D9", "icon": "🐠"},
        15: {"name": "Vida Terrestre", "color": "#56C02B", "icon": "🌳"},
        16: {"name": "Paz e Justiça", "color": "#00689D", "icon": "⚖️"},
        17: {"name": "Parcerias", "color": "#19486A", "icon": "🤝"}
    }

def create_advanced_radar_chart(data, municipalities, title="Comparação ODS"):
    """Create advanced radar chart with multiple municipalities"""
    if data is None or not municipalities:
        return None
    
    ods_info = get_ods_info()
    
    # Get ODS numbers and create labels
    ods_numbers = sorted(data['ODS'].dropna().unique())
    labels = [f"{ods_info.get(int(ods), {}).get('icon', '📊')} ODS {int(ods)}" for ods in ods_numbers]
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    
    for i, municipality in enumerate(municipalities):
        if municipality in data.columns:
            values = []
            for ods in ods_numbers:
                ods_row = data[data['ODS'] == ods]
                if not ods_row.empty and municipality in ods_row.columns:
                    value = ods_row[municipality].iloc[0]
                    values.append(value if pd.notna(value) else 0)
                else:
                    values.append(0)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=labels,
                fill='toself',
                name=municipality,
                line_color=colors[i % len(colors)],
                fillcolor=colors[i % len(colors)],
                opacity=0.6
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        title=dict(text=title, x=0.5, font=dict(size=16)),
        height=500,
        font=dict(size=12)
    )
    
    return fig

def create_performance_gauge(value, title, color_scheme="Viridis"):
    """Create a gauge chart for performance metrics"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16}},
        delta = {'reference': 0.5, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.3], 'color': '#ffcccc'},
                {'range': [0.3, 0.7], 'color': '#ffffcc'},
                {'range': [0.7, 1], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.8
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_ods_treemap(data, municipality):
    """Create treemap visualization for ODS performance"""
    if data is None or municipality not in data.columns:
        return None
    
    ods_info = get_ods_info()
    
    # Prepare data
    treemap_data = []
    for _, row in data.iterrows():
        ods_num = int(row['ODS'])
        value = row[municipality]
        if pd.notna(value):
            treemap_data.append({
                'ODS': f"ODS {ods_num}",
                'Nome': ods_info.get(ods_num, {}).get('name', 'N/A'),
                'Valor': value,
                'Icon': ods_info.get(ods_num, {}).get('icon', '📊'),
                'Color': ods_info.get(ods_num, {}).get('color', '#333333')
            })
    
    if not treemap_data:
        return None
    
    df_treemap = pd.DataFrame(treemap_data)
    
    fig = px.treemap(
        df_treemap,
        path=['ODS'],
        values='Valor',
        color='Valor',
        color_continuous_scale='RdYlGn',
        title=f'Mapa de Árvore ODS - {municipality}',
        hover_data=['Nome']
    )
    
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:.3f}",
        textfont_size=12
    )
    
    fig.update_layout(height=500)
    return fig

def create_trend_analysis(data, municipalities):
    """Create trend analysis chart"""
    if data is None or not municipalities:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribuição de Performance', 'Comparação por Quartis', 
                       'Análise de Variabilidade', 'Performance Relativa'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, municipality in enumerate(municipalities[:4]):
        if municipality in data.columns:
            values = data[municipality].dropna()
            
            # Histogram
            fig.add_trace(
                go.Histogram(x=values, name=f'{municipality} Dist', 
                           opacity=0.7, nbinsx=10, 
                           marker_color=colors[i % len(colors)]),
                row=1, col=1
            )
            
            # Box plot
            fig.add_trace(
                go.Box(y=values, name=f'{municipality} Box',
                      marker_color=colors[i % len(colors)]),
                row=1, col=2
            )
            
            # Violin plot
            fig.add_trace(
                go.Violin(y=values, name=f'{municipality} Violin',
                         line_color=colors[i % len(colors)]),
                row=2, col=1
            )
            
            # Performance by ODS
            ods_performance = []
            for ods in sorted(data['ODS'].dropna().unique()):
                ods_row = data[data['ODS'] == ods]
                if not ods_row.empty:
                    value = ods_row[municipality].iloc[0]
                    if pd.notna(value):
                        ods_performance.append(value)
            
            fig.add_trace(
                go.Scatter(x=list(range(len(ods_performance))), y=ods_performance,
                          mode='lines+markers', name=f'{municipality} Trend',
                          line=dict(color=colors[i % len(colors)], width=3),
                          marker=dict(size=8)),
                row=2, col=2
            )
    
    fig.update_layout(height=800, showlegend=True, title_text="Análise Avançada de Tendências")
    return fig

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Dashboard Interativo ODS - Goiana PE</h1>', unsafe_allow_html=True)
    
    # Load data
    ods_data, tabela_dados, dados_tabela_din = load_and_process_data()
    
    if ods_data is None:
        st.error("❌ Não foi possível carregar os dados. Verifique o arquivo Excel.")
        return
    
    # Process data
    municipalities = [col for col in ods_data.columns if col not in ['Unnamed: 0', 'Unnamed: 1'] and 'Unnamed' not in str(col)]
    ods_data_clean = ods_data[['Unnamed: 0'] + municipalities].copy()
    ods_data_clean.columns = ['ODS'] + municipalities
    ods_data_clean['ODS'] = pd.to_numeric(ods_data_clean['ODS'], errors='coerce')
    ods_data_clean = ods_data_clean.dropna(subset=['ODS'])
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Controles do Dashboard")
    
    # Municipality selection
    selected_municipalities = st.sidebar.multiselect(
        "🏙️ Selecione Municípios:",
        municipalities,
        default=municipalities[:3] if len(municipalities) >= 3 else municipalities,
        help="Escolha até 4 municípios para comparação"
    )
    
    # ODS selection
    available_ods = sorted(ods_data_clean['ODS'].dropna().unique())
    selected_ods = st.sidebar.selectbox(
        "🎯 Foco em ODS:",
        available_ods,
        format_func=lambda x: f"ODS {int(x)}: {get_ods_info().get(int(x), {}).get('name', 'N/A')}"
    )
    
    # Analysis type
    analysis_type = st.sidebar.radio(
        "📊 Tipo de Análise:",
        ["Visão Geral", "Comparativo Detalhado", "Análise Avançada", "Relatório Executivo"]
    )
    
    # Main content based on analysis type
    if analysis_type == "Visão Geral":
        show_overview(ods_data_clean, selected_municipalities)
    elif analysis_type == "Comparativo Detalhado":
        show_detailed_comparison(ods_data_clean, selected_municipalities)
    elif analysis_type == "Análise Avançada":
        show_advanced_analysis(ods_data_clean, selected_municipalities)
    else:
        show_executive_report(ods_data_clean, selected_municipalities)

def show_overview(data, municipalities):
    """Show overview dashboard"""
    st.markdown("## 📊 Visão Geral do Desempenho ODS")
    
    if not municipalities:
        st.warning("⚠️ Selecione pelo menos um município para visualizar os dados.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ods = len(data['ODS'].dropna())
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 ODS Avaliados</h3>
            <h2>{total_ods}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_municipalities = len(municipalities)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏙️ Municípios</h3>
            <h2>{total_municipalities}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if 'Goiana 1' in data.columns:
            avg_goiana = data['Goiana 1'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Média Goiana</h3>
                <h2>{avg_goiana:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if municipalities:
            best_municipality = municipalities[0]
            best_avg = 0
            for municipality in municipalities:
                if municipality in data.columns:
                    avg = data[municipality].mean()
                    if avg > best_avg:
                        best_avg = avg
                        best_municipality = municipality
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 Melhor Média</h3>
                <h2>{best_municipality}</h2>
                <p>{best_avg:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main visualizations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Radar chart
        radar_fig = create_advanced_radar_chart(data, municipalities[:4], "Comparação Multidimensional ODS")
        if radar_fig:
            st.plotly_chart(radar_fig, use_container_width=True)
    
    with col2:
        # Performance gauges
        st.markdown("### 🎯 Medidores de Performance")
        for municipality in municipalities[:3]:
            if municipality in data.columns:
                avg_performance = data[municipality].mean()
                gauge_fig = create_performance_gauge(avg_performance, municipality)
                st.plotly_chart(gauge_fig, use_container_width=True)
    
    # Treemap visualization
    if municipalities:
        st.markdown("### 🗺️ Mapa de Árvore - Distribuição ODS")
        selected_municipality = st.selectbox("Escolha um município para o mapa de árvore:", municipalities)
        
        treemap_fig = create_ods_treemap(data, selected_municipality)
        if treemap_fig:
            st.plotly_chart(treemap_fig, use_container_width=True)

def show_detailed_comparison(data, municipalities):
    """Show detailed comparison analysis"""
    st.markdown("## 📈 Análise Comparativa Detalhada")
    
    if len(municipalities) < 2:
        st.warning("⚠️ Selecione pelo menos 2 municípios para comparação.")
        return
    
    # Performance comparison table
    st.markdown("### 📊 Tabela de Performance Comparativa")
    
    comparison_data = []
    ods_info = get_ods_info()
    
    for _, row in data.iterrows():
        ods_num = int(row['ODS'])
        row_data = {
            'ODS': f"{ods_info.get(ods_num, {}).get('icon', '📊')} ODS {ods_num}",
            'Nome': ods_info.get(ods_num, {}).get('name', 'N/A')
        }
        
        for municipality in municipalities:
            if municipality in data.columns:
                value = row[municipality]
                row_data[municipality] = f"{value:.3f}" if pd.notna(value) else "N/A"
        
        comparison_data.append(row_data)
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    # Statistical comparison
    st.markdown("### 📈 Análise Estatística")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot comparison
        box_data = []
        for municipality in municipalities:
            if municipality in data.columns:
                values = data[municipality].dropna()
                for value in values:
                    box_data.append({'Município': municipality, 'Valor ODS': value})
        
        if box_data:
            box_df = pd.DataFrame(box_data)
            fig_box = px.box(box_df, x='Município', y='Valor ODS',
                           title='Distribuição de Performance ODS',
                           color='Município')
            fig_box.update_layout(height=400)
            st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        # Violin plot
        if box_data:
            fig_violin = px.violin(box_df, x='Município', y='Valor ODS',
                                 title='Densidade de Performance ODS',
                                 color='Município')
            fig_violin.update_layout(height=400)
            st.plotly_chart(fig_violin, use_container_width=True)
    
    # Correlation analysis
    st.markdown("### 🔗 Análise de Correlação")
    
    if len(municipalities) >= 2:
        correlation_data = data[municipalities].corr()
        
        fig_corr = px.imshow(correlation_data,
                           title='Matriz de Correlação entre Municípios',
                           color_continuous_scale='RdBu',
                           aspect='auto')
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)

def show_advanced_analysis(data, municipalities):
    """Show advanced analysis"""
    st.markdown("## 🔬 Análise Avançada")
    
    if not municipalities:
        st.warning("⚠️ Selecione municípios para análise avançada.")
        return
    
    # Trend analysis
    trend_fig = create_trend_analysis(data, municipalities)
    if trend_fig:
        st.plotly_chart(trend_fig, use_container_width=True)
    
    # Performance clustering
    st.markdown("### 🎯 Análise de Clusters de Performance")
    
    # Create performance categories
    performance_categories = []
    ods_info = get_ods_info()
    
    for municipality in municipalities:
        if municipality in data.columns:
            values = data[municipality].dropna()
            high_performance = len(values[values >= 0.7])
            medium_performance = len(values[(values >= 0.4) & (values < 0.7)])
            low_performance = len(values[values < 0.4])
            
            performance_categories.append({
                'Município': municipality,
                'Alta Performance (≥0.7)': high_performance,
                'Média Performance (0.4-0.7)': medium_performance,
                'Baixa Performance (<0.4)': low_performance
            })
    
    if performance_categories:
        perf_df = pd.DataFrame(performance_categories)
        
        fig_stack = px.bar(perf_df, x='Município',
                          y=['Alta Performance (≥0.7)', 'Média Performance (0.4-0.7)', 'Baixa Performance (<0.4)'],
                          title='Distribuição de Performance por Categoria',
                          color_discrete_map={
                              'Alta Performance (≥0.7)': '#2ECC71',
                              'Média Performance (0.4-0.7)': '#F39C12',
                              'Baixa Performance (<0.4)': '#E74C3C'
                          })
        fig_stack.update_layout(height=500)
        st.plotly_chart(fig_stack, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Recomendações Baseadas em Dados")
    
    recommendations = []
    
    for municipality in municipalities[:3]:
        if municipality in data.columns:
            values = data[municipality].dropna()
            worst_ods_idx = values.idxmin()
            worst_ods = data.loc[worst_ods_idx, 'ODS']
            worst_value = values.min()
            
            best_ods_idx = values.idxmax()
            best_ods = data.loc[best_ods_idx, 'ODS']
            best_value = values.max()
            
            recommendations.append({
                'municipality': municipality,
                'worst_ods': int(worst_ods),
                'worst_value': worst_value,
                'best_ods': int(best_ods),
                'best_value': best_value
            })
    
    for rec in recommendations:
        ods_info = get_ods_info()
        worst_name = ods_info.get(rec['worst_ods'], {}).get('name', 'N/A')
        best_name = ods_info.get(rec['best_ods'], {}).get('name', 'N/A')
        
        st.markdown(f"""
        <div class="info-box">
            <h4>🏙️ {rec['municipality']}</h4>
            <div class="warning-card">
                <strong>⚠️ Área de Melhoria:</strong> ODS {rec['worst_ods']} - {worst_name} ({rec['worst_value']:.3f})
            </div>
            <div class="success-card">
                <strong>✅ Ponto Forte:</strong> ODS {rec['best_ods']} - {best_name} ({rec['best_value']:.3f})
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_executive_report(data, municipalities):
    """Show executive report"""
    st.markdown("## 📋 Relatório Executivo")
    
    # Executive summary
    st.markdown("### 📊 Resumo Executivo")
    
    if municipalities:
        # Calculate overall statistics
        total_municipalities = len(municipalities)
        total_ods = len(data['ODS'].dropna())
        
        # Performance summary
        performance_summary = {}
        for municipality in municipalities:
            if municipality in data.columns:
                values = data[municipality].dropna()
                performance_summary[municipality] = {
                    'média': values.mean(),
                    'mediana': values.median(),
                    'desvio_padrão': values.std(),
                    'mínimo': values.min(),
                    'máximo': values.max()
                }
        
        # Create summary table
        summary_df = pd.DataFrame(performance_summary).T
        summary_df = summary_df.round(3)
        
        st.markdown("#### 📈 Estatísticas Gerais")
        st.dataframe(summary_df, use_container_width=True)
        
        # Key insights
        st.markdown("### 🔍 Principais Insights")
        
        # Best and worst performing municipalities
        best_municipality = max(performance_summary.keys(), 
                              key=lambda x: performance_summary[x]['média'])
        worst_municipality = min(performance_summary.keys(), 
                               key=lambda x: performance_summary[x]['média'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="success-card">
                <h4>🏆 Melhor Performance Geral</h4>
                <h3>{best_municipality}</h3>
                <p>Média ODS: {performance_summary[best_municipality]['média']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="warning-card">
                <h4>⚠️ Maior Potencial de Melhoria</h4>
                <h3>{worst_municipality}</h3>
                <p>Média ODS: {performance_summary[worst_municipality]['média']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Action items
        st.markdown("### 🎯 Plano de Ação Recomendado")
        
        action_items = [
            "🔍 **Análise Detalhada**: Investigar as causas dos baixos índices nos ODS críticos",
            "📊 **Benchmarking**: Estudar as melhores práticas dos municípios com melhor performance",
            "🤝 **Parcerias**: Estabelecer colaborações entre municípios para compartilhamento de experiências",
            "📈 **Monitoramento**: Implementar sistema de acompanhamento contínuo dos indicadores ODS",
            "💡 **Inovação**: Desenvolver soluções inovadoras para os desafios identificados"
        ]
        
        for item in action_items:
            st.markdown(f"- {item}")
        
        # Download report
        st.markdown("### 📥 Exportar Relatório")
        
        if st.button("📊 Gerar Relatório Completo"):
            # Create comprehensive report data
            report_data = {
                'Resumo Executivo': summary_df,
                'Dados Completos': data[['ODS'] + municipalities]
            }
            
            st.success("✅ Relatório gerado com sucesso!")
            st.info("💡 Os dados estão disponíveis nas tabelas acima para análise detalhada.")

if __name__ == "__main__":
    main()