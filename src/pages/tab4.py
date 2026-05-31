import streamlit as st
import pandas as pd

def render_tab4(df: pd.DataFrame) -> None:
    """Render full strategic conclusion and action plan (Phần 5)."""
    # ===== 1. VẼ CÁC TARGET KPI CARDS CHO NĂM 2026 =====
    st.markdown(
"""<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-label">Thương hiệu tiêu điểm</div>
<div class="kpi-value">Cozy RTD Tea</div>
</div>
<div class="kpi-card">
<div class="kpi-label">Mục tiêu TOM Awareness (2026)</div>
<div class="kpi-value">15.0%</div>
</div>
<div class="kpi-card">
<div class="kpi-label">Mục tiêu Consideration (2026)</div>
<div class="kpi-value">55.0%</div>
</div>
<div class="kpi-card">
<div class="kpi-label">Trụ cột Chiến lược thực thi</div>
<div class="kpi-value">3 Giải pháp</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )
    st.divider()

    # ===== 2. LỘ TRÌNH CHIẾN LƯỢC TRỰC QUAN HÓA (HTML Roadmap) =====
    st.subheader("Lộ trình Chiến lược Đột phá Sức khỏe Thương hiệu Cozy (2025-2026)")
    st.markdown(
"""<div style="background: white; padding: 22px; border-radius: 18px; border: 1px solid rgba(21,104,53,0.15); box-shadow: 0 10px 24px rgba(21,104,53,0.04); margin-bottom: 1.5rem;">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 15px; position: relative;">
<div style="flex: 1; min-width: 240px; padding: 15px; border-radius: 12px; background: #f0fdf4; border-left: 5px solid #156835;">
<div style="font-weight: 700; color: #156835; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 5px;">Hành động 1 — Sản phẩm (SKU)</div>
<div style="font-size: 1.1rem; font-weight: 800; color: #14532d; margin-bottom: 8px;">Đẩy mạnh Olong Trái cây</div>
<div style="font-size: 0.85rem; color: #4e6556; line-height: 1.4;">
Khai thác triệt để nguồn chuyển đổi từ OLong Tea Plus (50.7%) bằng cách tung SKU Cozy Olong Xoài, Olong chanh muối và dâu tây.
</div>
</div>
<div style="font-size: 1.5rem; color: #3b903e; font-weight: 800; text-align: center;">➔</div>
<div style="flex: 1; min-width: 240px; padding: 15px; border-radius: 12px; background: #e8f5e8; border-left: 5px solid #3b903e;">
<div style="font-weight: 700; color: #3b903e; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 5px;">Hành động 2 — Thương hiệu (Branding)</div>
<div style="font-size: 1.1rem; font-weight: 800; color: #14532d; margin-bottom: 8px;">Tái định vị hiện đại, trẻ trung</div>
<div style="font-size: 0.85rem; color: #4e6556; line-height: 1.4;">
Thiết kế lại bao bì chai nhựa thon gọn và bắt mắt, truyền thông thông điệp năng động để bứt phá nút thắt Consideration lên 55%.
</div>
</div>
<div style="font-size: 1.5rem; color: #3b903e; font-weight: 800; text-align: center;">➔</div>
<div style="flex: 1; min-width: 240px; padding: 15px; border-radius: 12px; background: #dcfce7; border-left: 5px solid #14532d;">
<div style="font-weight: 700; color: #14532d; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 5px;">Hành động 3 — Phân phối (Distribution)</div>
<div style="font-size: 1.1rem; font-weight: 800; color: #14532d; margin-bottom: 8px;">Tài trợ tủ mát tạp hóa</div>
<div style="font-size: 0.85rem; color: #4e6556; line-height: 1.4;">
Giải quyết rào cản "Hỏi mua không có" (9.6%) và "Không ướp lạnh" (9.2%) bằng việc tài trợ điện, cấp tủ mát mang nhãn Cozy.
</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # ===== 3. CHI TIẾT 3 GIẢI PHÁP CHIẾN LƯỢC =====
    st.subheader("Chi tiết các trụ cột giải pháp thực thi (Khung ODTO)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
"""<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
<h3 style="color:#156835; font-size:1.15rem; margin-top:0;">1. ĐÁNH CHIẾM KHÁCH HÀNG ĐỐI THỦ</h3>
<p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
<b>Observation (Quan sát):</b> 50.7% lượng khách hàng mới dịch chuyển sang Cozy là từ nhóm người dùng trung thành của đối thủ OLong Tea Plus.<br><br>
<b>Driver (Động lực):</b> Nhu cầu tiêu dùng dịch chuyển mạnh mẽ sang các dòng trà Ô long trái cây cao cấp, vị tươi mát tự nhiên thay vì trà xanh nguyên bản.<br><br>
<b>Tension (Xung đột):</b> Khách hàng muốn trải nghiệm nhiều hương vị Ô long mới lạ nhưng danh mục Ô long trái cây hiện tại của Cozy vẫn còn khá hạn chế.<br><br>
<b>Opportunity (Cơ hội):</b> Dồn lực R&D và ngân sách Marketing tung thêm các SKU Ô long trái cây trendy (Olong Chanh Muối, Đào Cam Sả) để trực diện chiếm lĩnh phân khúc này.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
"""<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
<h3 style="color:#3b903e; font-size:1.15rem; margin-top:0;">2. THÁO GỠ NÚT THẮT CÂN NHẮC</h3>
<p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
<b>Observation (Quan sát):</b> Tỷ lệ Nhận biết cực cao (91.8%) nhưng tỷ lệ Cân nhắc mua lại lọt thỏm ở mức 38.4%, tạo ra nút thắt rò rỉ lớn nhất phễu.<br><br>
<b>Driver (Động lực):</b> Người tiêu dùng nhận biết Cozy qua lịch sử lâu đời và là nhãn hiệu trà túi lọc quen thuộc của gia đình.<br><br>
<b>Tension (Xung đột):</b> Thiết kế chai nhựa vuông kiểu cũ tạo cảm giác "truyền thống", thiếu bắt mắt và chưa năng động, năng lượng như tệp khách Gen Z kỳ vọng.<br><br>
<b>Opportunity (Cơ hội):</b> Tái thiết kế kiểu dáng chai thon gọn hiện đại và thực hiện chiến dịch truyền thông hình ảnh trẻ trung trên kênh Digital để bứt phá tỷ lệ Cân nhắc lên 55%.
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
"""<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
<h3 style="color:#14532d; font-size:1.15rem; margin-top:0;">3. KHƠI THÔNG KÊNH PHÂN PHỐI</h3>
<p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
<b>Observation (Quan sát):</b> Rào cản mua Cozy lớn nhất là "Hỏi mua nhưng cửa hàng không bán" (9.3%) và "Không được ướp lạnh sẵn" (9.2%).<br><br>
<b>Driver (Động lực):</b> Trà đóng chai RTD là sản phẩm mua sắm bốc đồng (impulse buy), khách hàng chỉ quyết định mua khi sản phẩm sẵn mát lạnh.<br><br>
<b>Tension (Xung đột):</b> Các tiệm tạp hóa truyền thống ngại trữ lạnh Cozy vì ưu tiên không gian tủ mát hữu hạn cho các hãng lớn có ngân sách tài trợ tủ riêng.<br><br>
<b>Opportunity (Cơ hội):</b> Triển khai chiến dịch tài trợ tủ mát Cozy hoặc hỗ trợ tiền điện ủ mát cho các đại lý tạp hóa trọng điểm để khơi thông dòng phân phối lạnh.
</p>
</div>""",
            unsafe_allow_html=True,
        )