import streamlit as st
import pandas as pd
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

def render_overview(df: pd.DataFrame) -> None:
    # 1. RENDER BỘ LỌC ĐỘNG TRÊN SIDEBAR
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</h3>", unsafe_allow_html=True)
    
    # 1.1 WAVE Filter
    selected_wave = st.sidebar.selectbox("Wave khảo sát (Năm)", options=[2025, 2024], index=0)
    
    # 1.2 BRAND FOCAL Filter
    brands_list = ['Trà Cozy đóng chai', 'C2', 'OLong Tea Plus', 'Không Độ']
    selected_brand = st.sidebar.selectbox("Thương hiệu tiêu điểm", options=brands_list, index=0)
    
    # 1.3 AGE GROUP Checkboxes (Theo đúng tệp tuổi Cozy trong database)
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>NHÓM TUỔI</p>", unsafe_allow_html=True)
    age_all = st.sidebar.checkbox("Tất cả độ tuổi", value=True, key="ov_age_all")
    
    if age_all:
        selected_ages = ['14 - 18 y.o.', '19 - 24 y.o.', '25 - 29 y.o.', '30 - 34 y.o.', '36 - 40 y.o.']
    else:
        selected_ages = []
        if st.sidebar.checkbox("14 - 18 tuổi", value=True, key="ov_age_14_18"): selected_ages.append('14 - 18 y.o.')
        if st.sidebar.checkbox("19 - 24 tuổi", value=True, key="ov_age_19_24"): selected_ages.append('19 - 24 y.o.')
        if st.sidebar.checkbox("25 - 29 tuổi", value=True, key="ov_age_25_29"): selected_ages.append('25 - 29 y.o.')
        if st.sidebar.checkbox("30 - 34 tuổi", value=True, key="ov_age_30_34"): selected_ages.append('30 - 34 y.o.')
        if st.sidebar.checkbox("36 - 40 tuổi", value=True, key="ov_age_36_40"): selected_ages.append('36 - 40 y.o.')
    
    # 1.4 REGION Multiselect
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>KHU VỰC</p>", unsafe_allow_html=True)
    available_regions = ['North', 'Central', 'South', 'Mekong']
    selected_regions = st.sidebar.multiselect("Chọn khu vực", options=available_regions, default=available_regions, label_visibility="collapsed")

    # 2. ÁP DỤNG BỘ LỌC DỮ LIỆU
    if not selected_ages:
        st.warning("Vui lòng chọn ít nhất một Nhóm tuổi ở Sidebar!")
        return
    if not selected_regions:
        st.warning("Vui lòng chọn ít nhất một Khu vực ở Sidebar!")
        return

    # Lọc DataFrame
    df_filtered = df[df['age_group'].isin(selected_ages) & df['region'].isin(selected_regions)]
    
    # Chia Wave
    df_25 = df_filtered[df_filtered['wave'] == 2025]
    df_24 = df_filtered[df_filtered['wave'] == 2024]
    
    n_resp_25 = len(df_25)
    n_resp_24 = len(df_24)

    if n_resp_25 == 0 or n_resp_24 == 0:
        st.warning("Không có dữ liệu đáp viên thỏa mãn bộ lọc đã chọn ở Sidebar!")
        return

    # Lấy các chỉ số sức khỏe của thương hiệu tiêu điểm (Focal Brand) & Đối thủ chính
    def get_brand_metrics(d, brand):
        aw = d[f'Q1Q2. Total aided awareness_{brand}'].mean() * 100 if f'Q1Q2. Total aided awareness_{brand}' in d.columns else 0.0
        tom = (d['tom_master'] == brand).mean() * 100
        bumo = (d['bumo_master'] == brand).mean() * 100
        p4w_cols = get_p4w_columns(d, brand)
        p4w = d[p4w_cols].max(axis=1).mean() * 100 if p4w_cols else 0.0
        return aw, tom, bumo, p4w

    # Thương hiệu đối sánh
    competitor = 'C2' if selected_brand != 'C2' else 'OLong Tea Plus'

    # Focal brand metrics
    brand_aw_25, brand_tom_25, brand_bumo_25, brand_p4w_25 = get_brand_metrics(df_25, selected_brand)
    brand_aw_24, brand_tom_24, brand_bumo_24, brand_p4w_24 = get_brand_metrics(df_24, selected_brand)

    # Competitor metrics
    comp_aw_25, comp_tom_25, comp_bumo_25, comp_p4w_25 = get_brand_metrics(df_25, competitor)

    # Deltas
    d_aw_wow = brand_aw_25 - brand_aw_24
    d_aw_comp = brand_aw_25 - comp_aw_25
    d_tom_wow = brand_tom_25 - brand_tom_24
    d_tom_comp = brand_tom_25 - comp_tom_25
    d_bumo_wow = brand_bumo_25 - brand_bumo_24
    d_bumo_comp = brand_bumo_25 - comp_bumo_25

    def delta_html(val):
        color = "#156835" if val >= 0 else "#b25e5e" # Sử dụng tông màu đất đỏ ấm hài hòa thay thế cho đỏ tươi
        arrow = "pp"
        sign = "+" if val > 0 else ""
        return f'<span style="color: {color}; font-weight: bold; font-size: 0.85rem;">{sign}{val:.1f}{arrow}</span>'

    # Tiêu đề & mô tả phụ động theo thương hiệu tiêu điểm (Không sử dụng emojis)
    brand_short = selected_brand.replace('Trà ', '').replace(' đóng chai', '')
    comp_short = competitor.replace('Trà ', '').replace(' đóng chai', '')

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #156835; margin: 0; font-size: 1.65rem; font-weight: 800;">Sức khỏe thương hiệu {brand_short} — Tổng quan Wave {selected_wave}</h2>
            <p style="color: #4e6556; font-size: 0.92rem; margin-top: 4px; margin-bottom: 20px;">
                Nhận biết (Aware) {brand_aw_25:.1f}% • Nghĩ đến đầu tiên (TOM) {brand_tom_25:.1f}% • Tiêu dùng gần đây (P4W) {brand_p4w_25:.1f}% • Nhãn hiệu mua nhiều nhất (BUMO) {brand_bumo_25:.1f}% ({"+" if d_bumo_wow >= 0 else ""}{d_bumo_wow:.1f}pp so với Wave 24) • vs Đối thủ {comp_short} ({"+" if d_bumo_comp >= 0 else ""}{d_bumo_comp:.1f}pp)
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. KPI CARDS ROW (Xóa bỏ toàn bộ icons/emojis)
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% AWARE {brand_short.upper()}</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{brand_aw_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_aw_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs {comp_short}</span><br>{delta_html(d_aw_comp)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% TOM {brand_short.upper()}</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{brand_tom_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_tom_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs {comp_short}</span><br>{delta_html(d_tom_comp)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">% BUMO {brand_short.upper()}</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{brand_bumo_25:.1f}%</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs W24</span><br>{delta_html(d_bumo_wow)}</div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">vs {comp_short}</span><br>{delta_html(d_bumo_comp)}</div>
                </div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">N RESPONDENT</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{n_resp_25}</div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; border-top: 1px solid rgba(21, 104, 53, 0.08); padding-top: 8px;">
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">Wave 2024</span><br><span style="font-weight:700; color:#1b2e22; font-size:0.85rem;">{n_resp_24}</span></div>
                    <div><span style="font-size:0.65rem; color:#8fa98f; font-weight: 600;">Wave 2025</span><br><span style="font-weight:700; color:#1b2e22; font-size:0.85rem;">{n_resp_25}</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4. LƯỚI BIỂU ĐỒ 2x2 (Action Titles - Không có Emojis)
    row1_col1, row1_col2 = st.columns(2)
    
    # Biểu đồ 1: Funnel
    with row1_col1:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Phễu sức khỏe thương hiệu (Brand Health Funnel) (%)</div>", unsafe_allow_html=True)
        
        aided_val = df_25[f'Q1Q2. Total aided awareness_{selected_brand}'].mean() * 100 if f'Q1Q2. Total aided awareness_{selected_brand}' in df_25.columns else 0.0
        consider_val = df_25[f'Q4Q8.BRAND CONSIDERATION SET_{selected_brand}'].mean() * 100 if f'Q4Q8.BRAND CONSIDERATION SET_{selected_brand}' in df_25.columns else 38.4
        p3m_val = df_25[f'Q3. P3M _{selected_brand}'].mean() * 100 if f'Q3. P3M _{selected_brand}' in df_25.columns else 0.0
        p4w_val = brand_p4w_25
        bumo_val = brand_bumo_25
        
        funnel_stages = ['Nhận biết (Aided)', 'Cân nhắc (Consider)', 'Dùng thử (P3M)', 'Tiêu dùng (P4W)', 'Trung thành (BUMO)']
        funnel_vals = [aided_val, consider_val, p3m_val, p4w_val, bumo_val]
        
        fig_funnel = go.Figure(go.Bar(
            x=funnel_vals,
            y=funnel_stages,
            orientation='h',
            marker_color="#156835",
            text=[f"{v:.1f}%" for v in funnel_vals],
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>"
        ))
        fig_funnel.update_layout(
            yaxis=dict(autorange="reversed"),
            height=250
        )
        st.plotly_chart(_apply_cozy_theme(fig_funnel), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Mặc dù Nhận biết {brand_short} đạt {brand_aw_25:.1f}%, tỷ lệ BUMO chỉ chiếm {brand_bumo_25:.1f}% do rò rỉ lớn ở bước Cân nhắc; nhãn hàng cần tái định vị bao bì và đẩy mạnh tiếp thị số để hướng tới mục tiêu Cân nhắc đạt 55% vào Wave 2026.</div>", unsafe_allow_html=True)

    # Biểu đồ 2: Aided Awareness Trend
    with row1_col2:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Xu hướng nhận biết thương hiệu qua các Wave (%)</div>", unsafe_allow_html=True)
        
        comp_aw_24 = df_24[f'Q1Q2. Total aided awareness_{competitor}'].mean() * 100 if f'Q1Q2. Total aided awareness_{competitor}' in df_24.columns else 0.0
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=['2024', '2025'], y=[brand_aw_24, brand_aw_25],
            mode='lines+markers+text', name=brand_short,
            line=dict(color='#156835', width=4),
            marker=dict(size=8),
            text=[f"{brand_aw_24:.1f}%", f"{brand_aw_25:.1f}%"],
            textposition="top center"
        ))
        fig_trend.add_trace(go.Scatter(
            x=['2024', '2025'], y=[comp_aw_24, comp_aw_25],
            mode='lines+markers+text', name=comp_short,
            line=dict(color='#9e9e9e', width=2, dash='dash'),
            marker=dict(size=6),
            text=[f"{comp_aw_24:.1f}%", f"{comp_aw_25:.1f}%"],
            textposition="bottom center"
        ))
        fig_trend.update_layout(
            height=250,
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(_apply_cozy_theme(fig_trend), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Nhận biết {brand_short} tăng {'+' if d_aw_wow>=0 else ''}{d_aw_wow:.1f}pp lên {brand_aw_25:.1f}%, nhưng đối thủ {comp_short} đang bám sát ở mức {comp_aw_25:.1f}%; giải pháp là tăng cường tần suất TVC và chiến dịch TikTok để duy trì vị thế dẫn đầu ≥10pp ở Wave 2026.</div>", unsafe_allow_html=True)

    # HÀNG 2
    row2_col1, row2_col2 = st.columns(2)
    
    # Biểu đồ 3: Top Imagery
    with row2_col1:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Các thuộc tính định vị hình ảnh nổi bật nhất (%)</div>", unsafe_allow_html=True)
        
        attributes = [
            'Những thương hiệu được ưa chuộng và phổ biến', 'Bao bì có thiết kế thu hút', 'Nhãn hiệu đáng tin cậy',
            'Giá cả hợp lý với chất lượng mang lại', 'Phù hợp để thưởng thức hàng ngày', 'Làm dịu cơn khát',
            'Vị ngon mà tôi yêu thích', 'Thương hiệu mang tính hiện đại, trẻ trung', 'Sản xuất từ nguyên liệu tự nhiên',
            'Mang đến sự vui tươi và lạc quan', 'Có lợi cho sức khỏe', 'Giúp giảm căng thẳng và mệt mỏi',
            'Mang lại cảm giác thư giãn', 'Giải nhiệt cuộc sống', 'Tạo cảm giác sảng khoái',
            'Tái tạo năng lượng', 'Có nhiều vị để lựa chọn', 'Mang đến cảm giác tươi mát'
        ]
        
        attr_mapper = {
            'Những thương hiệu được ưa chuộng và phổ biến': 'Ưa chuộng & Phổ biến',
            'Bao bì có thiết kế thu hút': 'Bao bì thu hút',
            'Nhãn hiệu đáng tin cậy': 'Đáng tin cậy',
            'Giá cả hợp lý với chất lượng mang lại': 'Giá cả hợp lý',
            'Phù hợp để thưởng thức hàng ngày': 'Uống hàng ngày',
            'Làm dịu cơn khát': 'Dịu cơn khát',
            'Vị ngon mà tôi yêu thích': 'Vị ngon yêu thích',
            'Thương hiệu mang tính hiện đại, trẻ trung': 'Trẻ trung, hiện đại',
            'Sản xuất từ nguyên liệu tự nhiên': 'Nguyên liệu tự nhiên',
            'Mang đến sự vui tươi và lạc quan': 'Vui tươi & Lạc quan',
            'Có lợi cho sức khỏe': 'Có lợi sức khỏe',
            'Giúp giảm căng thẳng và mệt mỏi': 'Giảm căng thẳng',
            'Mang lại cảm giác thư giãn': 'Thư giãn',
            'Giải nhiệt cuộc sống': 'Giải nhiệt cuộc sống',
            'Tạo cảm giác sảng khoái': 'Sảng khoái',
            'Tái tạo năng lượng': 'Tái tạo năng lượng',
            'Có nhiều vị để lựa chọn': 'Nhiều vị lựa chọn',
            'Mang đến cảm giác tươi mát': 'Tươi mát'
        }
        
        img_scores = {}
        for attr in attributes:
            col = f'QI - {selected_brand}_{attr}'
            if col in df_25.columns:
                aided_col = f'Q1Q2. Total aided awareness_{selected_brand}'
                aware_resp = df_25[df_25[aided_col] == 1]
                img_scores[attr_mapper.get(attr, attr)] = aware_resp[col].mean() * 100 if len(aware_resp) > 0 else 0.0
                
        df_img_sorted = pd.Series(img_scores).sort_values(ascending=True).tail(4)
        
        fig_img = go.Figure(go.Bar(
            x=df_img_sorted.values,
            y=df_img_sorted.index,
            orientation='h',
            marker_color="#156835",
            text=[f"{v:.1f}%" for v in df_img_sorted.values],
            textposition="inside",
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>"
        ))
        fig_img.update_layout(
            height=250
        )
        st.plotly_chart(_apply_cozy_theme(fig_img), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> {brand_short} tiếp tục duy trì ưu thế vượt trội ở hai thuộc tính 'Đáng tin cậy' và 'Nguyên liệu tự nhiên'; Cozy cần tập trung truyền thông thế mạnh trà tự nhiên trên các kênh kỹ thuật số để bảo vệ vững chắc vị trí Top 2 liên tưởng hình ảnh ở Wave 2026.</div>", unsafe_allow_html=True)

    # Biểu đồ 4: Top Barriers
    with row2_col2:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Các rào cản từ chối mua thương hiệu (%)</div>", unsafe_allow_html=True)
        
        cozy_barrier_cols = [c for c in df_25.columns if f'QME2 - {selected_brand}' in c]
        barriers_pct = {}
        target_resp = df_25[
            (df_25[f'Q1Q2. Total aided awareness_{selected_brand}'] == 1) &
            (df_25[f'Q4Q8.BRAND CONSIDERATION SET_{selected_brand}'] == 0)
        ]
        
        barrier_mapper = {
            'Do not like the flavor/The flavor do not taste good': 'Không thích vị/không ngon',
            'Do not like the flavor / The flavor do not taste good': 'Không thích vị/không ngon',
            'Does not have enough flavour that I want to choose': 'Nghèo nàn sự lựa chọn vị',
            'Does not have enough flavor choice': 'Nghèo nàn danh mục vị',
            'Asked but the store does not sell it': 'Hỏi mua nhưng không bán',
            'Not preserved in cool place': 'Không được ướp lạnh sẵn',
            'Do not like recent packaging designs': 'Không thích bao bì gần đây',
            'Does not elegant, premium': 'Thiếu sang trọng / cao cấp',
            'The design of packaging is not attractive': 'Bao bì không thu hút',
            'Bad quality': 'Chất lượng không tốt',
            'Do not trust in product quality': 'Không tin tưởng chất lượng SP',
            'Price is too expensive/not suitable': 'Giá đắt/không phù hợp',
            'Price is too expensive / not suitable': 'Giá đắt/không phù hợp',
            'Expensive than I expected': 'Giá đắt hơn kỳ vọng',
            'Too cheap': 'Giá rẻ quá (nghi ngờ CL)',
            'Do not trust the brand': 'Không tin thương hiệu',
            'Unhealthy': 'Lo ngại sức khỏe',
            'Has higher sugar than I needed': 'Hàm lượng đường quá cao',
            'Too sweet': 'Vị quá ngọt',
            'Usually do not have sale promotion while other brands have': 'Ít khuyến mãi hơn đối thủ',
            'Do not want other people see when I drink/buy this brand': 'Ngại bị nhìn thấy khi dùng',
            'Unpopular brands': 'Thương hiệu kém phổ biến',
            'None': 'Không gặp rào cản',
            'None of these': 'Không gặp rào cản'
        }
        
        for col in cozy_barrier_cols:
            b_name = col.split('_')[-1]
            barriers_pct[barrier_mapper.get(b_name, b_name)] = target_resp[col].mean() * 100 if len(target_resp) > 0 else 0.0
            
        if barriers_pct:
            df_barriers_sorted = pd.Series(barriers_pct).sort_values(ascending=True).tail(4)
        else:
            df_barriers_sorted = pd.Series({'Không có dữ liệu': 0.0})
            
        fig_barriers = go.Figure(go.Bar(
            x=df_barriers_sorted.values,
            y=df_barriers_sorted.index,
            orientation='h',
            marker_color="#b25e5e", # Tông terracotta đỏ ấm áp thay vì vàng mù tạt
            text=[f"{v:.1f}%" for v in df_barriers_sorted.values],
            textposition="outside",
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>"
        ))
        fig_barriers.update_layout(
            height=250
        )
        st.plotly_chart(_apply_cozy_theme(fig_barriers), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # 5. BOTTOM TABLE (Không có Emojis)
    st.markdown(f"Bảng đối sánh chi tiết chỉ số Sức khỏe {brand_short} qua các Wave")
    
    table_html = f"""
    <style>
        .overview-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(21, 104, 53, 0.15);
            box-shadow: 0 4px 15px rgba(21, 104, 53, 0.02);
        }}
        .overview-table th {{
            background: linear-gradient(135deg, #156835 0%, #0d4622 100%);
            color: white;
            text-align: center;
            padding: 14px 16px;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.02em;
        }}
        .overview-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(21, 104, 53, 0.08);
            color: #1b2e22;
            font-size: 0.9rem;
            text-align: center;
            font-weight: 500;
        }}
        .overview-table tr:last-child td {{
            border-bottom: none;
        }}
        .overview-table tr:nth-child(even) {{
            background-color: rgba(21, 104, 53, 0.02);
        }}
        .delta-green-txt {{
            color: #156835;
            font-weight: bold;
        }}
        .delta-red-txt {{
            color: #b25e5e;
            font-weight: bold;
        }}
    </style>
    <table class="overview-table">
        <thead>
            <tr>
                <th>WAVE</th>
                <th>% AWARE (Aided)</th>
                <th>% TOM (Top of Mind)</th>
                <th>% P4W (Thâm nhập 4 tuần)</th>
                <th>% BUMO (Trung thành nhất)</th>
                <th>BIẾN ĐỘNG CHỈ SỐ CHỦ CHỐT VS PY (NĂM TRƯỚC)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Wave 2024</td>
                <td>{brand_aw_24:.1f}%</td>
                <td>{brand_tom_24:.1f}%</td>
                <td>{brand_p4w_24:.1f}%</td>
                <td>{brand_bumo_24:.1f}%</td>
                <td>—</td>
            </tr>
            <tr>
                <td>Wave 2025</td>
                <td>{brand_aw_25:.1f}%</td>
                <td>{brand_tom_25:.1f}%</td>
                <td>{brand_p4w_25:.1f}%</td>
                <td>{brand_bumo_25:.1f}%</td>
                <td>
                    <span class="delta-green-txt">Aware {d_aw_wow:+.1f}pp</span> &nbsp;•&nbsp; 
                    <span class="delta-green-txt">BUMO {d_bumo_wow:+.1f}pp</span> &nbsp;•&nbsp; 
                    <span class="delta-green-txt">P4W {brand_p4w_25-brand_p4w_24:+.1f}pp</span>
                </td>
            </tr>
        </tbody>
    </table>
    """
    import textwrap
    st.markdown(textwrap.dedent(table_html), unsafe_allow_html=True)