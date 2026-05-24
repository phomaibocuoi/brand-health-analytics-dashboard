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
        title_font=dict(color="#156835", size=14, family="sans-serif", weight="bold"),
        legend=dict(
            font=dict(color="#1b2e22", size=9),
            bgcolor="rgba(255,255,255,0.6)",
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="rgba(21, 104, 53, 0.2)",
            font=dict(color="#1b2e22"),
        ),
    )
    fig.update_xaxes(
        tickfont=dict(color="#4e6556", size=9),
        gridcolor="rgba(21, 104, 53, 0.08)",
        zerolinecolor="rgba(21, 104, 53, 0.12)",
    )
    fig.update_yaxes(
        tickfont=dict(color="#4e6556", size=9),
        gridcolor="rgba(21, 104, 53, 0.08)",
        zerolinecolor="rgba(21, 104, 53, 0.12)",
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
    """Render full brand health and behavior analysis (Phần 2)."""
    # ===== 1. TÍNH TOÁN CÁC CHỈ SỐ SỨC KHỎE CHO COZY (WAVE MỚI NHẤT 2025) =====
    df_25 = df[df['wave'] == 2025]
    
    cozy_tom = (df_25['tom_master'] == 'Trà Cozy đóng chai').mean() * 100
    cozy_aided = df_25['Q1Q2. Total aided awareness_Trà Cozy đóng chai'].mean() * 100
    cozy_p3m = df_25['Q3. P3M _Trà Cozy đóng chai'].mean() * 100
    cozy_bumo = (df_25['bumo_master'] == 'Trà Cozy đóng chai').mean() * 100

    # ===== 2. VẼ CÁC KPI CARDS =====
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">TOM Awareness (Nghĩ đến đầu tiên)</div>
                <div class="kpi-value">{cozy_tom:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Aided Awareness (Nhận biết gợi ý)</div>
                <div class="kpi-value">{cozy_aided:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">P3M Penetration (Dùng thử 3 tháng)</div>
                <div class="kpi-value">{cozy_p3m:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">BUMO Share (Thương hiệu trung thành)</div>
                <div class="kpi-value">{cozy_bumo:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<p style='font-size:0.8rem;color:#6b7280;margin:0;'>* Chỉ số hiển thị trên thẻ được tính trên mẫu Wave 2025 (n = 1,300) đại diện cho sức khỏe hiện tại của Cozy.</p>", unsafe_allow_html=True)
    st.divider()

    # ===== 3. BỘ LỌC NĂM (WAVE FILTERS) CHO PHÂN TÍCH SO SÁNH =====
    target_brands = ['C2', 'OLong Tea Plus', 'Không Độ', 'Trà Cozy đóng chai', 'Trà mật ong Boncha', 'Trà TH True Tea', 'Dr. Thanh', 'Trà Tea Go']
    
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        selected_wave = st.selectbox(
            "Chọn thời kỳ báo cáo:",
            options=["Mới nhất (2025)", "So sánh 2024 vs 2025"],
            index=0
        )
    
    st.subheader("📊 1. Kim tự tháp Nhận biết Thương hiệu (Brand Awareness)")
    
    # Tính toán dữ liệu Nhận biết cho cả 2 năm
    df_24 = df[df['wave'] == 2024]
    
    results_24 = []
    results_25 = []
    for b in target_brands:
        tom_24 = (df_24['tom_master'] == b).mean() * 100
        spon_24 = df_24[f'Q1.Total Spontaneous_{b}'].mean() * 100 if f'Q1.Total Spontaneous_{b}' in df_24.columns else 0.0
        aided_24 = df_24[f'Q1Q2. Total aided awareness_{b}'].mean() * 100 if f'Q1Q2. Total aided awareness_{b}' in df_24.columns else 0.0
        results_24.append({'Brand': b, 'TOM': tom_24, 'Spontaneous': spon_24, 'Aided': aided_24})

        tom_25 = (df_25['tom_master'] == b).mean() * 100
        spon_25 = df_25[f'Q1.Total Spontaneous_{b}'].mean() * 100 if f'Q1.Total Spontaneous_{b}' in df_25.columns else 0.0
        aided_25 = df_25[f'Q1Q2. Total aided awareness_{b}'].mean() * 100 if f'Q1Q2. Total aided awareness_{b}' in df_25.columns else 0.0
        results_25.append({'Brand': b, 'TOM': tom_25, 'Spontaneous': spon_25, 'Aided': aided_25})
        
    df_aw_24 = pd.DataFrame(results_24).set_index('Brand')
    df_aw_25 = pd.DataFrame(results_25).set_index('Brand')
    
    # Sắp xếp các nhãn hàng theo Aided 2025 giảm dần để chuẩn hóa biểu đồ
    df_aw_25 = df_aw_25.sort_values(by='Aided', ascending=False)
    df_aw_24 = df_aw_24.reindex(df_aw_25.index)

    # Hàm vẽ cột Nhận biết
    def draw_bar_charts(metric_name, title):
        fig = go.Figure()
        
        # Đặt màu đặc trưng: Cozy màu đậm/nhạt, các đối thủ màu sage đồng đều để làm nổi bật Cozy
        colors_24 = ['#a3c9a8' if b == 'Trà Cozy đóng chai' else '#DAEEDA' for b in df_aw_25.index]
        colors_25 = ['#156835' if b == 'Trà Cozy đóng chai' else '#8FA98F' for b in df_aw_25.index]
        
        if selected_wave == "Mới nhất (2025)":
            fig.add_trace(go.Bar(
                x=df_aw_25.index,
                y=df_aw_25[metric_name],
                marker_color=colors_25,
                text=df_aw_25[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2025"
            ))
        else:
            fig.add_trace(go.Bar(
                x=df_aw_24.index,
                y=df_aw_24[metric_name],
                marker_color=colors_24,
                text=df_aw_24[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2024"
            ))
            fig.add_trace(go.Bar(
                x=df_aw_25.index,
                y=df_aw_25[metric_name],
                marker_color=colors_25,
                text=df_aw_25[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2025"
            ))
            fig.update_layout(barmode='group')
            
        fig.update_layout(
            title=title,
            yaxis_title="Tỷ lệ phần trăm (%)",
            height=300,
            margin=dict(l=10, r=10, t=65, b=10),
            legend=dict(orientation="h", y=1.1, x=0)
        )
        return _apply_cozy_theme(fig)

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.plotly_chart(draw_bar_charts('TOM', "Q1.TOM: Nhận biết đầu tiên (%)"), use_container_width=True, config={"displayModeBar": False})
    with r1c2:
        st.plotly_chart(draw_bar_charts('Spontaneous', "Q1.Spontaneous: Tự phát (%)"), use_container_width=True, config={"displayModeBar": False})
    with r1c3:
        st.plotly_chart(draw_bar_charts('Aided', "Q1Q2.Aided: Có gợi ý (%)"), use_container_width=True, config={"displayModeBar": False})

    # ===== 4. PHÂN TÍCH THÂM NHẬP THỊ TRƯỜNG =====
    st.subheader("📈 2. Chỉ số Thâm nhập và Tiêu dùng (Penetration & Usage)")
    
    results_use_24 = []
    results_use_25 = []
    
    for b in target_brands:
        p4w_cols = get_p4w_columns(df_24, b)
        p3m_24 = df_24[f'Q3. P3M _{b}'].mean() * 100 if f'Q3. P3M _{b}' in df_24.columns else 0.0
        p4w_24 = df_24[p4w_cols].max(axis=1).mean() * 100 if p4w_cols else 0.0
        bumo_24 = (df_24['bumo_master'] == b).mean() * 100
        results_use_24.append({'Brand': b, 'P3M': p3m_24, 'P4W': p4w_24, 'BUMO': bumo_24})
        
        p4w_cols_25 = get_p4w_columns(df_25, b)
        p3m_25 = df_25[f'Q3. P3M _{b}'].mean() * 100 if f'Q3. P3M _{b}' in df_25.columns else 0.0
        p4w_25 = df_25[p4w_cols_25].max(axis=1).mean() * 100 if p4w_cols_25 else 0.0
        bumo_25 = (df_25['bumo_master'] == b).mean() * 100
        results_use_25.append({'Brand': b, 'P3M': p3m_25, 'P4W': p4w_25, 'BUMO': bumo_25})
        
    df_use_24 = pd.DataFrame(results_use_24).set_index('Brand')
    df_use_25 = pd.DataFrame(results_use_25).set_index('Brand')
    
    df_use_25 = df_use_25.sort_values(by='P3M', ascending=False)
    df_use_24 = df_use_24.reindex(df_use_25.index)

    def draw_use_charts(metric_name, title):
        fig = go.Figure()
        colors_24 = ['#a3c9a8' if b == 'Trà Cozy đóng chai' else '#DAEEDA' for b in df_use_25.index]
        colors_25 = ['#156835' if b == 'Trà Cozy đóng chai' else '#8FA98F' for b in df_use_25.index]
        
        if selected_wave == "Mới nhất (2025)":
            fig.add_trace(go.Bar(
                x=df_use_25.index,
                y=df_use_25[metric_name],
                marker_color=colors_25,
                text=df_use_25[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2025"
            ))
        else:
            fig.add_trace(go.Bar(
                x=df_use_24.index,
                y=df_use_24[metric_name],
                marker_color=colors_24,
                text=df_use_24[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2024"
            ))
            fig.add_trace(go.Bar(
                x=df_use_25.index,
                y=df_use_25[metric_name],
                marker_color=colors_25,
                text=df_use_25[metric_name].map(lambda x: f"{x:.1f}%"),
                textposition="outside",
                name="2025"
            ))
            fig.update_layout(barmode='group')
            
        fig.update_layout(
            title=title,
            yaxis_title="Tỷ lệ phần trăm (%)",
            height=300,
            margin=dict(l=10, r=10, t=65, b=10),
            legend=dict(orientation="h", y=1.1, x=0)
        )
        return _apply_cozy_theme(fig)

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.plotly_chart(draw_use_charts('P3M', "Q3.P3M: Đã dùng trong 3 tháng (%)"), use_container_width=True, config={"displayModeBar": False})
    with r2c2:
        st.plotly_chart(draw_use_charts('P4W', "Q4.P4W: Đã dùng trong 4 tuần (%)"), use_container_width=True, config={"displayModeBar": False})
    with r2c3:
        st.plotly_chart(draw_use_charts('BUMO', "Q5.BUMO: Uống thường xuyên nhất (%)"), use_container_width=True, config={"displayModeBar": False})

    # ===== 5. PHỄU CHUYỂN ĐỔI SỨC KHỎE THƯƠNG HIỆU (BRAND HEALTH FUNNEL) =====
    st.subheader("🎯 3. Phễu chuyển đổi sức khỏe thương hiệu (Brand Health Funnel)")
    
    # Bộ lọc đa chọn cho biểu đồ Phễu
    funnel_default_brands = ['Trà Cozy đóng chai', 'C2', 'OLong Tea Plus', 'Không Độ']
    all_available_funnel_brands = ['Trà Cozy đóng chai', 'C2', 'OLong Tea Plus', 'Không Độ', 'Dr. Thanh', 'Trà mật ong Boncha', 'Trà TH True Tea', 'Trà Tea Go']
    
    selected_funnel_brands = st.multiselect(
        "Lọc các thương hiệu so sánh trong Phễu:",
        options=all_available_funnel_brands,
        default=funnel_default_brands
    )
    
    stages = ['Aided', 'Consideration', 'P3M', 'P4W', 'BUMO']
    stages_vn = ['Nhận biết (Aided)', 'Cân nhắc (Consideration)', 'Dùng thử (P3M)', 'Thường xuyên (P4W)', 'Trung thành (BUMO)']
    
    funnel_data = {}
    for b in selected_funnel_brands:
        p4w_cols_25 = get_p4w_columns(df_25, b)
        
        aided_val = df_25[f'Q1Q2. Total aided awareness_{b}'].mean() * 100 if f'Q1Q2. Total aided awareness_{b}' in df_25.columns else 0.0
        consider_val = df_25[f'Q4Q8.BRAND CONSIDERATION SET_{b}'].mean() * 100 if f'Q4Q8.BRAND CONSIDERATION SET_{b}' in df_25.columns else 0.0
        p3m_val = df_25[f'Q3. P3M _{b}'].mean() * 100 if f'Q3. P3M _{b}' in df_25.columns else 0.0
        p4w_val = df_25[p4w_cols_25].max(axis=1).mean() * 100 if p4w_cols_25 else 0.0
        bumo_val = (df_25['bumo_master'] == b).mean() * 100
        
        funnel_data[b] = [aided_val, consider_val, p3m_val, p4w_val, bumo_val]
        
    df_funnel = pd.DataFrame(funnel_data, index=stages_vn)
    
    fig_funnel = go.Figure()
    
    # Định nghĩa màu sắc biểu đồ phễu
    funnel_colors = {
        'Trà Cozy đóng chai': '#156835',
        'C2': '#769276',
        'OLong Tea Plus': '#A8C0A8',
        'Không Độ': '#DAEEDA',
        'Dr. Thanh': '#A8A8A8',
        'Trà mật ong Boncha': '#D1E2D1',
        'Trà TH True Tea': '#B5C7B5',
        'Trà Tea Go': '#E0EAE0'
    }
    
    for idx, b in enumerate(selected_funnel_brands):
        color = funnel_colors.get(b, '#8FA98F')
        linewidth = 4.0 if b == 'Trà Cozy đóng chai' else 2.0
        
        fig_funnel.add_trace(go.Scatter(
            x=stages_vn,
            y=df_funnel[b],
            mode='lines+markers+text',
            name=b,
            line=dict(color=color, width=linewidth),
            marker=dict(size=8),
            text=[f"{v:.1f}%" for v in df_funnel[b]],
            textposition="top center" if b == 'Trà Cozy đóng chai' else "bottom center",
            hovertemplate="<b>" + b + "</b><br>Giai đoạn: %{x}<br>Tỷ lệ: %{y:.1f}%<extra></extra>"
        ))
        
    fig_funnel.update_layout(
        title="Quy trình chuyển đổi phễu thương hiệu năm 2025 (%)",
        xaxis_title="Các giai đoạn phễu thương hiệu",
        yaxis_title="Tỷ lệ phần trăm trên tổng mẫu (%)",
        height=400,
        margin=dict(l=10, r=10, t=65, b=10),
        legend=dict(orientation="h", y=1.1, x=0)
    )
    st.plotly_chart(_apply_cozy_theme(fig_funnel), use_container_width=True, config={"displayModeBar": False})

    # ===== 6. TẤM THẺ ĐÚC KẾT CHIẾN LƯỢC (Insight Card) =====
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🧠 NHẬN ĐỊNH SỨC KHỎE THƯƠNG HIỆU COZY — SENIOR ANALYST INSIGHTS:</div>
            <div class="insight-main">
                <ul>
                    <li><strong>Mức độ Nhận biết nền móng vững chắc:</strong> Trà Cozy đóng chai giữ vững vị thế Top 4 thị trường với <strong>Aided Awareness cực cao (91.8%)</strong>, ngang ngửa với Không Độ (92.5%) và bỏ xa các thương hiệu trẻ tuổi. Tuy nhiên, mức độ nhận biết đầu tiên <strong>Top-of-Mind (TOM)</strong> lại rất hạn chế, chỉ đạt <strong>9.3%</strong>. Điều này chứng tỏ Cozy có danh tiếng lâu đời nhưng chưa phải thương hiệu khách hàng "khát là nghĩ tới".</li>
                    <li><strong>Động lực tăng trưởng thâm nhập:</strong> Cozy ghi nhận mức tăng trưởng dương rõ rệt qua hai năm trên cả 3 chỉ số tiêu dùng (P3M: 33.6%, P4W: 27.1%, BUMO: 9.3%). C2 tuy dẫn đầu thị trường nhưng đang bộc lộ xu thế thoái trào mạnh mẽ, mở ra khoảng trống thị phần cho Cozy.</li>
                    <li><strong>Vạch trần "Điểm nghẽn rò rỉ" trên phễu thương hiệu:</strong> Phễu chuyển đổi bộc lộ điểm yếu chết người của Cozy nằm ở chặng chuyển hóa <strong>Aided Awareness ➔ Consideration (Cân nhắc mua)</strong> chỉ đạt <strong>38.4%</strong>. Hơn một nửa khách hàng biết Cozy nhưng không đưa Cozy vào danh sách cân nhắc mua sắm hàng ngày!</li>
                    <li><strong>Trải nghiệm sản phẩm dẫn đầu thị trường:</strong> Tuy nhiên, một khi khách hàng chịu đưa Cozy vào bộ cân nhắc, tỷ lệ dùng thử thực tế <strong>Consideration ➔ P3M</strong> đạt mức kinh ngạc **94.1%**, dẫn đầu tuyệt đối toàn bộ thị trường nước giải khát. Điều này chứng minh <strong>chất lượng sản phẩm Cozy cực tốt</strong> và hoàn toàn đủ sức giữ chân người tiêu dùng một khi họ vượt qua rào cản cân nhắc ban đầu.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
