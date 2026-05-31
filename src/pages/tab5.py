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

def render_tab5(df: pd.DataFrame) -> None:
    # 1. RENDER BỘ LỌC ĐỘNG TRÊN SIDEBAR
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</h3>", unsafe_allow_html=True)
    
    barriers_base = st.sidebar.selectbox("Tệp đáp viên (Base)", options=["Người nhận biết nhưng chưa cân nhắc", "Tổng số đáp viên"], index=0)
    
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>THƯƠNG HIỆU SO SÁNH</p>", unsafe_allow_html=True)
    cozy_sel = st.sidebar.checkbox("Cozy", value=True, key="br_cozy")
    c2_sel = st.sidebar.checkbox("C2", value=True, key="br_c2")
    tp_sel = st.sidebar.checkbox("Tea Plus", value=True, key="br_tp")
    kd_sel = st.sidebar.checkbox("Không Độ", value=True, key="br_kd")
    
    region_map = {
        "Tất cả": "All",
        "Miền Bắc": "North",
        "Miền Trung": "Central",
        "Miền Nam": "South",
        "ĐBSCL (Mekong)": "Mekong"
    }
    region_sel_vn = st.sidebar.selectbox("Khu vực", options=list(region_map.keys()), index=0)
    region_sel = region_map[region_sel_vn]

    # Danh sách thương hiệu được chọn
    selected_brands = []
    if cozy_sel: selected_brands.append('Trà Cozy đóng chai')
    if c2_sel: selected_brands.append('C2')
    if tp_sel: selected_brands.append('OLong Tea Plus')
    if kd_sel: selected_brands.append('Không Độ')

    if not selected_brands:
        st.warning("Vui lòng chọn ít nhất một Thương hiệu ở Sidebar!")
        return

    # Lọc DataFrame theo vùng miền
    if region_sel != "All":
        df_filtered = df[df['region'] == region_sel]
    else:
        df_filtered = df

    # Phân tách Wave
    df_25 = df_filtered[df_filtered['wave'] == 2025]
    df_24 = df_filtered[df_filtered['wave'] == 2024]

    # Map rào cản tiếng Việt (đầy đủ theo dữ liệu thực tế)
    barrier_mapper = {
        'Do not like the flavor/The flavor do not taste good': 'Không thích vị / không ngon',
        'Do not like the flavor / The flavor do not taste good': 'Không thích vị / không ngon',
        'Does not have enough flavour that I want to choose': 'Nghèo nàn sự lựa chọn vị',
        'Does not have enough flavor choice': 'Nghèo nàn danh mục vị',
        'Asked but the store does not sell it': 'Hỏi mua nhưng không bán',
        'Not preserved in cool place': 'Không được ướp lạnh sẵn',
        'Do not like recent packaging designs': 'Không thích thiết kế bao bì gần đây',
        'Does not elegant, premium': 'Thiếu sang trọng / cao cấp',
        'The design of packaging is not attractive': 'Bao bì không thu hút',
        'Bad quality': 'Chất lượng không tốt',
        'Do not trust in product quality': 'Không tin tưởng chất lượng sản phẩm',
        'Price is too expensive/not suitable': 'Giá đắt/không phù hợp',
        'Price is too expensive / not suitable': 'Giá đắt/không phù hợp',
        'Expensive than I expected': 'Giá đắt hơn kỳ vọng',
        'Too cheap': 'Giá rẻ quá (nghi ngờ chất lượng)',
        'Do not trust the brand': 'Không tin tưởng thương hiệu',
        'Unhealthy': 'Lo ngại về sức khỏe (không lành mạnh)',
        'Has higher sugar than I needed': 'Hàm lượng đường quá cao',
        'Too sweet': 'Vị trà quá ngọt',
        'Usually do not have sale promotion while other brands have': 'Ít khuyến mãi hơn đối thủ',
        'Do not want other people see when I drink/buy this brand': 'Ngại bị nhìn thấy khi dùng',
        'Unpopular brands': 'Thương hiệu kém phổ biến',
        'None': 'Không gặp rào cản',
        'None of these': 'Không gặp rào cản'
    }

    # Hàm tính toán rào cản động cho thương hiệu focal
    def get_barriers_data(d, brand):
        cozy_barrier_cols = [c for c in d.columns if f'QME2 - {brand}' in c]
        barriers_pct = {}
        
        if barriers_base == "Người nhận biết nhưng chưa cân nhắc":
            target_resp = d[
                (d[f'Q1Q2. Total aided awareness_{brand}'] == 1) &
                (d[f'Q4Q8.BRAND CONSIDERATION SET_{brand}'] == 0)
            ]
        else:
            target_resp = d
            
        for col in cozy_barrier_cols:
            b_name = col.split('_')[-1]
            barriers_pct[barrier_mapper.get(b_name, b_name)] = target_resp[col].mean() * 100 if len(target_resp) > 0 else 0.0
        return pd.Series(barriers_pct).sort_values(ascending=False)

    focal_brand = 'Trà Cozy đóng chai'
    df_barriers_25 = get_barriers_data(df_25, focal_brand)
    df_barriers_24 = get_barriers_data(df_24, focal_brand)

    # Đảm bảo index khớp nhau để so sánh
    all_barriers = df_barriers_25.index
    df_barriers_24 = df_barriers_24.reindex(all_barriers, fill_value=0.0)

    # KPI calculations
    top_barrier_name = df_barriers_25.index[0] if not df_barriers_25.empty else "Nghèo nàn vị"
    top_barrier_val = df_barriers_25.values[0] if not df_barriers_25.empty else 0.0
    top_barrier_24 = df_barriers_24.loc[top_barrier_name] if top_barrier_name in df_barriers_24.index else 0.0
    top_barrier_delta = top_barrier_val - top_barrier_24

    dist_barrier_val = df_barriers_25.get('Hỏi mua nhưng không bán', 0.0)
    cool_barrier_val = df_barriers_25.get('Không được ướp lạnh sẵn', 0.0)
    
    cozy_aware_non_con = (
        (df_25[f'Q1Q2. Total aided awareness_{focal_brand}'] == 1) &
        (df_25[f'Q4Q8.BRAND CONSIDERATION SET_{focal_brand}'] == 0)
    ).sum()

    # Precalculate dynamic BUMO switching source for Cozy
    df_cozy_bumo = df_25[df_25['bumo_master'] == 'Trà Cozy đóng chai']
    top_switch_name = "Không xác định"
    top_switch_val = 0.0
    switching_source_sorted = pd.Series(dtype=float)
    
    if len(df_cozy_bumo) > 0:
        switching_source = df_cozy_bumo['Q7. Previous BUMO'].value_counts(normalize=True) * 100
        brand_vn_map = {
            'OLong Tea Plus': 'Trà Ô long Tea Plus',
            'Không Độ': 'Trà xanh Không Độ',
            'Trà Cozy đóng chai': 'Trà Cozy đóng chai',
            'Trà Tea Go': 'Trà Tea Go',
            'Trà mật ong Boncha': 'Trà mật ong Boncha'
        }
        switching_source.index = [brand_vn_map.get(str(x), str(x)) for x in switching_source.index]
        switching_source_sorted = switching_source.sort_values(ascending=True)
        if not switching_source_sorted.empty:
            top_switch_name = switching_source_sorted.index[-1]
            top_switch_val = switching_source_sorted.values[-1]

    # Title & Subtitle
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #156835; margin: 0; font-size: 1.6rem; font-weight: 800;">Phân tích Rào cản & Nguồn chuyển đổi — Cozy vs C2 + Đối thủ</h2>
            <p style="color: #4e6556; font-size: 0.9rem; margin-top: 4px; margin-bottom: 20px;">
                Căn cứ (Base): {barriers_base} • Khu vực lọc: {region_sel} • Rào cản hàng đầu: {top_barrier_name} ({top_barrier_val:.1f}%)
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. HÀNG KPI CARDS
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">RÀO CẢN SỐ 1 (HƯƠNG Vị)</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #b25e5e; line-height: 1.2;">Nghèo nàn vị</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{top_barrier_val:.1f}% <span style="font-size:0.75rem; color:#b25e5e; font-weight:bold;">{top_barrier_delta:+.1f}pp ▲</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">RÀO CẢN PHÂN PHỐI</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #b25e5e; line-height: 1.2;">Hỏi mua không bán</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{dist_barrier_val:.1f}% <span style="font-size:0.75rem; color:#b25e5e; font-weight:bold;">Nút thắt kênh</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">NGUỒN CHUYỂN ĐỔI CHỦ YẾU</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #156835; line-height: 1.2;">{top_switch_name}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{top_switch_val:.1f}% chuyển dịch <span style="font-size:0.75rem; color:#156835; font-weight:bold;">BUMO</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">CỠ MẪU KHÔNG CÂN NHẮC</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_aware_non_con}</div>
                <div style="font-size: 0.75rem; color: #8fa98f; font-weight: 600; margin-top: 8px;">Đáp viên bỏ qua Cozy</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. KHUNG BIỂU ĐỒ SONG SONG 2 BÊN
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Tỉ lệ các rào cản từ chối mua Cozy RTD (%)</div>", unsafe_allow_html=True)
        
        top_6_barriers = df_barriers_25.head(6)
        
        fig_barriers = go.Figure()
        fig_barriers.add_trace(go.Bar(
            y=top_6_barriers.index,
            x=df_barriers_24.loc[top_6_barriers.index],
            name='Wave 2024',
            orientation='h',
            marker_color='#d8a4a4', # Tông màu terracotta nhạt cho Wave 24
            text=[f"{v:.1f}%" for v in df_barriers_24.loc[top_6_barriers.index]],
            textposition='inside'
        ))
        fig_barriers.add_trace(go.Bar(
            y=top_6_barriers.index,
            x=top_6_barriers.values,
            name='Wave 2025',
            orientation='h',
            marker_color='#b25e5e', # Tông màu terracotta đậm cho Wave 25 (Focal)
            text=[f"{v:.1f}%" for v in top_6_barriers.values],
            textposition='inside'
        ))
        
        fig_barriers.update_layout(
            barmode='group',
            height=320,
            xaxis_title="Tỷ lệ rào cản (%)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(_apply_cozy_theme(fig_barriers), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Rào cản '{top_barrier_name}' của Cozy lớn nhất ở mức {top_barrier_val:.1f}% ({top_barrier_delta:+.1f}pp vs W24) do thiếu hụt sự đa dạng vị; nhãn hàng cần đẩy mạnh sampling tại điểm bán để giảm tỷ lệ rào cản xuống dưới 20% vào Wave 2026.</div>", unsafe_allow_html=True)

    with col_right:
        if len(df_cozy_bumo) > 0 and not switching_source_sorted.empty:
            st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Nguồn chuyển dịch thương hiệu ưu tiên BUMO Cozy (%)</div>", unsafe_allow_html=True)
            
            fig_switch = go.Figure(go.Bar(
                y=switching_source_sorted.index,
                x=switching_source_sorted.values,
                orientation='h',
                marker_color='#9e9e9e',
                text=[f"{v:.1f}%" for v in switching_source_sorted.values],
                textposition='outside'
            ))
            fig_switch.update_layout(
                height=320,
                xaxis_title="Tỷ lệ phần trăm (%)"
            )
            st.plotly_chart(_apply_cozy_theme(fig_switch), use_container_width=True, config={"displayModeBar": False})
            st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Có {top_switch_val:.1f}% nguồn chuyển dịch Cozy BUMO đến từ {top_switch_name}; Cozy nên triển khai các gói dùng thử kèm ưu đãi để thu hút thêm 10% nhóm khách hàng này ở Wave 2026.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Nguồn chuyển dịch thương hiệu ưu tiên BUMO Cozy (%)</div>", unsafe_allow_html=True)
            st.warning("Không có đủ mẫu người dùng Cozy BUMO để phân tích chuyển dịch.")

    st.divider()

    # 4. BẢNG ĐỐI SÁNH CHI TIẾT CHÂN TRANG
    st.markdown("<div style='font-weight: 800; font-size: 1.1rem; color: #156835; margin-bottom: 10px;'>Bảng đối sánh chi tiết biến động Rào cản Cozy (%)</div>", unsafe_allow_html=True)
    
    rows_html = ""
    for short_name in df_barriers_25.index:
        v_25 = df_barriers_25.loc[short_name]
        v_24 = df_barriers_24.loc[short_name]
        diff_v = v_25 - v_24
        
        diff_class = "delta-red-txt" if diff_v >= 0 else "delta-green-txt"
        diff_str = f"{'+' if diff_v >= 0 else ''}{diff_v:.1f}pp"
        
        rows_html += f"""<tr>
<td style="text-align: left; padding-left: 20px;">{short_name}</td>
<td>{v_24:.1f}%</td>
<td>{v_25:.1f}%</td>
<td class="{diff_class}">{diff_str}</td>
</tr>"""

    table_html = f"""<style>
.barrier-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(21, 104, 53, 0.15);
    box-shadow: 0 4px 15px rgba(21, 104, 53, 0.02);
}}
.barrier-table th {{
    background: linear-gradient(135deg, #156835 0%, #0d4622 100%);
    color: white;
    text-align: center;
    padding: 14px 16px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}}
.barrier-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(21, 104, 53, 0.08);
    color: #1b2e22;
    font-size: 0.88rem;
    text-align: center;
    font-weight: 500;
}}
.barrier-table tr:last-child td {{
    border-bottom: none;
}}
.barrier-table tr:nth-child(even) {{
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
<table class="barrier-table">
<thead>
<tr>
<th style="text-align: left; padding-left: 20px;">DANH SÁCH CÁC RÀO CẢN TỪ CHỐI COZY</th>
<th>TỶ LỆ WAVE 2024</th>
<th>TỶ LỆ WAVE 2025</th>
<th>BIẾN ĐỘNG CHỈ SỐ (Δ)</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>"""
    st.markdown(table_html, unsafe_allow_html=True)
