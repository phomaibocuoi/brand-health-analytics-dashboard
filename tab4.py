import streamlit as st
import pandas as pd

def render_tab4(df: pd.DataFrame) -> None:
    """Render full strategic conclusion and action plan (Phần 5)."""
    # ===== 1. VẼ CÁC TARGET KPI CARDS CHO NĂM 2026 =====
    st.markdown(
"""
<div class="kpi-grid">
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
</div>
""",
        unsafe_allow_html=True,
    )
    st.divider()

    # ===== 2. LỘ TRÌNH CHIẾN LƯỢC TRỰC QUAN HÓA (HTML Roadmap) =====
    st.subheader("🗺️ Lộ trình Chiến lược Đột phá Sức khỏe Thương hiệu Cozy (2025-2026)")
    st.markdown(
"""
<div style="background: white; padding: 22px; border-radius: 18px; border: 1px solid rgba(21,104,53,0.15); box-shadow: 0 10px 24px rgba(21,104,53,0.04); margin-bottom: 1.5rem;">
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
</div>
""",
        unsafe_allow_html=True,
    )

    # ===== 3. CHI TIẾT 3 GIẢI PHÁP CHIẾN LƯỢC =====
    st.subheader("🎯 Chi tiết các trụ cột giải pháp thực thi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
"""
<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
    <h3 style="color:#156835; font-size:1.15rem; margin-top:0;">🍃 1. ĐÁNH CHIẾM KHÁCH HÀNG ĐỐI THỦ</h3>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Bối cảnh dữ liệu:</b> 50.7% khách hàng trung thành Cozy hiện tại dịch chuyển sang từ OLong Tea Plus. Điều này chứng minh định vị trà Olong trái cây cao cấp là vô cùng đúng đắn.
    </p>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Đề xuất thực thi:</b>
        <ul>
            <li>Dồn ngân sách R&D và Marketing cho dòng chủ lực <b>Cozy Olong Trái cây</b>.</li>
            <li>Tung thêm các SKU trendy như Olong chanh muối, Olong Đào Cam Sả.</li>
            <li>Tập trung truyền thông lợi ích kép: "Olong tốt cho sức khỏe + Vị xoài/trái cây thơm ngon".</li>
        </ul>
    </p>
</div>
""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
"""
<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
    <h3 style="color:#3b903e; font-size:1.15rem; margin-top:0;">⚡ 2. THÁO GỠ NÚT THẮT CÂN NHẮC</h3>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Bối cảnh dữ liệu:</b> Aided Awareness cực cao (91.8%) nhưng Consideration lọt thỏm chỉ đạt 38.4%. Rõ ràng khách hàng biết danh tiếng Cozy nhưng không cân nhắc mua uống.
    </p>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Đề xuất thực thi:</b>
        <ul>
            <li><b>Tái thiết kế bao bì:</b> Thay đổi kiểu chai nhựa từ dáng vuông truyền thống sang kiểu thon gọn, bắt mắt, dán nhãn decal tươi mát làm nổi bật màu trà.</li>
            <li><b>Tái định vị hình ảnh:</b> Thay đổi thông điệp từ "ấm áp gia đình" sang "năng động, tươi trẻ, refresh năng lượng cùng Gen Z".</li>
            <li>Tập trung ngân sách vào kênh Digital (TikTok/Instagram) thay vì PR truyền thống.</li>
        </ul>
    </p>
</div>
""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
"""
<div style="background: white; padding: 20px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.03); height: 100%;">
    <h3 style="color:#14532d; font-size:1.15rem; margin-top:0;">🧊 3. KHƠI THÔNG KÊNH PHÂN PHỐI</h3>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Bối cảnh dữ liệu:</b> Rào cản phân phối "Hỏi mua không có" chiếm 9.6% và "Không ướp lạnh sẵn trong tủ" chiếm 9.2%. Trà đóng chai là mua sắm bốc đồng, nếu không sẵn mát lạnh sẽ thất bại.
    </p>
    <p style="font-size:0.88rem; color:#4e6556; line-height:1.5;">
        <b>Đề xuất thực thi:</b>
        <ul>
            <li>Triển khai chương trình kích cầu bán lẻ <b>"Ủ mát Cozy - Bán liền sảng khoái"</b>.</li>
            <li>Tài trợ tiền điện tủ mát hoặc cấp tủ mát mang nhãn Cozy cho các tạp hóa truyền thống ở vùng ngoại ô thành phố lớn.</li>
            <li>Chiết khấu hoa hồng trưng bày POSM Cozy trực tiếp tại kệ tủ lạnh chính diện đại lý.</li>
        </ul>
    </p>
</div>
""",
            unsafe_allow_html=True,
        )

    # ===== 4. ĐÁNH GIÁ CHẤT LƯỢNG KỸ THUẬT DỮ LIỆU SẠCH (DATA PREPROCESSING QUALITY) =====
    st.subheader("🛠️ Báo cáo kỹ thuật: Quy trình Tiền xử lý & Làm sạch dữ liệu")
    
    st.markdown(
"""
<div style="background: #f7faf7; padding: 18px; border-radius: 16px; border: 1px solid rgba(21,104,53,0.15);">
    <p style="font-size: 0.9rem; color: #1b2e22; line-height: 1.5; margin: 0 0 10px 0;">
        Để xây dựng được hệ thống chỉ số sức khỏe thương hiệu có độ tin cậy tuyệt đối và trực quan hóa mượt mà trên dashboard này, toàn bộ dữ liệu khảo sát gốc đã được đội ngũ Data Engineer tiền xử lý nghiêm ngặt qua <b>Quy trình 3 chặng tiêu chuẩn</b>:
    </p>
    <ol style="font-size: 0.88rem; color: #4e6556; line-height: 1.6; margin: 0; padding-left: 20px;">
        <li><b>Chuẩn hóa cấu trúc và kiểu dữ liệu (Data Standardization):</b> Khắc phục triệt để lỗi định dạng thập phân và ký tự đặc biệt từ file Excel gốc. Loại bỏ hoàn toàn các giá trị lỗi hệ thống <code>#NULL!</code> và chuyển đổi khoa học thành <code>NaN</code> để không gây nhiễu cho tính toán thống kê.</li>
        <li><b>Ánh xạ Thương hiệu Đồng nhất (SKU to Master Brand mapping):</b> Thiết lập từ điển ánh xạ thông minh, chuyển đổi hàng chục SKU con của các hãng (ví dụ Cozy đào sả, Cozy vải, Cozy Olong xoài) về một Master Brand duy nhất là <code>Trà Cozy đóng chai</code> để đo lường chính xác sức mạnh tổng thể của thương hiệu.</li>
        <li><b>Tái cấu trúc Fact Table (Wide-to-Long Melting):</b> Triển khai kỹ thuật unpivot xoay bảng Fact gốc từ định dạng Wide sang định dạng Long độ phân giải cao (Fact table & Dimension table), lưu trữ hoàn hảo ký tự tiếng Việt với chuẩn mã hóa <code>utf-8-sig</code> phục vụ trực quan hóa hiệu năng cao trên Dashboard.</li>
    </ol>
</div>
""",
        unsafe_allow_html=True,
    )