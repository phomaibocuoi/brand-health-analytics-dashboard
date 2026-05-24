import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def _apply_cozy_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b2e22", family="sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def render_imagery(df: pd.DataFrame) -> None:
    df_25 = df[df['wave'] == 2025]
    
    # 1. Trích xuất top 5 thuộc tính mạnh nhất của Cozy
    attrs = [
        'Nhãn hiệu đáng tin cậy', 'Sản xuất từ nguyên liệu tự nhiên', 
        'Giải nhiệt cuộc sống', 'Phù hợp để thưởng thức hàng ngày', 'Có lợi cho sức khỏe'
    ]
    
    cozy_scores = []
    c2_scores = []
    
    for attr in attrs:
        # Cozy
        c_col = f'QI - Trà Cozy đóng chai_{attr}'
        aw_cozy = df_25[df_25['Q1Q2. Total aided awareness_Trà Cozy đóng chai'] == 1]
        cozy_scores.append(aw_cozy[c_col].mean() * 100 if len(aw_cozy)>0 and c_col in df_25.columns else 0)
        
        # C2
        c2_col = f'QI - C2_{attr}'
        aw_c2 = df_25[df_25['Q1Q2. Total aided awareness_C2'] == 1]
        c2_scores.append(aw_c2[c2_col].mean() * 100 if len(aw_c2)>0 and c2_col in df_25.columns else 0)

    st.markdown("### Cozy Top Imagery: Định vị mạnh mẽ ở 'Niềm tin' & 'Tự nhiên'")
    st.caption("So sánh điểm liên tưởng hình ảnh (Base: Aware Respondents) giữa Cozy và C2")

    col1, col2 = st.columns([1, 1])
    
    # Biểu đồ Radar bên trái cho cái nhìn tổng quan định vị
    with col1:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=cozy_scores + [cozy_scores[0]], theta=attrs + [attrs[0]],
            fill='toself', name='Cozy', marker=dict(color='#156835')
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=c2_scores + [c2_scores[0]], theta=attrs + [attrs[0]],
            fill='toself', name='C2', marker=dict(color='#9ca3af')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 80])),
            showlegend=True, legend=dict(orientation="h", y=-0.2), height=400
        )
        st.plotly_chart(_apply_cozy_theme(fig_radar), use_container_width=True)

    # Biểu đồ Bar ngang bên phải giống y hệt style MoMo
    with col2:
        short_attrs = ['Đáng tin cậy', 'Tự nhiên', 'Giải nhiệt', 'Uống hằng ngày', 'Tốt sức khỏe']
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=short_attrs, x=cozy_scores, name='Cozy', orientation='h',
            marker_color='#156835', text=[f"{v:.0f}%" for v in cozy_scores], textposition='inside'
        ))
        fig_bar.add_trace(go.Bar(
            y=short_attrs, x=c2_scores, name='C2', orientation='h',
            marker_color='#e5e7eb', text=[f"{v:.0f}%" for v in c2_scores], textposition='outside'
        ))
        fig_bar.update_layout(barmode='group', yaxis=dict(autorange="reversed"), height=400)
        st.plotly_chart(_apply_cozy_theme(fig_bar), use_container_width=True)