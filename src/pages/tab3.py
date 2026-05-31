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

def render_tab3(df: pd.DataFrame) -> None:
    # 1. RENDER BỘ LỌC ĐỘNG TRÊN SIDEBAR
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</h3>", unsafe_allow_html=True)
    
    imagery_base = st.sidebar.selectbox("Tệp đáp viên (Base)", options=["Người nhận biết thương hiệu", "Tổng số đáp viên"], index=0)
    
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>THƯƠNG HIỆU SO SÁNH</p>", unsafe_allow_html=True)
    cozy_sel = st.sidebar.checkbox("Cozy", value=True, key="im_cozy")
    c2_sel = st.sidebar.checkbox("C2", value=True, key="im_c2")
    tp_sel = st.sidebar.checkbox("Tea Plus", value=True, key="im_tp")
    kd_sel = st.sidebar.checkbox("Không Độ", value=True, key="im_kd")
    
    show_as = st.sidebar.selectbox("Hiển thị dưới dạng", options=["Tỷ lệ phần trăm (%)", "Điểm trung bình (1-5)"], index=0)

    # Lập danh sách thương hiệu so sánh
    selected_brands = []
    if cozy_sel: selected_brands.append('Trà Cozy đóng chai')
    if c2_sel: selected_brands.append('C2')
    if tp_sel: selected_brands.append('OLong Tea Plus')
    if kd_sel: selected_brands.append('Không Độ')

    if not selected_brands:
        st.warning("Vui lòng chọn ít nhất một Thương hiệu ở Sidebar!")
        return

    # 2. ĐỊNH NGHĨA 18 THUỘC TÍNH
    attributes_viet = {
        'Những thương hiệu được ưa chuộng và phổ biến': '1. Được ưa chuộng & Phổ biến',
        'Bao bì có thiết kế thu hút': '2. Thiết kế bao bì thu hút',
        'Nhãn hiệu đáng tin cậy': '3. Nhãn hiệu đáng tin cậy',
        'Giá cả hợp lý với chất lượng mang lại': '4. Giá cả hợp lý với chất lượng',
        'Phù hợp để thưởng thức hàng ngày': '5. Phù hợp uống hàng ngày',
        'Làm dịu cơn khát': '6. Làm dịu cơn khát',
        'Vị ngon mà tôi yêu thích': '7. Vị ngon yêu thích',
        'Thương hiệu mang tính hiện đại, trẻ trung': '8. Trẻ trung, hiện đại',
        'Sản xuất từ nguyên liệu tự nhiên': '9. Nguyên liệu tự nhiên',
        'Mang đến sự vui tươi và lạc quan': '10. Vui tươi & Lạc quan',
        'Có lợi cho sức khỏe': '11. Có lợi cho sức khỏe',
        'Giúp giảm căng thẳng và mệt mỏi': '12. Giảm căng thẳng mệt mỏi',
        'Mang lại cảm giác thư giãn': '13. Cảm giác thư giãn',
        'Giải nhiệt cuộc sống': '14. Giải nhiệt cuộc sống',
        'Tạo cảm giác sảng khoái': '15. Cảm giác sảng khoái',
        'Tái tạo năng lượng': '16. Tái tạo năng lượng',
        'Có nhiều vị để lựa chọn': '17. Nhiều vị lựa chọn',
        'Mang đến cảm giác tươi mát': '18. Cảm giác tươi mát'
    }

    df_25 = df[df['wave'] == 2025]
    df_24 = df[df['wave'] == 2024]

    # Tính toán điểm liên tưởng động
    def calculate_img_data(d, base_filter):
        res = {}
        for orig, short in attributes_viet.items():
            scores = {}
            for b in selected_brands:
                col = f'QI - {b}_{orig}'
                if col in d.columns:
                    if base_filter == "Người nhận biết thương hiệu":
                        aided_col = f'Q1Q2. Total aided awareness_{b}'
                        aware_resp = d[d[aided_col] == 1]
                    else:
                        aware_resp = d
                        
                    # Lọc show_as
                    if show_as == "Điểm trung bình (1-5)":
                        # Chuyển đổi sang thang điểm 5 nếu là mean
                        scores[b] = aware_resp[col].mean() * 4 + 1 if len(aware_resp) > 0 else 1.0
                    else:
                        scores[b] = aware_resp[col].mean() * 100 if len(aware_resp) > 0 else 0.0
                else:
                    scores[b] = 0.0
            res[short] = scores
        return pd.DataFrame(res).T

    df_img_25 = calculate_img_data(df_25, imagery_base)
    df_img_24 = calculate_img_data(df_24, imagery_base)

    # Cozy KPI calculations
    cozy_name = 'Trà Cozy đóng chai'
    is_cozy_active = cozy_name in selected_brands

    cozy_trust_25 = df_img_25.loc['3. Nhãn hiệu đáng tin cậy', cozy_name] if is_cozy_active else 0.0
    cozy_natural_25 = df_img_25.loc['9. Nguyên liệu tự nhiên', cozy_name] if is_cozy_active else 0.0
    c2_natural_25 = df_img_25.loc['9. Nguyên liệu tự nhiên', 'C2'] if 'C2' in selected_brands else 0.0
    cozy_taste_25 = df_img_25.loc['7. Vị ngon yêu thích', cozy_name] if is_cozy_active else 0.0
    
    cozy_trust_24 = df_img_24.loc['3. Nhãn hiệu đáng tin cậy', cozy_name] if is_cozy_active else 0.0
    cozy_trust_delta = cozy_trust_25 - cozy_trust_24
    
    natural_gap = cozy_natural_25 - c2_natural_25
    cozy_base = (df_25[f'Q1Q2. Total aided awareness_{cozy_name}'] == 1).sum() if is_cozy_active else len(df_25)

    # Title & Subtitle
    show_suffix = "Điểm trung bình (1-5)" if show_as == "Điểm trung bình (1-5)" else "Tỷ lệ %"
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #156835; margin: 0; font-size: 1.6rem; font-weight: 800;">Định vị hình ảnh thương hiệu — So sánh thuộc tính trên {len(selected_brands)} nhãn hàng</h2>
            <p style="color: #4e6556; font-size: 0.9rem; margin-top: 4px; margin-bottom: 20px;">
                Định dạng hiển thị: {show_suffix} • Căn cứ tính toán (Base): {imagery_base} • Nhãn hiệu đáng tin cậy của Cozy đạt {cozy_trust_25:.1f}
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
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">ĐIỂM HÌNH ẢNH MẠNH NHẤT</div>
                <div style="font-size: 1.55rem; font-weight: 850; color: #156835; line-height: 1.2;">Đáng tin cậy</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{cozy_trust_25:.1f} <span style="font-size:0.75rem; color:#156835; font-weight:bold;">{" + " if cozy_trust_delta >=0 else ""}{cozy_trust_delta:.1f} {"pp" if show_as != "Điểm trung bình (1-5)" else ""} ▲</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">LỢI THẾ LỚN NHẤT VS C2</div>
                <div style="font-size: 1.55rem; font-weight: 850; color: #156835; line-height: 1.2;">Tự nhiên</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">+{natural_gap:.1f} lead <span style="font-size:0.75rem; color:#156835; font-weight:bold;">{cozy_natural_25:.1f}</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">ĐIỂM YẾU ĐANG GIẢM</div>
                <div style="font-size: 1.55rem; font-weight: 850; color: #b25e5e; line-height: 1.2;">Nhiều vị lựa chọn</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">Chỉ đạt {df_img_25.loc['17. Nhiều vị lựa chọn', cozy_name] if cozy_name in df_img_25.columns else 0.0:.1f} <span style="font-size:0.75rem; color:#b25e5e; font-weight:bold;">Bét bảng</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">CỠ MẪU NHẬN BIẾT (COZY)</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{cozy_base}</div>
                <div style="font-size: 0.75rem; color: #8fa98f; font-weight: 600; margin-top: 8px;">Đáp viên phân tích</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. KHUNG BIỂU ĐỒ SONG SONG 2 BÊN
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>So sánh thuộc tính định vị hình ảnh thương hiệu (%)</div>", unsafe_allow_html=True)
        
        target_attrs = [
            '3. Nhãn hiệu đáng tin cậy',
            '9. Nguyên liệu tự nhiên',
            '11. Có lợi cho sức khỏe',
            '7. Vị ngon yêu thích',
            '17. Nhiều vị lựa chọn'
        ]
        
        df_top_5 = df_img_25.loc[target_attrs]
        
        fig_attr = go.Figure()
        colors = {
            'Trà Cozy đóng chai': '#156835',
            'C2': '#7f7f7f',
            'OLong Tea Plus': '#aaaaaa',
            'Không Độ': '#d0d0d0'
        }
        
        for b in selected_brands:
            fig_attr.add_trace(go.Bar(
                y=[x.split('. ')[-1] for x in target_attrs],
                x=df_top_5[b],
                name=b.replace('Trà ', '').replace(' đóng chai', ''),
                orientation='h',
                marker_color=colors.get(b, '#cccccc'),
                text=[f"{v:.1f}" for v in df_top_5[b]],
                textposition='inside'
            ))
            
        fig_attr.update_layout(
            barmode='group',
            height=320,
            xaxis_title=show_suffix,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(_apply_cozy_theme(fig_attr), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Cozy tiếp tục dẫn đầu ở hai thuộc tính 'Đáng tin cậy' và 'Nguyên liệu tự nhiên' nhưng ghi nhận điểm yếu về 'Nhiều vị lựa chọn'; nhãn hàng cần đa dạng danh mục SKU để củng cố vị trí số 1 này ở Wave 2026.</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Biến động thuộc tính Đáng tin cậy qua 2 Wave (%)</div>", unsafe_allow_html=True)
        
        fig_trend = go.Figure()
        
        for b in selected_brands:
            is_focal = b == 'Trà Cozy đóng chai'
            linewidth = 4 if is_focal else 2
            dashstyle = 'solid' if is_focal else ('dash' if b == 'C2' else 'dot')
            
            b_trend = [df_img_24.loc['3. Nhãn hiệu đáng tin cậy', b], df_img_25.loc['3. Nhãn hiệu đáng tin cậy', b]]
            fig_trend.add_trace(go.Scatter(
                x=['Wave 2024', 'Wave 2025'],
                y=b_trend,
                mode='lines+markers+text',
                name=b.replace('Trà ', '').replace(' đóng chai', ''),
                line=dict(color=colors.get(b, '#cccccc'), width=linewidth, dash=dashstyle),
                marker=dict(size=8 if is_focal else 6),
                text=[f"{v:.1f}" for v in b_trend],
                textposition="top center" if is_focal else "bottom center"
            ))
            
        fig_trend.update_layout(
            height=320,
            yaxis_title=show_suffix,
            yaxis=dict(range=[1, 5] if show_as == "Điểm trung bình (1-5)" else [0, 100])
        )
        st.plotly_chart(_apply_cozy_theme(fig_trend), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Liên tưởng hình ảnh 'Đáng tin cậy' của Cozy tăng trưởng {'+' if cozy_trust_delta>=0 else ''}{cozy_trust_delta:.1f}pp vs Wave 2024 dẫn đầu thị trường; nhãn hàng cần duy trì thông điệp tin cậy và tích hợp wellness để nâng chỉ số thêm 5pp vào Wave 2026.</div>", unsafe_allow_html=True)

    st.divider()

    # 3. BẢNG ĐỐI SÁNH CHI TIẾT CHÂN TRANG
    st.markdown("<div style='font-weight: 800; font-size: 1.1rem; color: #156835; margin-bottom: 10px;'>Bảng đối sánh chi tiết 18 thuộc tính định vị thương hiệu</div>", unsafe_allow_html=True)
    
    rows_html = ""
    for idx, short_name in enumerate(df_img_25.index):
        row_cells = f"<td style='text-align: left; padding-left: 20px;'>{short_name}</td>"
        cozy_v = 0.0
        c2_v = 0.0
        
        for b in selected_brands:
            val = df_img_25.loc[short_name, b]
            if b == 'Trà Cozy đóng chai':
                cozy_v = val
            elif b == 'C2':
                c2_v = val
            row_cells += f"<td>{val:.1f}</td>"
            
        # Tính khoảng cách lead vs C2 hoặc hãng đầu tiên
        lead_v = cozy_v - c2_v
        lead_class = "delta-green-txt" if lead_v >= 0 else "delta-red-txt"
        lead_str = f"{'+' if lead_v >= 0 else ''}{lead_v:.1f}{'pp' if show_as != 'Điểm trung bình (1-5)' else ''}"
        
        row_cells += f"<td class='{lead_class}'>{lead_str}</td>"
        rows_html += f"<tr>{row_cells}</tr>"

    headers_html = "".join([f"<th>{b.replace('Trà ', '').replace(' đóng chai', '').upper()}</th>" for b in selected_brands])

    table_html = f"""
    <style>
        .img-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(21, 104, 53, 0.15);
            box-shadow: 0 4px 15px rgba(21, 104, 53, 0.02);
        }}
        .img-table th {{
            background: linear-gradient(135deg, #156835 0%, #0d4622 100%);
            color: white;
            text-align: center;
            padding: 14px 16px;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.02em;
        }}
        .img-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid rgba(21, 104, 53, 0.08);
            color: #1b2e22;
            font-size: 0.88rem;
            text-align: center;
            font-weight: 500;
        }}
        .img-table tr:last-child td {{
            border-bottom: none;
        }}
        .img-table tr:nth-child(even) {{
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
    <table class="img-table">
        <thead>
            <tr>
                <th style="text-align: left; padding-left: 20px;">18 THUỘC TÍNH HÌNH ẢNH</th>
                {headers_html}
                <th>COZY LEAD (VS C2)</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    import textwrap
    st.markdown(textwrap.dedent(table_html), unsafe_allow_html=True)
