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

def render_tab3(df: pd.DataFrame) -> None:
    """Render full brand imagery and attribute association analysis (Phần 3)."""
    # ===== 1. ĐỊNH NGHĨA 18 THUỘC TÍNH VÀ MAP SANG TIẾNG VIỆT =====
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

    # Lọc Wave 2025 mới nhất để phản ánh đúng hiện trạng định vị thương hiệu
    df_25 = df[df['wave'] == 2025]
    funnel_brands = ['Trà Cozy đóng chai', 'C2', 'OLong Tea Plus', 'Không Độ']

    # ===== 2. TÍNH TOÁN CÁC KPI CHỦ CHỐT CHO COZY =====
    # Tính điểm Cozy cho một số thuộc tính cốt lõi
    def get_cozy_score(orig_attr: str) -> float:
        col = f'QI - Trà Cozy đóng chai_{orig_attr}'
        if col in df_25.columns:
            aware_resp = df_25[df_25['Q1Q2. Total aided awareness_Trà Cozy đóng chai'] == 1]
            return float(aware_resp[col].mean() * 100) if len(aware_resp) > 0 else 0.0
        return 0.0

    cozy_trust = get_cozy_score('Nhãn hiệu đáng tin cậy')
    cozy_natural = get_cozy_score('Sản xuất từ nguyên liệu tự nhiên')
    cozy_health = get_cozy_score('Giải nhiệt cuộc sống')
    cozy_flavor_bottleneck = get_cozy_score('Có nhiều vị để lựa chọn')

    # ===== 3. VẼ CÁC KPI CARDS =====
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Thuộc tính cao nhất (Đáng tin cậy)</div>
                <div class="kpi-value">{cozy_trust:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Nguyên liệu tự nhiên (Natural)</div>
                <div class="kpi-value">{cozy_natural:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Định vị Giải nhiệt (Refreshment)</div>
                <div class="kpi-value">{cozy_health:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Điểm rào cản Đa dạng hương vị</div>
                <div class="kpi-value">{cozy_flavor_bottleneck:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # ===== 4. TÍNH TOÁN BẢNG DỮ LIỆU ĐỊNH VỊ CHO CẢ 4 THƯƠNG HIỆU =====
    results_img = []
    for orig_attr, eng_attr in attributes_viet.items():
        row = {'Thuộc tính': eng_attr}
        for b in funnel_brands:
            col = f'QI - {b}_{orig_attr}'
            if col in df_25.columns:
                aided_col = f'Q1Q2. Total aided awareness_{b}'
                aware_respondents = df_25[df_25[aided_col] == 1]
                row[b] = aware_respondents[col].mean() * 100 if len(aware_respondents) > 0 else 0.0
            else:
                row[b] = 0.0
        results_img.append(row)

    df_img = pd.DataFrame(results_img).set_index('Thuộc tính')

    st.subheader("🗺️ 1. Bản đồ nhiệt liên tưởng hình ảnh thương hiệu (Brand Attribute Heatmap)")
    st.caption("Khảo sát mối liên tưởng giữa tệp đáp viên nhận biết thương hiệu đối với 18 thuộc tính hình ảnh (Wave 2025)")

    # Biểu đồ Heatmap Plotly
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=df_img.values,
        x=df_img.columns,
        y=df_img.index,
        colorscale='YlGn',
        colorbar=dict(title="Tỷ lệ liên tưởng (%)"),
        hovertemplate="<b>Thuộc tính:</b> %{y}<br><b>Thương hiệu:</b> %{x}<br><b>Tỷ lệ liên tưởng:</b> %{z:.1f}%<extra></extra>"
    ))

    # Thêm giá trị số trực tiếp lên bản đồ nhiệt (Annotations)
    annotations = []
    for y_idx, y_val in enumerate(df_img.index):
        for x_idx, x_val in enumerate(df_img.columns):
            val = df_img.values[y_idx, x_idx]
            annotations.append(
                dict(
                    x=x_val,
                    y=y_val,
                    text=f"{val:.1f}%",
                    showarrow=False,
                    font=dict(color="black" if val < 45 else "white", size=9, weight="bold")
                )
            )
    fig_heatmap.update_layout(
        annotations=annotations,
        height=620,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(_apply_cozy_theme(fig_heatmap), use_container_width=True, config={"displayModeBar": False})

    # ===== 5. TƯƠNG TÁC SO SÁNH ĐƠN THUỘC TÍNH (Single Attribute Comparison) =====
    st.subheader("📊 2. So sánh chi tiết theo từng thuộc tính đơn lẻ")
    
    col_sel, _ = st.columns([2, 2])
    with col_sel:
        selected_attr_vn = st.selectbox(
            "Chọn thuộc tính hình ảnh để so sánh giữa các hãng:",
            options=list(attributes_viet.values())
        )
    
    # Lấy dữ liệu của thuộc tính được chọn
    if selected_attr_vn in df_img.index:
        attr_data = df_img.loc[selected_attr_vn]
        
        # Sắp xếp để vẽ biểu đồ
        attr_data_sorted = attr_data.sort_values(ascending=False)
        colors_bar = ['#156835' if b == 'Trà Cozy đóng chai' else '#8FA98F' for b in attr_data_sorted.index]
        
        fig_attr = go.Figure(go.Bar(
            x=attr_data_sorted.index,
            y=attr_data_sorted.values,
            marker_color=colors_bar,
            text=[f"{v:.1f}%" for v in attr_data_sorted.values],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Tỷ lệ liên tưởng: %{y:.1f}%<extra></extra>"
        ))
        
        fig_attr.update_layout(
            title=f"Tỷ lệ liên tưởng của thuộc tính: '{selected_attr_vn}' (%)",
            xaxis_title="Thương hiệu",
            yaxis_title="Tỷ lệ (%)",
            height=300,
            margin=dict(l=10, r=10, t=55, b=10),
        )
        st.plotly_chart(_apply_cozy_theme(fig_attr), use_container_width=True, config={"displayModeBar": False})

    # ===== 6. TẤM THẺ ĐÚC KẾT CHIẾN LƯỢC (Insight Card) =====
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🧠 ĐỊNH VỊ HÌNH ẢNH COZY — ĐÚC KẾT CỦA SENIOR ANALYST:</div>
            <div class="insight-main">
                <ul>
                    <li><strong>Thế mạnh độc quyền về uy tín lý tính:</strong> Người tiêu dùng liên tưởng mạnh mẽ nhất Cozy với 3 thuộc tính: <strong>Nhãn hiệu đáng tin cậy (60.3%)</strong>, <strong>Nguyên liệu tự nhiên (60.2%)</strong> và <strong>Có lợi cho sức khỏe (55.3%)</strong>. Đây là tài sản thương hiệu khổng lồ thừa hưởng từ di sản trà sạch truyền thống của Cozy, giúp Cozy xây dựng lòng tin vững chắc hơn các thương hiệu công nghiệp.</li>
                    <li><strong>Vết nứt nghiêm trọng về xúc cảm vị giác (Sensory Bottleneck):</strong> Cozy chịu điểm số cực thấp ở thuộc tính <strong>Vị ngon tôi yêu thích (36.6%)</strong> so với C2 (68.8%) và OLong Tea Plus (68.3%). Rất đáng báo động khi thuộc tính cốt lõi của ngành hàng giải khát là "Vị ngon sảng khoái tức thì" lại là điểm yếu của Cozy.</li>
                    <li><strong>Điểm mù về sự phong phú sản phẩm (Wide Flavor Variety):</strong> Điểm liên tưởng cho <strong>Nhiều vị để lựa chọn</strong> chỉ đạt mức không tưởng <strong>13.8%</strong> (trong khi C2 đạt 42.3%). Thực tế, Cozy có trà đào sả, vải, olong xoài cực trend, nhưng do phủ kênh yếu và truyền thông mỏng khiến người dùng bị "mù thông tin" về các SKU này.</li>
                    <li><strong>Cơ hội định vị (Opportunity):</strong> Cozy cần dịch chuyển trục truyền thông từ "Trà lý tính tốt cho sức khỏe" sang "Trà trái cây thơm ngon cực đỉnh", kết hợp chạy các chương trình phát mẫu dùng thử (sampling) quy mô lớn để thay đổi nhận thức vị giác thực tế của tệp đáp viên trẻ tuổi.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
