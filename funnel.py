import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def _apply_cozy_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b2e22", family="sans-serif"),
        legend=dict(orientation="h", y=-0.15, x=0, font=dict(size=10)),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def render_funnel(df: pd.DataFrame) -> None:
    df_25 = df[df['wave'] == 2025]
    
    # 1. Tính toán data Funnel cho 3 nhãn
    brands = ['Trà Cozy đóng chai', 'C2', 'Không Độ']
    colors = {'Trà Cozy đóng chai': '#156835', 'C2': '#9ca3af', 'Không Độ': '#d1d5db'}
    stages = ['Aware', 'P3M', 'P4W', 'TOM', 'BUMO']
    
    funnel_data = {}
    for b in brands:
        aw = df_25[f'Q1Q2. Total aided awareness_{b}'].mean() * 100 if f'Q1Q2. Total aided awareness_{b}' in df_25.columns else 0
        p3m = df_25[f'Q3. P3M _{b}'].mean() * 100 if f'Q3. P3M _{b}' in df_25.columns else 0
        p4w_cols = [c for c in df_25.columns if b.split()[0] in c and c.startswith('Q4. P4W_')]
        p4w = df_25[p4w_cols].max(axis=1).mean() * 100 if p4w_cols else 0
        tom = (df_25['tom_master'] == b).mean() * 100
        bumo = (df_25['bumo_master'] == b).mean() * 100
        funnel_data[b] = [aw, p3m, p4w, tom, bumo]

    # 2. Render Biểu đồ cột Clustered
    st.markdown("### Trà Cozy vs C2 + Không Độ: 5 stage funnel")
    st.caption("Khoảng hụt lớn nhất của Cozy so với đối thủ nằm ở bước P3M và P4W")
    
    fig_funnel = go.Figure()
    for b in brands:
        fig_funnel.add_trace(go.Bar(
            x=stages, y=funnel_data[b], name=b.replace('Trà ', '').replace(' đóng chai', ''),
            marker_color=colors[b], text=[f"{v:.0f}" for v in funnel_data[b]], textposition='outside'
        ))
    
    # Thêm đường nối (Line) cho Cozy để giống design MoMo
    fig_funnel.add_trace(go.Scatter(
        x=stages, y=funnel_data['Trà Cozy đóng chai'], mode='lines', 
        line=dict(color='#156835', dash='dot', width=2), showlegend=False
    ))
    
    fig_funnel.update_layout(barmode='group', height=400)
    st.plotly_chart(_apply_cozy_theme(fig_funnel), use_container_width=True)

    # 3. Data Table Style (Bảng số liệu tổng hợp)
    st.markdown("---")
    st.markdown("**BẢNG CHUYỂN ĐỔI FUNNEL CHI TIẾT (WAVE 2025)**")
    
    table_data = []
    for i, stage in enumerate(stages):
        cozy_val = funnel_data['Trà Cozy đóng chai'][i]
        c2_val = funnel_data['C2'][i]
        kd_val = funnel_data['Không Độ'][i]
        
        # Tính tỷ lệ convert từ Aware cho Cozy
        cozy_aw = funnel_data['Trà Cozy đóng chai'][0]
        convert = f"{(cozy_val / cozy_aw * 100):.0f}% of Aware" if cozy_aw > 0 else "-"
        if stage == 'Aware': convert = "-"
        
        table_data.append({
            "STAGE": stage,
            "COZY": f"{cozy_val:.0f}%",
            "C2": f"{c2_val:.0f}%",
            "KHÔNG ĐỘ": f"{kd_val:.0f}%",
            "COZY CONVERT": convert
        })
        
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)