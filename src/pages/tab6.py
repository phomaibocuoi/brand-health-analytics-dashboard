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

def render_tab6(df: pd.DataFrame) -> None:
    # 1. RENDER BỘ LỌC ĐỘNG TRÊN SIDEBAR
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #ffffff; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</h3>", unsafe_allow_html=True)
    
    selected_wave = st.sidebar.selectbox("Wave khảo sát (Năm)", options=[2025, 2024], index=0)
    
    st.sidebar.markdown("<p style='color: #ffffff; font-weight: bold; margin: 12px 0 4px 0; font-size: 0.88rem; opacity: 0.95;'>THƯƠNG HIỆU SO SÁNH</p>", unsafe_allow_html=True)
    cozy_sel = st.sidebar.checkbox("Cozy", value=True, key="tp_cozy")
    c2_sel = st.sidebar.checkbox("C2", value=True, key="tp_c2")
    tp_sel = st.sidebar.checkbox("Tea Plus", value=True, key="tp_tp")
    kd_sel = st.sidebar.checkbox("Không Độ", value=True, key="tp_kd")
    
    region_map = {
        "Tất cả": "All",
        "Miền Bắc": "North",
        "Miền Trung": "Central",
        "Miền Nam": "South",
        "ĐBSCL (Mekong)": "Mekong"
    }
    region_sel_vn = st.sidebar.selectbox("Khu vực", options=list(region_map.keys()), index=0)
    region_sel = region_map[region_sel_vn]

    # Danh sách thương hiệu so sánh
    selected_brands = []
    if cozy_sel: selected_brands.append('Trà Cozy đóng chai')
    if c2_sel: selected_brands.append('C2')
    if tp_sel: selected_brands.append('OLong Tea Plus')
    if kd_sel: selected_brands.append('Không Độ')

    if not selected_brands:
        st.warning("Vui lòng chọn ít nhất một Thương hiệu ở Sidebar!")
        return

    # Lọc theo vùng miền
    if region_sel != "All":
        df_filtered = df[df['region'] == region_sel]
    else:
        df_filtered = df

    # Lọc theo Wave
    df_active = df_filtered[df_filtered['wave'] == selected_wave]

    if len(df_active) == 0:
        st.warning("Không có dữ liệu thỏa mãn bộ lọc hiện tại!")
        return

    # Tiêu đề chuyên đề
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #156835; margin: 0; font-size: 1.6rem; font-weight: 800;">Dịp tiêu dùng & Điểm chạm thương hiệu — Cozy vs C2 + Đối thủ</h2>
            <p style="color: #4e6556; font-size: 0.9rem; margin-top: 4px; margin-bottom: 20px;">
                Cơ cấu dịp sử dụng và các kênh truyền thông tiếp cận thương hiệu chính
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bảng dịch tên các nhãn hiệu hiển thị trên biểu đồ
    brand_short_map = {
        'Trà Cozy đóng chai': 'Cozy',
        'C2': 'C2',
        'OLong Tea Plus': 'Tea Plus',
        'Không Độ': 'Không Độ'
    }

    # Bảng R-code mapping cho TP1 columns (format: Q_TP1_C1_R15- Trà Cozy đóng chai_...)
    brand_rcode_map = {
        'Trà Cozy đóng chai': 'R15- Trà Cozy đóng chai',
        'C2': 'R1- C2',
        'OLong Tea Plus': 'R7- OLong Tea Plus',
        'Không Độ': 'R11- Không Độ'
    }

    # Bảng dịch dịp uống (Occasions) sang tiếng Việt
    occ_viet_map = {
        'When taking a break after school/work': 'Nghỉ giải lao sau giờ học/làm',
        'When outside': 'Khi đi ngoài trời nắng',
        'When entertaining at home (Listen to music, watch movie, watch TV,…)': 'Thư giãn/giải trí tại nhà',
        'When having meals/party with friends/family': 'Ăn tiệc cùng bạn bè/gia đình',
        'When hanging out with friends/family': 'Đi chơi/dã ngoại cùng bạn bè/gia đình',
        'When having meals': 'Khi đang ăn cơm',
        'After consuming beer/ alcohol': 'Giải rượu bia/sau uống cồn',
        'After doing sport': 'Sau khi tập thể thao',
        'When watch movie/ attend music concert': 'Đi xem phim/nhạc kịch',
        'Other (specify): …………….': 'Dịp khác'
    }

    # Bảng dịch kênh mua (Purchase Channels) sang tiếng Việt
    chan_viet_map = {
        'Grocery Shop': 'Tiệm tạp hóa truyền thống',
        'Coffee shop/ Beverage street vendor': 'Quán cà phê/nước vỉa hè',
        'Supermarket': 'Siêu thị đại siêu thị',
        'Convenient store': 'Cửa hàng tiện lợi',
        'Eatery place/restaurant': 'Quán ăn/nhà hàng',
        'Vending machine': 'Máy bán hàng tự động',
        'E-commerce website': 'Trang online/Thương mại điện tử',
        'Carteen': 'Căng-tin trường học/công sở',
        'Wet Markets': 'Chợ truyền thống',
        'Other (specify): …………….': 'Kênh khác'
    }

    # 1. HÀNG KPI CARDS TỔNG QUAN HÀNH VI COZY
    cozy_name = 'Trà Cozy đóng chai'
    is_cozy_selected = cozy_name in selected_brands

    # Tính toán các chỉ số cho Cozy nếu được chọn
    if is_cozy_selected:
        cozy_occ_col = f'Q_TP3_R15- {cozy_name}'
        cozy_chan_col = f'Q_TP2_R15- {cozy_name}'
        
        # Dịp phổ biến nhất
        cozy_occ_data = df_active[cozy_occ_col].dropna().value_counts(normalize=True) * 100
        top_occ_name = occ_viet_map.get(cozy_occ_data.index[0], cozy_occ_data.index[0]) if not cozy_occ_data.empty else "Nghỉ giải lao"
        top_occ_val = cozy_occ_data.values[0] if not cozy_occ_data.empty else 0.0

        # Kênh mua phổ biến nhất
        cozy_chan_data = df_active[cozy_chan_col].dropna().value_counts(normalize=True) * 100
        top_chan_name = chan_viet_map.get(cozy_chan_data.index[0], cozy_chan_data.index[0]) if not cozy_chan_data.empty else "Tạp hóa"
        top_chan_val = cozy_chan_data.values[0] if not cozy_chan_data.empty else 0.0
        
        # Tỷ lệ chạm kênh Online quảng cáo của Cozy
        online_ad_col = f'Q_TP1_C2_R15- {cozy_name}_Advertising on Internet (website, Facebook, YouTube, etc)'
        aided_col = f'Q1Q2. Total aided awareness_{cozy_name}'
        cozy_aware = df_active[df_active[aided_col] == 1]
        cozy_online_ad = cozy_aware[online_ad_col].mean() * 100 if len(cozy_aware) > 0 and online_ad_col in df_active.columns else 0.0
    else:
        top_occ_name, top_occ_val = "N/A", 0.0
        top_chan_name, top_chan_val = "N/A", 0.0
        cozy_online_ad = 0.0

    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">DỊP TIÊU DÙNG SỐ 1 COZY</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #156835; line-height: 1.2;">{top_occ_name}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{top_occ_val:.1f}% <span style="font-size:0.75rem; color:#156835; font-weight:bold;">đáp viên uống</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">KÊNH MUA PHỔ BIẾN NHẤT</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #156835; line-height: 1.2;">{top_chan_name}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{top_chan_val:.1f}% <span style="font-size:0.75rem; color:#156835; font-weight:bold;">thị phần kênh</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">ĐIỂM CHẠM QUẢNG CÁO TRỰC TUYẾN</div>
                <div style="font-size: 1.45rem; font-weight: 850; color: #156835; line-height: 1.2;">Quảng cáo Internet</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #4e6556; margin-top: 4px;">{cozy_online_ad:.1f}% <span style="font-size:0.75rem; color:#156835; font-weight:bold;">độ phủ quảng cáo</span></div>
            </div>
            <div style="background: white; border: 1px solid rgba(21, 104, 53, 0.15); border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(21, 104, 53, 0.03);">
                <div style="color: #4e6556; size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">NĂM ĐANG PHÂN TÍCH</div>
                <div style="font-size: 2.1rem; font-weight: 850; color: #156835; line-height: 1.1;">{selected_wave}</div>
                <div style="font-size: 0.75rem; color: #8fa98f; font-weight: 600; margin-top: 8px;">Wave dữ liệu của báo cáo</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. KHUNG BIỂU ĐỒ 2 BÊN: OCCASIONS VS PURCHASE CHANNELS
    col_left, col_right = st.columns(2)

    colors = {
        'Trà Cozy đóng chai': '#156835',
        'C2': '#7f7f7f',
        'OLong Tea Plus': '#aaaaaa',
        'Không Độ': '#d0d0d0'
    }

    with col_left:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Cơ cấu các dịp uống trà RTD của các hãng (%)</div>", unsafe_allow_html=True)
        
        # Tính toán Occasions cho các hãng được chọn
        df_occ_list = []
        for b in selected_brands:
            b_mapper_names = {
                'Trà Cozy đóng chai': 'R15- Trà Cozy đóng chai',
                'C2': 'R1- C2',
                'OLong Tea Plus': 'R7- OLong Tea Plus',
                'Không Độ': 'R11- Không Độ'
            }
            col = f'Q_TP3_{b_mapper_names.get(b, b)}'
            if col in df_active.columns:
                occ_counts = df_active[col].dropna().value_counts(normalize=True) * 100
                df_b = pd.DataFrame(occ_counts).reset_index()
                df_b.columns = ['Occasion', 'Percentage']
                df_b['Brand'] = brand_short_map.get(b, b)
                df_occ_list.append(df_b)
        
        if df_occ_list:
            df_occ_all = pd.concat(df_occ_list)
            # Reindex and translate Occasion
            df_occ_all['Occasion_VN'] = df_occ_all['Occasion'].map(occ_viet_map)
            df_occ_pivot = df_occ_all.pivot(index='Occasion_VN', columns='Brand', values='Percentage').fillna(0.0)
            # Sắp xếp theo Cozy giảm dần
            focal_short = brand_short_map.get(cozy_name)
            if focal_short in df_occ_pivot.columns:
                df_occ_pivot = df_occ_pivot.sort_values(by=focal_short, ascending=True)
            
            fig_occ = go.Figure()
            for b in selected_brands:
                b_short = brand_short_map.get(b, b)
                if b_short in df_occ_pivot.columns:
                    fig_occ.add_trace(go.Bar(
                        y=df_occ_pivot.index,
                        x=df_occ_pivot[b_short],
                        name=b_short,
                        orientation='h',
                        marker_color=colors.get(b, '#cccccc'),
                        text=[f"{v:.1f}%" for v in df_occ_pivot[b_short]],
                        textposition='inside' if len(selected_brands) <= 2 else 'outside'
                    ))
            
            fig_occ.update_layout(
                barmode='group',
                height=350,
                xaxis_title="Tỷ lệ % dịp uống của hãng"
            )
            st.plotly_chart(_apply_cozy_theme(fig_occ), use_container_width=True, config={"displayModeBar": False})
            st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Dịp '{top_occ_name}' ({top_occ_val:.1f}%) chiếm ưu thế lớn nhất trong tiêu dùng Cozy RTD; nhãn hàng cần lồng ghép sản phẩm vào ngữ cảnh giải trí nhóm và ăn uống gia đình để tăng thị phần thêm 5pp trước Wave 2026.</div>", unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu Dịp uống của các thương hiệu đã chọn.")

    with col_right:
        st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Cơ cấu các kênh mua sắm trà RTD của các hãng (%)</div>", unsafe_allow_html=True)
        
        # Tính toán Channels cho các hãng được chọn
        df_chan_list = []
        for b in selected_brands:
            b_mapper_names = {
                'Trà Cozy đóng chai': 'R15- Trà Cozy đóng chai',
                'C2': 'R1- C2',
                'OLong Tea Plus': 'R7- OLong Tea Plus',
                'Không Độ': 'R11- Không Độ'
            }
            col = f'Q_TP2_{b_mapper_names.get(b, b)}'
            if col in df_active.columns:
                chan_counts = df_active[col].dropna().value_counts(normalize=True) * 100
                df_b = pd.DataFrame(chan_counts).reset_index()
                df_b.columns = ['Channel', 'Percentage']
                df_b['Brand'] = brand_short_map.get(b, b)
                df_chan_list.append(df_b)
        
        if df_chan_list:
            df_chan_all = pd.concat(df_chan_list)
            df_chan_all['Channel_VN'] = df_chan_all['Channel'].map(chan_viet_map)
            df_chan_pivot = df_chan_all.pivot(index='Channel_VN', columns='Brand', values='Percentage').fillna(0.0)
            if focal_short in df_chan_pivot.columns:
                df_chan_pivot = df_chan_pivot.sort_values(by=focal_short, ascending=True)
                
            fig_chan = go.Figure()
            for b in selected_brands:
                b_short = brand_short_map.get(b, b)
                if b_short in df_chan_pivot.columns:
                    fig_chan.add_trace(go.Bar(
                        y=df_chan_pivot.index,
                        x=df_chan_pivot[b_short],
                        name=b_short,
                        orientation='h',
                        marker_color=colors.get(b, '#cccccc'),
                        text=[f"{v:.1f}%" for v in df_chan_pivot[b_short]],
                        textposition='inside' if len(selected_brands) <= 2 else 'outside'
                    ))
            
            fig_chan.update_layout(
                barmode='group',
                height=350,
                xaxis_title="Tỷ lệ % địa điểm mua của hãng"
            )
            st.plotly_chart(_apply_cozy_theme(fig_chan), use_container_width=True, config={"displayModeBar": False})
            st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px;'><b>Nhận định:</b> Kênh '{top_chan_name}' ({top_chan_val:.1f}%) chiếm ưu thế tuyệt đối trong phân phối của Cozy; nhãn hàng cần tăng cường hiện diện tại quầy kệ tạp hóa truyền thống và tài trợ tủ mát để bứt phá thị phần lên 40% ở Wave 2026.</div>", unsafe_allow_html=True)
        else:
            st.warning("Không có dữ liệu Kênh mua sắm của các thương hiệu đã chọn.")

    st.divider()

    # 3. KÊNH TIẾP CẬN TRUYỀN THÔNG (Q_TP1)
    st.markdown(f"<div style='font-weight: 700; font-size: 1rem; color: #156835; margin-bottom: 8px;'>Top 8 điểm chạm truyền thông quảng cáo phổ biến nhất (%)</div>", unsafe_allow_html=True)
    
    # Định nghĩa danh sách điểm chạm quảng cáo
    tp1_viet_map = {
        'TV': 'Quảng cáo Tivi (TVC/Gameshow)',
        'Internet': 'Quảng cáo Internet (Mạng xã hội/TikTok/YouTube)',
        'Outdoor': 'Bảng quảng cáo ngoài trời (Billboard)',
        'Transportation': 'Quảng cáo dán trên Xe buýt/Grab',
        'LCD': 'Màn hình LCD tòa nhà/văn phòng',
        'Events': 'Sự kiện tài trợ ngoài trời',
        'Product display': 'Trưng bày sản phẩm tại kệ siêu thị/tạp hóa',
        'Poster': 'Áp phích/Poster dán tại cửa hàng',
        'store sign': 'Hộp đèn/bảng hiệu tại quán ăn/cửa hàng',
        'Promotion': 'Khuyến mại giảm giá tại siêu thị/tạp hóa',
        'Marketing staff': 'Nhân viên PG tiếp thị giới thiệu',
        'Recommended by seller': 'Được chủ tiệm/người bán khuyên dùng',
        'Recommended by friends/relatives': 'Bạn bè/người thân giới thiệu',
        'Seeing others use': 'Nhìn thấy người xung quanh uống',
        'Sampling': 'Phát hàng mẫu dùng thử miễn phí (Sampling)',
        'newspaper': 'Quảng cáo trên Báo/Tạp chí',
        'radio': 'Quảng cáo trên Radio/Loa phát thanh',
        'None of these': 'Không tiếp cận kênh nào'
    }

    # Tổng hợp dữ liệu TP1 cho các hãng
    # Format cột thực tế: Q_TP1_C1_R15- Trà Cozy đóng chai_Advertising on TV
    tp1_scores = {}
    
    for b in selected_brands:
        aided_col = f'Q1Q2. Total aided awareness_{b}'
        aware_resp = df_active[df_active[aided_col] == 1]
        r_code = brand_rcode_map.get(b, b)
        
        b_scores = {}
        for short_k, vn_name in tp1_viet_map.items():
            # Tìm cột theo R-code của thương hiệu (tránh khớp nhầm channel codes C1/C2...)
            matching_cols = [
                c for c in df_active.columns
                if 'Q_TP1_' in c and r_code in c and short_k.lower() in c.lower()
            ]
            if matching_cols:
                col = matching_cols[0]
                b_scores[vn_name] = aware_resp[col].mean() * 100 if len(aware_resp) > 0 else 0.0
            else:
                b_scores[vn_name] = 0.0
        tp1_scores[brand_short_map.get(b, b)] = b_scores

    if tp1_scores:
        df_tp1 = pd.DataFrame(tp1_scores)
        # Lọc bỏ dòng 'Không tiếp cận kênh nào' hoặc sắp xếp top 8
        if focal_short in df_tp1.columns:
            df_tp1 = df_tp1.sort_values(by=focal_short, ascending=False).head(8)
        else:
            df_tp1 = df_tp1.head(8)
            
        fig_tp1 = go.Figure()
        for b in selected_brands:
            b_short = brand_short_map.get(b, b)
            if b_short in df_tp1.columns:
                fig_tp1.add_trace(go.Bar(
                    x=df_tp1.index,
                    y=df_tp1[b_short],
                    name=b_short,
                    marker_color=colors.get(b, '#cccccc'),
                    text=[f"{v:.0f}%" for v in df_tp1[b_short]],
                    textposition='outside'
                ))
        
        fig_tp1.update_layout(
            barmode='group',
            height=340,
            yaxis_title="Tỷ lệ % tiếp cận của người biết thương hiệu"
        )
        st.plotly_chart(_apply_cozy_theme(fig_tp1), use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"<div style='font-size: 0.82rem; color: #4e6556; line-height: 1.4; font-style: italic; margin-top: 5px; margin-bottom: 15px;'><b>Nhận định:</b> Kênh quảng cáo trực tuyến ({cozy_online_ad:.1f}%) và trưng bày tại điểm bán là hai điểm chạm truyền thông lớn nhất của Cozy; nhãn hàng cần tăng cường ngân sách tiếp thị số (TikTok/YouTube) để nâng tỷ lệ tiếp cận lên trên 60% ở Wave 2026.</div>", unsafe_allow_html=True)
    else:
        st.warning("Không có dữ liệu Điểm chạm truyền thông.")

    st.divider()

    # 4. BẢNG THỐNG KÊ CHI TIẾT
    st.markdown("<div style='font-weight: 800; font-size: 1.1rem; color: #156835; margin-bottom: 10px;'>Bảng đối sánh chi tiết Kênh tiếp cận truyền thông (Media Touchpoints) (%)</div>", unsafe_allow_html=True)
    
    df_tp1_all = pd.DataFrame(tp1_scores)
    if focal_short in df_tp1_all.columns:
        df_tp1_all = df_tp1_all.sort_values(by=focal_short, ascending=False)
        
    rows_html = ""
    for vn_name in df_tp1_all.index:
        row_cells = f"<td style='text-align: left; padding-left: 20px;'>{vn_name}</td>"
        cozy_val = df_tp1_all.loc[vn_name, focal_short] if focal_short in df_tp1_all.columns else 0.0
        c2_val = df_tp1_all.loc[vn_name, 'C2'] if 'C2' in df_tp1_all.columns else 0.0
        
        for b in selected_brands:
            b_short = brand_short_map.get(b, b)
            val = df_tp1_all.loc[vn_name, b_short]
            row_cells += f"<td>{val:.1f}%</td>"
            
        lead_v = cozy_val - c2_val
        lead_class = "delta-green-txt" if lead_v >= 0 else "delta-red-txt"
        lead_str = f"{'+' if lead_v >= 0 else ''}{lead_v:.1f}pp"
        
        row_cells += f"<td class='{lead_class}'>{lead_str}</td>"
        rows_html += f"<tr>{row_cells}</tr>"

    headers_html = "".join([f"<th>{b.replace('Trà ', '').replace(' đóng chai', '').upper()}</th>" for b in selected_brands])

    table_html = f"""<style>
.touch-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(21, 104, 53, 0.15);
    box-shadow: 0 4px 15px rgba(21, 104, 53, 0.02);
}}
.touch-table th {{
    background: linear-gradient(135deg, #156835 0%, #0d4622 100%);
    color: white;
    text-align: center;
    padding: 14px 16px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}}
.touch-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(21, 104, 53, 0.08);
    color: #1b2e22;
    font-size: 0.88rem;
    text-align: center;
    font-weight: 500;
}}
.touch-table tr:last-child td {{
    border-bottom: none;
}}
.touch-table tr:nth-child(even) {{
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
<table class="touch-table">
<thead>
<tr>
<th style="text-align: left; padding-left: 20px;">DANH SÁCH 18 ĐIỂM CHẠM TRUYỀN THÔNG TỔNG HỢP</th>
{headers_html}
<th>COZY DẪN ĐẦU (VS C2)</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>"""
    st.markdown(table_html, unsafe_allow_html=True)
