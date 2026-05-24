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

def render_tab5(df: pd.DataFrame) -> None:
    """Render Cozy product switching and barriers analysis (Phần 4)."""
    # Lọc dữ liệu Wave 2025 mới nhất
    df_25 = df[df['wave'] == 2025]

    # ===== 1. TÍNH TOÁN CÁC KPI CHỦ CHỐT =====
    # 1.1 Switching Source
    df_cozy_bumo = df_25[df_25['bumo_master'] == 'Trà Cozy đóng chai']
    if len(df_cozy_bumo) > 0:
        switching_source = df_cozy_bumo['Q7. Previous BUMO'].value_counts(normalize=True) * 100
        top_switch_brand = switching_source.index[0]
        top_switch_pct = switching_source.values[0]
    else:
        top_switch_brand = "Không Độ"
        top_switch_pct = 0.0

    # 1.2 Barriers (Q.ME2)
    cozy_barrier_cols = [c for c in df_25.columns if 'QME2 - Trà Cozy đóng chai' in c]
    barriers_pct = {}
    target_resp = df_25[
        (df_25['Q1Q2. Total aided awareness_Trà Cozy đóng chai'] == 1) &
        (df_25['Q4Q8.BRAND CONSIDERATION SET_Trà Cozy đóng chai'] == 0)
    ]
    
    for col in cozy_barrier_cols:
        barrier_name = col.split('_')[-1]
        barriers_pct[barrier_name] = target_resp[col].mean() * 100 if len(target_resp) > 0 else 0.0

    df_barriers = pd.Series(barriers_pct).sort_values(ascending=False).head(10)
    
    # Map sang tiếng Việt cho trực quan
    barrier_mapper = {
        'Do not like the flavor / The flavor do not taste good': 'Không thích vị / Vị không ngon',
        'Does not have enough flavour that I want to choose': 'Nghèo nàn sự lựa chọn hương vị',
        'Asked but the store does not sell it': 'Hỏi mua nhưng cửa hàng không bán',
        'Not preserved in cool place': 'Không được ướp lạnh sẵn trong tủ',
        'The design of packaging is not attractive': 'Thiết kế bao bì không thu hút',
        'Does not have enough flavor choice': 'Nghèo nàn danh mục vị',
        'Bad quality': 'Chất lượng không tốt',
        'Price is too expensive/not suitable': 'Giá đắt / không phù hợp',
        'Do not trust the brand': 'Không tin tưởng thương hiệu',
        'Too sweet': 'Vị trà quá ngọt'
    }
    
    df_barriers.index = [barrier_mapper.get(x, x) for x in df_barriers.index]
    
    top_flavor_barrier = df_barriers.values[0]
    top_flavor_label = df_barriers.index[0]
    
    top_dist_barrier = df_barriers.get('Hỏi mua nhưng cửa hàng không bán', 0.0)

    # ===== 2. VẼ KPI CARDS =====
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Nguồn chuyển đổi chính</div>
                <div class="kpi-value">{top_switch_brand} ({top_switch_pct:.1f}%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Rào cản Cảm quan lớn nhất</div>
                <div class="kpi-value">{top_flavor_label} ({top_flavor_barrier:.1f}%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Rào cản Nghèo nàn danh mục vị</div>
                <div class="kpi-value">{df_barriers.get('Nghèo nàn danh mục vị', 0.0):.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Rào cản phân phối (Hỏi mua không có)</div>
                <div class="kpi-value">{top_dist_barrier:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # ===== 3. BIỂU ĐỒ HAI CỘT SONG SONG =====
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("🔄 1. Nguồn chuyển đổi thương hiệu (Switching Source)")
        st.caption("Người dùng uống Cozy thường xuyên nhất trước đây dùng nhãn hiệu nào? (%)")
        
        if len(df_cozy_bumo) > 0:
            # Map tên các nhãn hàng sang tiếng Việt
            brand_vn_map = {
                'OLong Tea Plus': 'Trà Ô long Tea Plus',
                'Không Độ': 'Trà xanh Không Độ',
                'Trà Cozy đóng chai': 'Trà Cozy đóng chai',
                'Trà Tea Go': 'Trà Tea Go',
                'Trà mật ong Boncha': 'Trà mật ong Boncha'
            }
            switching_source.index = [brand_vn_map.get(str(x), str(x)) for x in switching_source.index]
            
            # Sắp xếp tăng dần để vẽ thanh ngang
            switching_source_sorted = switching_source.sort_values(ascending=True)
            
            fig_switch = go.Figure(go.Bar(
                y=switching_source_sorted.index,
                x=switching_source_sorted.values,
                orientation='h',
                marker_color='#3b903e',
                text=[f"{v:.1f}%" for v in switching_source_sorted.values],
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>Tỷ lệ chuyển đổi: %{x:.1f}%<extra></extra>"
            ))
            
            fig_switch.update_layout(
                xaxis_title="Tỷ lệ phần trăm người dùng Cozy (%)",
                yaxis_title="",
                height=350,
                margin=dict(l=10, r=20, t=20, b=10),
            )
            st.plotly_chart(_apply_cozy_theme(fig_switch), use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning("⚠️ Không tìm thấy người dùng trung thành Cozy BUMO trong Wave được chọn.")

    with col_right:
        st.subheader("🚫 2. Top 10 Rào cản ngăn cân nhắc thương hiệu Cozy")
        st.caption("Q.ME2: Lý do khiến đáp viên nhận biết Cozy nhưng từ chối cân nhắc mua? (%)")
        
        # Sắp xếp tăng dần để vẽ thanh ngang
        df_barriers_sorted = df_barriers.sort_values(ascending=True)
        
        fig_barriers = go.Figure(go.Bar(
            y=df_barriers_sorted.index,
            x=df_barriers_sorted.values,
            orientation='h',
            marker_color='#156835',
            text=[f"{v:.1f}%" for v in df_barriers_sorted.values],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Tỷ lệ rào cản: %{x:.1f}%<extra></extra>"
        ))
        
        fig_barriers.update_layout(
            xaxis_title="Tỷ lệ phần trăm đáp viên từ chối (%)",
            yaxis_title="",
            height=350,
            margin=dict(l=10, r=20, t=20, b=10),
        )
        st.plotly_chart(_apply_cozy_theme(fig_barriers), use_container_width=True, config={"displayModeBar": False})

    # ===== 4. TẤM THẺ ĐÚC KẾT CHIẾN LƯỢC (Insight Card) =====
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">🧠 ĐỘNG LỰC DỊCH CHUYỂN & NÚT THẮT SẢN PHẨM — PHÂN TÍCH CHUYÊN SÂU:</div>
            <div class="insight-main">
                <ul>
                    <li><strong>Đánh chiếm cực mạnh thị phần của OLong Tea Plus:</strong> Chỉ số Switching Source vạch trần một sự thật chấn động: có tới <strong>50.7% người dùng trung thành Cozy hiện tại trước đó uống OLong Tea Plus thường xuyên nhất!</strong> Cozy cũng thành công lôi kéo khách hàng từ Không Độ (22.5%) và C2 (16.9%).</li>
                    <li><strong>Lý giải driver đằng sau cú bứt phá:</strong> Cozy đánh trúng tệp khách hàng coi trọng sức khỏe của Tea Plus nhờ tung ra dòng sản phẩm cao cấp <strong>Trà Cozy Olong Xoài</strong>. Đây là SKU kết hợp tài tình giữa vị trà Olong thanh lành tốt sức khỏe và hương vị trái cây nhiệt đới ngọt ngào, tạo ra sức hút khó cưỡng cho nhóm khách hàng trung lưu.</li>
                    <li><strong>Rào cản vị giác (Flavor Barrier) đang kìm hãm thương hiệu:</strong> Lý do từ chối Cozy lớn nhất là <strong>Không thích vị / Vị không ngon (34.1%)</strong> và <strong>Nghèo nàn danh mục vị (20.8%)</strong>. Vị trà Cozy đậm chát đặc trưng trà Bắc có thể không hợp gu hảo ngọt của khách miền Nam. Cozy cần điều chỉnh vị thanh ngọt dịu nhẹ riêng cho khu vực phía Nam.</li>
                    <li><strong>Rào cản phân phối (Distribution Bottleneck):</strong> Cozy bị từ chối do <strong>Hỏi mua nhưng cửa hàng không bán (9.6%)</strong> và <strong>Không được ướp lạnh sẵn trong tủ mát (9.2%)</strong>. Nước giải khát đóng chai là ngành hàng mua sắm bốc đồng (impulse buy), nếu không mát lạnh sẵn tại tạp hóa, Cozy sẽ mất trắng cơ hội bán hàng vào tay đối thủ.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
