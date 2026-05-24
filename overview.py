import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def _apply_cozy_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b2e22", family="sans-serif"),
        title_font=dict(color="#156835", size=14, family="sans-serif", weight="bold"),
        legend=dict(font=dict(color="#1b2e22", size=9), bgcolor="rgba(255,255,255,0.6)"),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def render_overview(df: pd.DataFrame) -> None:
    # 1. Tính toán Data
    df_25 = df[df['wave'] == 2025]
    df_24 = df[df['wave'] == 2024]
    
    def get_metric(d, brand, metric_type):
        if metric_type == 'aware':
            return d[f'Q1Q2. Total aided awareness_{brand}'].mean() * 100 if f'Q1Q2. Total aided awareness_{brand}' in d.columns else 0
        elif metric_type == 'tom':
            return (d['tom_master'] == brand).mean() * 100
        elif metric_type == 'bumo':
            return (d['bumo_master'] == brand).mean() * 100
            
    # Cozy Metrics
    cozy_aw_25 = get_metric(df_25, 'Trà Cozy đóng chai', 'aware')
    cozy_aw_24 = get_metric(df_24, 'Trà Cozy đóng chai', 'aware')
    cozy_tom_25 = get_metric(df_25, 'Trà Cozy đóng chai', 'tom')
    cozy_tom_24 = get_metric(df_24, 'Trà Cozy đóng chai', 'tom')
    cozy_bumo_25 = get_metric(df_25, 'Trà Cozy đóng chai', 'bumo')
    cozy_bumo_24 = get_metric(df_24, 'Trà Cozy đóng chai', 'bumo')
    n_resp_25 = len(df_25)
    
    # C2 Metrics (Đối thủ chính)
    c2_aw_25 = get_metric(df_25, 'C2', 'aware')
    c2_tom_25 = get_metric(df_25, 'C2', 'tom')
    c2_bumo_25 = get_metric(df_25, 'C2', 'bumo')

    # Deltas
    d_aw_wow = cozy_aw_25 - cozy_aw_24
    d_aw_c2 = cozy_aw_25 - c2_aw_25
    d_tom_wow = cozy_tom_25 - cozy_tom_24
    d_tom_c2 = cozy_tom_25 - c2_tom_25
    d_bumo_wow = cozy_bumo_25 - cozy_bumo_24
    d_bumo_c2 = cozy_bumo_25 - c2_bumo_25

    def delta_html(val):
        color = "#156835" if val >= 0 else "#dc2626"
        arrow = "▲" if val >= 0 else "▼"
        sign = "+" if val > 0 else ""
        return f'<span style="color: {color}; font-weight: bold; font-size: 0.9rem;">{sign}{val:.1f}pp {arrow}</span>'

    # 2. Render KPI Cards (Style MoMo)
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px;">
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px;">
                <div style="color: #6b7280; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">% AWARE COZY</div>
                <div style="font-size: 2rem; font-weight: 900; color: #111827;">{cozy_aw_25:.0f}%</div>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <div><span style="font-size:0.7rem; color:#9ca3af;">Δ W24</span><br>{delta_html(d_aw_wow)}</div>
                    <div><span style="font-size:0.7rem; color:#9ca3af;">VS C2</span><br>{delta_html(d_aw_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px;">
                <div style="color: #6b7280; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">% TOM COZY</div>
                <div style="font-size: 2rem; font-weight: 900; color: #111827;">{cozy_tom_25:.0f}%</div>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <div><span style="font-size:0.7rem; color:#9ca3af;">Δ W24</span><br>{delta_html(d_tom_wow)}</div>
                    <div><span style="font-size:0.7rem; color:#9ca3af;">VS C2</span><br>{delta_html(d_tom_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px;">
                <div style="color: #6b7280; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">% BUMO COZY</div>
                <div style="font-size: 2rem; font-weight: 900; color: #111827;">{cozy_bumo_25:.0f}%</div>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <div><span style="font-size:0.7rem; color:#9ca3af;">Δ W24</span><br>{delta_html(d_bumo_wow)}</div>
                    <div><span style="font-size:0.7rem; color:#9ca3af;">VS C2</span><br>{delta_html(d_bumo_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px;">
                <div style="color: #6b7280; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">N RESPONDENT</div>
                <div style="font-size: 2rem; font-weight: 900; color: #111827;">{n_resp_25}</div>
                <div style="display: flex; gap: 15px; margin-top: 5px;">
                    <div><span style="font-size:0.7rem; color:#9ca3af;">W24</span><br><span style="font-weight:bold; color:#374151;">1300</span></div>
                    <div><span style="font-size:0.7rem; color:#9ca3af;">W25</span><br><span style="font-weight:bold; color:#374151;">{n_resp_25}</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # 3. Charts (2x2 Grid)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Cozy dẫn funnel: 91% Aware → 9% BUMO · Rò rỉ lớn ở chặng đầu**")
        stages = ['Aware', 'P3M', 'P4W', 'TOM', 'BUMO']
        # Tính P3M, P4W nhanh
        p3m_25 = df_25['Q3. P3M _Trà Cozy đóng chai'].mean() * 100 if 'Q3. P3M _Trà Cozy đóng chai' in df_25.columns else 0
        p4w_cols = [c for c in df_25.columns if 'Cozy' in c and c.startswith('Q4. P4W_')]
        p4w_25 = df_25[p4w_cols].max(axis=1).mean() * 100 if p4w_cols else 0
        
        vals = [cozy_aw_25, p3m_25, p4w_25, cozy_tom_25, cozy_bumo_25]
        
        fig_funnel = go.Figure(go.Bar(
            x=vals, y=stages, orientation='h', marker_color="#156835",
            text=[f"{v:.0f}%" for v in vals], textposition="inside"
        ))
        fig_funnel.update_layout(yaxis=dict(autorange="reversed"), height=250)
        st.plotly_chart(_apply_cozy_theme(fig_funnel), use_container_width=True)

    with col2:
        st.markdown("**Cozy Aware tăng (+1pp) · C2 giảm (-4pp) W24→W25**")
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=['2024', '2025'], y=[cozy_aw_24, cozy_aw_25], mode='lines+markers+text', name='Cozy', line=dict(color='#156835', width=3), text=[f"{cozy_aw_24:.0f}%", f"{cozy_aw_25:.0f}%"], textposition="top center"))
        fig_trend.add_trace(go.Scatter(x=['2024', '2025'], y=[get_metric(df_24, 'C2', 'aware'), c2_aw_25], mode='lines+markers+text', name='C2', line=dict(color='#9ca3af', width=2, dash='dash'), text=[f"{get_metric(df_24, 'C2', 'aware'):.0f}%", f"{c2_aw_25:.0f}%"], textposition="bottom center"))
        fig_trend.update_layout(height=250, yaxis=dict(range=[80, 100]))
        st.plotly_chart(_apply_cozy_theme(fig_trend), use_container_width=True)