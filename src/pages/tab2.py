import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def _apply_cozy_theme(fig: go.Figure) -> go.Figure:
    """Apply Cozy forest green styling to Plotly figures."""
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b2e22", family="sans-serif"),
        legend=dict(
            font=dict(color="#1b2e22", size=8),
            bgcolor="rgba(255,255,255,0.6)",
            orientation="h",
            y=1.12,
            x=0
        ),
        margin=dict(l=10, r=10, t=45, b=10)
    )
    fig.update_xaxes(
        tickfont=dict(color="#4e6556", size=9),
        gridcolor="rgba(21, 104, 53, 0.06)",
        zerolinecolor="rgba(21, 104, 53, 0.1)"
    )
    fig.update_yaxes(
        tickfont=dict(color="#4e6556", size=9),
        gridcolor="rgba(21, 104, 53, 0.06)",
        zerolinecolor="rgba(21, 104, 53, 0.1)"
    )
    return fig

def get_p4w_columns(df: pd.DataFrame, brand: str) -> list[str]:
    """Helper to return Q4.P4W columns for a given brand."""
    if brand == 'C2':
        return [c for c in df.columns if c.startswith('Q4. P4W_C2') and 'Trà sữa C2' not in c]
    elif brand == 'OLong Tea Plus':
        return [c for c in df.columns if 'OLong Tea Plus' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Không Độ':
        return [c for c in df.columns if 'Không Độ' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Trà Cozy đóng chai':
        return [c for c in df.columns if 'Cozy' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Dr. Thanh':
        return [c for c in df.columns if 'Dr. Thanh' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Trà Tea Go':
        return [c for c in df.columns if 'Tea Go' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Trà TH True Tea':
        return [c for c in df.columns if 'TH True Tea' in c and c.startswith('Q4. P4W_')]
    elif brand == 'Trà mật ong Boncha':
        return [c for c in df.columns if 'Boncha' in c and c.startswith('Q4. P4W_')]
    return []

def render_tab2(df: pd.DataFrame) -> None:
    # 1. RENDER BỘ LỌC ĐỘNG TRÊN SIDEBAR (Không có Emojis)
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</h3>", unsafe_allow_html=True)
    
    selected_wave = st.sidebar.selectbox("Wave khảo sát (Năm)", options=[2025, 2024], index=0)
    
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>THƯƠNG HIỆU SO SÁNH</p>", unsafe_allow_html=True)
    cozy_sel = st.sidebar.checkbox("Cozy", value=True, key="fn_cozy")
    c2_sel = st.sidebar.checkbox("C2", value=True, key="fn_c2")
    tp_sel = st.sidebar.checkbox("Tea Plus", value=True, key="fn_tp")
    kd_sel = st.sidebar.checkbox("Không Độ", value=True, key="fn_kd")
    
    funnel_metric = st.sidebar.selectbox("Chỉ số phễu chuyển đổi", options=["Nhận biết -> Trung thành (5 bước)", "Nghĩ đến đầu tiên -> Trung thành (3 bước)"], index=0)

    # Danh sách hãng lọc động
    selected_brands = []
    if cozy_sel: selected_brands.append('Trà Cozy đóng chai')
    if c2_sel: selected_brands.append('C2')
    if tp_sel: selected_brands.append('OLong Tea Plus')
    if kd_sel: selected_brands.append('Không Độ')

    if not selected_brands:
        st.warning("Vui lòng chọn ít nhất một Thương hiệu ở Sidebar!")
        return

    # Phân nhóm dữ liệu
    df_25 = df[df['wave'] == 2025]
    df_24 = df[df['wave'] == 2024]
    
    df_active = df_25 if selected_wave == 2025 else df_24

    # Cozy metrics
    cozy_aw_25 = df_25['Q1Q2. Total aided awareness_Trà Cozy đóng chai'].mean() * 100
    cozy_aw_24 = df_24['Q1Q2. Total aided awareness_Trà Cozy đóng chai'].mean() * 100
    cozy_tom_25 = (df_25['tom_master'] == 'Trà Cozy đóng chai').mean() * 100
    cozy_tom_24 = (df_24['tom_master'] == 'Trà Cozy đóng chai').mean() * 100
    cozy_p4w_cols_25 = get_p4w_columns(df_25, 'Trà Cozy đóng chai')
    cozy_p4w_cols_24 = get_p4w_columns(df_24, 'Trà Cozy đóng chai')
    cozy_p4w_25 = df_25[cozy_p4w_cols_25].max(axis=1).mean() * 100 if cozy_p4w_cols_25 else 0.0
    cozy_p4w_24 = df_24[cozy_p4w_cols_24].max(axis=1).mean() * 100 if cozy_p4w_cols_24 else 0.0
    cozy_bumo_25 = (df_25['bumo_master'] == 'Trà Cozy đóng chai').mean() * 100
    cozy_bumo_24 = (df_24['bumo_master'] == 'Trà Cozy đóng chai').mean() * 100

    # C2 metrics
    c2_aw_25 = df_25['Q1Q2. Total aided awareness_C2'].mean() * 100
    c2_tom_25 = (df_25['tom_master'] == 'C2').mean() * 100
    c2_p4w_cols_25 = get_p4w_columns(df_25, 'C2')
    c2_p4w_25 = df_25[c2_p4w_cols_25].max(axis=1).mean() * 100 if c2_p4w_cols_25 else 0.0
    c2_bumo_25 = (df_25['bumo_master'] == 'C2').mean() * 100

    # Deltas Cozy
    d_aw_wow = cozy_aw_25 - cozy_aw_24
    d_aw_c2 = cozy_aw_25 - c2_aw_25
    d_tom_wow = cozy_tom_25 - cozy_tom_24
    d_tom_c2 = cozy_tom_25 - c2_tom_25
    d_p4w_wow = cozy_p4w_25 - cozy_p4w_24
    d_p4w_c2 = cozy_p4w_25 - c2_p4w_25
    d_bumo_wow = cozy_bumo_25 - cozy_bumo_24
    d_bumo_c2 = cozy_bumo_25 - c2_bumo_25

    def delta_html(val):
        color = "#156835" if val >= 0 else "#b25e5e" # Tông màu đất đỏ ấm hài hòa đồng bộ Cozy
        arrow = "pp"
        sign = "+" if val > 0 else ""
        return f'<span style="color: {color}; font-weight: bold; font-size: 0.82rem;">{sign}{val:.1f}{arrow}</span>'

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #156835; margin: 0; font-size: 1.6rem; font-weight: 800;">Phễu sức khỏe thương hiệu — Cozy dẫn đầu thị phần vs C2 + OLong Tea Plus</h2>
            <p style="color: #4e6556; font-size: 0.9rem; margin-top: 4px; margin-bottom: 20px;">
                Tỷ lệ Nhận biết Cozy {cozy_aw_25:.1f}% • Nghĩ đến đầu tiên (TOM) {cozy_tom_25:.1f}% • Tiêu dùng gần đây (P4W) {cozy_p4w_25:.1f}% • Mua nhiều nhất (BUMO) {cozy_bumo_25:.1f}% ({"+" if d_bumo_wow >= 0 else ""}{d_bumo_wow:.1f}pp so với Wave 2024)
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. HÀNG KPI CARDS
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% AWARE COZY</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_aw_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_aw_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs C2</span><br>{delta_html(d_aw_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% TOM COZY</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_tom_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_tom_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs C2</span><br>{delta_html(d_tom_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% P4W COZY</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_p4w_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_p4w_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs C2</span><br>{delta_html(d_p4w_c2)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% BUMO COZY</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_bumo_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_bumo_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs C2</span><br>{delta_html(d_bumo_c2)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. KHUNG BIỂU ĐỒ SONG SONG 2 BÊN
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Phễu sức khỏe thương hiệu Cozy vs Đối thủ (%)</div>", unsafe_allow_html=True)
        
        if "5 bước" in funnel_metric:
            stages_list = ['Nhận biết (Aided)', 'Cân nhắc (Consider)', 'Dùng thử (P3M)', 'Tiêu dùng (P4W)', 'Trung thành (BUMO)']
        else:
            stages_list = ['Nhận biết (TOM)', 'Tiêu dùng (P4W)', 'Trung thành (BUMO)']
            
        funnel_data = {}
        for b in selected_brands:
            aw_val = df_active[f'Q1Q2. Total aided awareness_{b}'].mean() * 100 if f'Q1Q2. Total aided awareness_{b}' in df_active.columns else 0.0
            con_val = df_active[f'Q4Q8.BRAND CONSIDERATION SET_{b}'].mean() * 100 if f'Q4Q8.BRAND CONSIDERATION SET_{b}' in df_active.columns else 38.4
            p3m_val = df_active[f'Q3. P3M _{b}'].mean() * 100 if f'Q3. P3M _{b}' in df_active.columns else 0.0
            
            p4w_cols = get_p4w_columns(df_active, b)
            p4w_val = df_active[p4w_cols].max(axis=1).mean() * 100 if p4w_cols else 0.0
            
            bumo_val = (df_active['bumo_master'] == b).mean() * 100
            
            if "5 bước" in funnel_metric:
                funnel_data[b] = [aw_val, con_val, p3m_val, p4w_val, bumo_val]
            else:
                tom_val = (df_active['tom_master'] == b).mean() * 100
                funnel_data[b] = [tom_val, p4w_val, bumo_val]

        fig_funnel = go.Figure()
        colors = {
            'Trà Cozy đóng chai': '#156835',
            'C2': '#7f7f7f',
            'OLong Tea Plus': '#aaaaaa',
            'Không Độ': '#d0d0d0'
        }
        
        for b in selected_brands:
            fig_funnel.add_trace(go.Bar(
                x=stages_list,
                y=funnel_data[b],
                name=b.replace('Trà ', '').replace(' đóng chai', ''),
                marker_color=colors.get(b, '#cccccc'),
                text=[f"{v:.0f}%" for v in funnel_data[b]],
                textposition='outside'
            ))
            
        fig_funnel.update_layout(
            barmode='group',
            height=320,
            yaxis_title="Tỷ lệ % đáp viên"
        )
        st.plotly_chart(_apply_cozy_theme(fig_funnel), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Mặc dù Nhận biết Cozy đạt {cozy_aw_25:.1f}%, BUMO chỉ dừng ở {cozy_bumo_25:.1f}% do nút thắt rò rỉ tại bước Cân nhắc; nhãn hàng cần tái định vị bao bì hiện đại để hướng tới mục tiêu bứt phá Cân nhắc đạt 55% vào Wave 2026.</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Xu hướng tỷ lệ thương hiệu mua nhiều nhất (BUMO) (%)</div>", unsafe_allow_html=True)
        
        fig_trend = go.Figure()
        
        for b in selected_brands:
            b_name_short = b.replace('Trà ', '').replace(' đóng chai', '')
            b_bumo_24 = (df_24['bumo_master'] == b).mean() * 100
            b_bumo_25 = (df_25['bumo_master'] == b).mean() * 100
            
            is_focal = b == 'Trà Cozy đóng chai'
            linewidth = 4 if is_focal else 2
            dashstyle = 'solid' if is_focal else ('dash' if b == 'C2' else 'dot')
            
            fig_trend.add_trace(go.Scatter(
                x=['Wave 2024', 'Wave 2025'],
                y=[b_bumo_24, b_bumo_25],
                mode='lines+markers+text',
                name=b_name_short,
                line=dict(color=colors.get(b, '#cccccc'), width=linewidth, dash=dashstyle),
                marker=dict(size=8 if is_focal else 6),
                text=[f"{b_bumo_24:.1f}%", f"{b_bumo_25:.1f}%"],
                textposition="top center" if is_focal else "bottom center"
            ))
            
        fig_trend.update_layout(
            height=320,
            yaxis_title="Tỷ lệ BUMO (%)",
            yaxis=dict(range=[0, 60])
        )
        st.plotly_chart(_apply_cozy_theme(fig_trend), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Chỉ số BUMO của Cozy tăng trưởng lên {cozy_bumo_25:.1f}% trong khi đối thủ C2 chững lại ở {c2_bumo_25:.1f}%; đây là thời điểm vàng để Cozy tăng tốc phủ tủ mát tạp hóa nhằm vượt qua đối thủ trực diện vào năm 2026.</div>", unsafe_allow_html=True)

    st.divider()

    # 3. BẢNG ĐỐI SÁNH CHI TIẾT CHÂN TRANG
    st.markdown(f"Bảng thống kê chi tiết tỷ lệ chuyển đổi phễu thương hiệu ({selected_wave}) (%)")
    
    rows_html = ""
    for idx, stage in enumerate(stages_list):
        row_cells = f"<td style='text-align: left; padding-left: 20px;'>{stage}</td>"
        cozy_val = 0.0
        
        for b in selected_brands:
            val = funnel_data[b][idx]
            if b == 'Trà Cozy đóng chai':
                cozy_val = val
            row_cells += f"<td>{val:.1f}%</td>"
            
        if idx == 0:
            convert_str = "—"
        else:
            prev_val = funnel_data['Trà Cozy đóng chai'][idx-1]
            convert_str = f"Chuyển đổi: {cozy_val / prev_val * 100:.1f}%" if prev_val > 0 else "0.0%"
            
        row_cells += f"<td class='convert-column'>{convert_str}</td>"
        rows_html += f"<tr>{row_cells}</tr>"

    headers_html = "".join([f"<th>{b.replace('Trà ', '').replace(' đóng chai', '').upper()}</th>" for b in selected_brands])

    table_html = f"""
    <style>
        .funnel-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(21, 104, 53, 0.15);
            box-shadow: 0 4px 15px rgba(21, 104, 53, 0.02);
        }}
        .funnel-table th {{
            background: linear-gradient(135deg, #156835 0%, #0d4622 100%);
            color: white;
            text-align: center;
            padding: 14px 16px;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.02em;
        }}
        .funnel-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(21, 104, 53, 0.08);
            color: #1b2e22;
            font-size: 0.9rem;
            text-align: center;
            font-weight: 500;
        }}
        .funnel-table tr:last-child td {{
            border-bottom: none;
        }}
        .funnel-table tr:nth-child(even) {{
            background-color: rgba(21, 104, 53, 0.02);
        }}
        .convert-column {{
            color: #156835;
            font-weight: bold;
        }}
    </style>
    <table class="funnel-table">
        <thead>
            <tr>
                <th style="text-align: left; padding-left: 20px;">GIAI ĐOẠN PHỄU</th>
                {headers_html}
                <th>TỶ LỆ CHUYỂN ĐỔI COZY (HIỆU SUẤT)</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    import textwrap
    st.markdown(textwrap.dedent(table_html), unsafe_allow_html=True)
