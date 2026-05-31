from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import streamlit as st
import pandas as pd

# Import các tab phân tích tương ứng từ src/pages
from src.pages.overview import render_overview
from src.pages.tab1 import render_tab1
from src.pages.tab2 import render_tab2
from src.pages.tab3 import render_tab3
from src.pages.tab4 import render_tab4
from src.pages.tab5 import render_tab5
from src.pages.tab6 import render_tab6

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Cozy Brand Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

@dataclass(frozen=True)
class QuestionGroup:
    title: str
    subtitle: str
    question: str
    placeholder_charts: tuple[str, str, str]

# Định nghĩa 5 nhóm chuyên đề đúng theo cấu trúc và câu hỏi đề bài
GROUPS: tuple[QuestionGroup, ...] = (
    QuestionGroup(
        title="Tổng quan dự án",
        subtitle="Báo cáo sức khỏe thương hiệu Cozy Wave 2025 — Tóm tắt các chỉ số cốt lõi từ Nhận biết, Sử dụng, Phễu chuyển đổi đến Liên tưởng hình ảnh và Rào cản sản phẩm.",
        question="Tổng quan sức khỏe thương hiệu Trà Cozy đóng chai năm 2025",
        placeholder_charts=("Chỉ số KPI", "Phễu thương hiệu", "Xu hướng & Rào cản"),
    ),
    QuestionGroup(
        title="Nhân khẩu học & Tần suất",
        subtitle="Khám phá chân dung, bối cảnh địa lý, độ tuổi, giới tính, thu nhập, nghề nghiệp, học vấn và tần suất uống trà đóng chai của 2,600 đáp viên.",
        question="Chân dung nhân khẩu học và hành vi sử dụng nền của khách hàng RTD Tea",
        placeholder_charts=("Vùng địa lý & Giới tính", "Độ tuổi & Thu nhập", "Tần suất, Nghề nghiệp & Học vấn"),
    ),
    QuestionGroup(
        title="Hành vi & Sức khỏe thương hiệu",
        subtitle="Khám phá kim tự tháp nhận biết, mức độ thâm nhập và phễu chuyển đổi thương hiệu từ Nhận biết đến Trung thành.",
        question="Sức khỏe thương hiệu Trà Cozy đóng chai đang đứng ở vị trí nào so với các đối thủ cạnh tranh?",
        placeholder_charts=("Nhận biết thương hiệu", "Thâm nhập thị trường", "Phễu chuyển đổi"),
    ),
    QuestionGroup(
        title="Định vị hình ảnh thương hiệu",
        subtitle="Đánh giá mức độ liên tưởng của người tiêu dùng đối với 18 thuộc tính hình ảnh đặc trưng lý tính và cảm tính.",
        question="Trà Cozy đóng chai gắn liền với những liên tưởng hình ảnh thế mạnh nào?",
        placeholder_charts=("Bản đồ nhiệt liên tưởng", "So sánh thuộc tính đơn", ""),
    ),
    QuestionGroup(
        title="Dịp tiêu dùng & Kênh mua",
        subtitle="Phân tích sâu các dịp uống trà RTD, địa điểm mua sắm gần đây nhất và các kênh tiếp cận quảng cáo của khách hàng.",
        question="Khách hàng thường uống trà đóng chai vào dịp nào, mua ở đâu và chạm thương hiệu qua kênh nào?",
        placeholder_charts=("Dịp tiêu dùng", "Kênh mua sắm", "Điểm chạm truyền thông"),
    ),
    QuestionGroup(
        title="Phân tích sản phẩm & Rào cản",
        subtitle="Định vị nguồn gốc khách hàng chuyển dịch và vạch trần top 10 rào cản ngăn cản việc cân nhắc mua Cozy.",
        question="Lý do cốt lõi nào khiến khách hàng chưa đưa Cozy vào danh mục cân nhắc mua sắm?",
        placeholder_charts=("Nguồn chuyển đổi thương hiệu", "Rào cản sản phẩm & Phân phối", ""),
    ),
    QuestionGroup(
        title="Tổng kết & Lộ trình hành động",
        subtitle="Tóm tắt các phát hiện chiến lược cốt lõi và vạch ra lộ trình giải pháp 3 điểm bứt phá cho Cozy.",
        question="Lộ trình hành động đột phá giúp Cozy giải quyết điểm nghẽn và phát triển thị phần",
        placeholder_charts=("Lưu đồ lộ trình", "Chiến dịch hành động", ""),
    ),
)

def _inject_style() -> None:
    """Inject Cozy-themed custom CSS for premium look (Forest Green & White)."""
    st.markdown(
        """
        <style>
            :root {
                --bg: #f8faf8;
                --panel: rgba(255, 255, 255, 0.88);
                --panel-strong: #ffffff;
                --text: #1b2e22;
                --muted: #4e6556;
                --accent: #156835; /* Cozy Forest Green */
                --accent-soft: rgba(21, 104, 53, 0.12);
                --border: rgba(21, 104, 53, 0.12);
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(21, 104, 53, 0.12), transparent 30%),
                    radial-gradient(circle at top right, rgba(59, 144, 62, 0.12), transparent 28%),
                    linear-gradient(180deg, #f7faf7 0%, #edf2ee 100%);
                color: var(--text);
            }

            /* Customizing Sidebar */
            section[data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at 0% 0%, rgba(21, 104, 53, 0.35), transparent 32%),
                    radial-gradient(circle at 100% 18%, rgba(59, 144, 62, 0.30), transparent 36%),
                    linear-gradient(180deg, #0b2214 0%, #0c1c12 55%, #06110b 100%) !important;
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] h4,
            section[data-testid="stSidebar"] h5,
            section[data-testid="stSidebar"] h6,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] .stCaption {
                color: #f0fdf4 !important;
            }

            /* --- BẮT ĐẦU CSS ĐỒNG BỘ NÚT SIDEBAR --- */
            
            /* Tắt định dạng mặc định, ép chữ trắng tuyệt đối cho mọi thành phần trong nút */
            section[data-testid="stSidebar"] .stButton > button,
            section[data-testid="stSidebar"] .stButton > button * {
                background-color: transparent !important;
                background-image: none !important;
                color: #ffffff !important;
                font-family: "Source Sans Pro", sans-serif !important;
                font-weight: 600 !important;
            }

            /* Ép chung 1 màu xanh Cozy duy nhất cho TẤT CẢ các nút */
            section[data-testid="stSidebar"] .stButton > button {
                background: #156835 !important; 
                border: 1px solid rgba(167, 243, 208, 0.3) !important;
                border-radius: 8px !important;
                padding-top: 10px !important;
                padding-bottom: 10px !important;
                box-shadow: none !important;
                transition: all 0.2s ease !important;
            }

            /* Hover: Đổi màu nhẹ khi di chuột vào */
            section[data-testid="stSidebar"] .stButton > button:hover {
                background: #1e4b33 !important;
                border-color: rgba(167, 243, 208, 0.8) !important;
            }

            /* Xóa hiệu ứng khác biệt của nút primary (nút đang được chọn) để giống y hệt nút thường */
            section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
                background: #156835 !important;
                border: 1px solid rgba(167, 243, 208, 0.3) !important;
                box-shadow: none !important;
            }
            
            /* --- KẾT THÚC CSS ĐỒNG BỘ NÚT SIDEBAR --- */

            /* --- ĐỒNG BỘ MÀU CHIP BỘ LỌC MULTISELECT VÀ CHECKBOX SANG XANH COZY --- */
            span[data-baseweb="tag"] {
                background-color: #156835 !important;
                color: #ffffff !important;
                border-radius: 6px !important;
                border: 1px solid rgba(167, 243, 208, 0.2) !important;
            }
            span[data-baseweb="tag"] span {
                color: #ffffff !important;
            }
            span[data-baseweb="tag"] svg {
                fill: #ffffff !important;
            }
            /* Checkbox khi được chọn: đổi sang màu Cam Ấm Áp nổi bật (#ff9f1c) đồng bộ nhãn Trà Đào/Trà Cam Cozy */
            div[data-testid="stCheckbox"] label div[role="checkbox"][aria-checked="true"],
            div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] > div,
            .stCheckbox [aria-checked="true"] > div,
            div[role="checkbox"][aria-checked="true"] > div {
                background-color: #ff9f1c !important;
                border-color: #ff9f1c !important;
            }
            /* Trả lại nền trong suốt và chữ trắng cho nhãn chữ của checkbox */
            div[data-testid="stCheckbox"] label,
            div[data-testid="stCheckbox"] label span,
            div[data-testid="stCheckbox"] label p {
                background-color: transparent !important;
                color: #ffffff !important;
            }
            /* Hộp selectbox khi active/focus */
            div[data-baseweb="select"] > div:focus-within {
                border-color: #156835 !important;
            }
            /* --- KẾT THÚC CSS BỘ LỌC --- */

            section[data-testid="stSidebar"] div[data-testid="stAlert"] {
                background: linear-gradient(145deg, rgba(11, 34, 20, 0.75), rgba(21, 104, 53, 0.65)) !important;
                border: 1px solid rgba(167, 243, 208, 0.4) !important;
                border-radius: 12px !important;
            }

            section[data-testid="stSidebar"] div[data-testid="stAlert"] p {
                color: #e6f7ec !important;
            }

            /* Customizing Main Area */
            .hero {
                padding: 1.35rem 1.5rem;
                border: 1px solid var(--border);
                border-radius: 22px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(245, 250, 246, 0.8));
                box-shadow: 0 15px 40px rgba(21, 104, 53, 0.05);
                margin-bottom: 1.5rem;
            }

            .eyebrow {
                display: inline-block;
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: var(--accent);
                font-weight: 700;
                margin-bottom: 0.4rem;
            }

            .hero h1 {
                font-size: 2.1rem;
                line-height: 1.15;
                margin: 0;
                color: var(--accent);
                font-weight: 800;
            }

            .hero p {
                margin: 0.6rem 0 0;
                color: var(--muted);
                font-size: 0.95rem;
                line-height: 1.45;
                max-width: 62rem;
            }

            /* Customizing KPI cards */
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.9rem;
                margin: 0.15rem 0 0.5rem;
                align-items: stretch;
            }

            .kpi-grid-5 {
                grid-template-columns: 1fr 1.2fr 1fr 1.1fr 0.9fr;
            }

            .kpi-card {
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 0.35rem;
                padding: 0.9rem 1rem 0.8rem;
                min-height: 105px;
                border-radius: 16px;
                background: linear-gradient(140deg, #f0fdf4 0%, #dcfce7 45%, #bbf7d0 100%);
                border: 1px solid rgba(21, 104, 53, 0.22);
                box-shadow: 0 8px 24px rgba(21, 104, 53, 0.08);
                overflow: hidden;
            }

            .kpi-card::after {
                content: "";
                position: absolute;
                right: -15px;
                top: -15px;
                width: 65px;
                height: 65px;
                background: radial-gradient(circle, rgba(21, 104, 53, 0.22), rgba(21, 104, 53, 0));
                pointer-events: none;
            }

            .kpi-label {
                font-size: 0.82rem;
                font-weight: 650;
                letter-spacing: 0.02em;
                color: #14532d;
                margin-bottom: 0;
                line-height: 1.25;
            }

            .kpi-value {
                font-size: clamp(1.25rem, 1.4vw, 1.75rem);
                line-height: 1.1;
                font-weight: 800;
                color: #156835;
            }

            .kpi-value-compact {
                font-size: clamp(1.05rem, 1.1vw, 1.4rem);
                line-height: 1.2;
            }

            @media (max-width: 992px) {
                .kpi-grid,
                .kpi-grid-5 {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }

                .kpi-card {
                    min-height: 95px;
                }
            }

            @media (max-width: 600px) {
                .kpi-grid,
                .kpi-grid-5 {
                    grid-template-columns: 1fr;
                }
            }

            /* Customizing Insight cards */
            .insight-card {
                padding: 18px;
                border-radius: 18px;
                background: linear-gradient(135deg, #e6f4ea, #d0ebd6);
                border: 1px solid rgba(167, 243, 208, 0.65);
                box-shadow: 0 10px 24px rgba(21, 104, 53, 0.05);
                transition: 0.2s ease;
                margin-top: 1rem;
            }

            .insight-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 28px rgba(21, 104, 53, 0.08);
            }

            .insight-title {
                font-size: 15px;
                color: #14532d;
                margin-bottom: 5px;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .insight-main {
                font-size: 14px;
                font-weight: 500;
                color: #1b2e22;
                line-height: 1.5;
            }

            .insight-main strong {
                color: #156835;
                font-weight: 750;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _render_navigation_sidebar(groups: Iterable[QuestionGroup] = GROUPS) -> None:
    """Render navigation buttons in the sidebar (Forest Green & White)."""
    st.sidebar.markdown(
        """
        <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 0px;'>
            <h2 style='margin: 0; color: #ffffff; font-size: 1.6rem;'>Cozy RTD Tea</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Portfolio Dashboard — Phân tích sức khỏe thương hiệu")
    st.sidebar.markdown("---")
    
    groups_list = list(groups)
    for idx, group in enumerate(groups_list):
        is_selected = st.session_state.get("selected_group", 0) == idx
        # Ký tự tích xanh thanh lịch biểu thị trang hiện tại
        button_text = f"{'✓  ' if is_selected else '    '}{group.title}"
        
        if st.sidebar.button(
            button_text,
            key=f"btn_{idx}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_group = idx
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Ý nghĩa:** Hệ thống báo cáo phân tích toàn diện Sức khỏe Thương hiệu Trà Cozy đóng chai (Cozy RTD Tea) "
        "dựa trên khảo sát 2,600 đáp viên qua các Wave 2024 - 2025, hỗ trợ nhãn hàng hoạch định chiến lược kinh doanh "
        "và Marketing cho giai đoạn 2025 - 2026."
    )

def _render_group_hero(group: QuestionGroup) -> None:
    """Render the Hero Section for the selected page."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{group.title}</div>
            <h1>{group.question}</h1>
            <p>{group.subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    """Load, clean, and map ready-to-drink tea brand survey data."""
    df = pd.read_csv("data/processed/Dataset_cleaned.csv", low_memory=False)
    
    brand_to_master = {
        'C2': 'C2',
        'C2 - Không xác định': 'C2',
        'C2 - Vị chanh': 'C2',
        'C2 - Vị táo': 'C2',
        'C2 - Vị đào': 'C2',
        'C2 - Olong Hoa hồng': 'C2',
        'C2 - Olong Chanh': 'C2',
        'C2 – Hồng Trà': 'C2',
        'C2 – Hồng Trà Đào': 'C2',
        'C2 – Hồng Trà Vải': 'C2',
        'C2 – Freeze Hương chanh tuyết bạc hà': 'C2',
        'C2 – Freeze Hương dâu anh đào': 'C2',
        'C2 – Dưa lưới': 'C2',
        
        'OLong Tea Plus': 'OLong Tea Plus',
        'OLong Tea Plus.1': 'OLong Tea Plus',
        'OLong Tea Plus vị chanh': 'OLong Tea Plus',
        'Trà xanh matcha Tea Plus': 'OLong Tea Plus',
        
        'Không Độ': 'Không Độ',
        'Không Độ - Không xác định': 'Không Độ',
        'Không Độ - Vị chanh': 'Không Độ',
        'Không Độ - Bí đao': 'Không Độ',
        
        'Trà Cozy đóng chai': 'Trà Cozy đóng chai',
        'Trà Cozy Olong Xoài': 'Trà Cozy đóng chai',
        'Trà Cozy Vải': 'Trà Cozy đóng chai',
        'Trà Cozy Đào Sả': 'Trà Cozy đóng chai',
        
        'Dr. Thanh': 'Dr. Thanh',
        'Dr. Thanh - Không xác định': 'Dr. Thanh',
        'Dr. Thanh - Có đường': 'Dr. Thanh',
        'Dr. Thanh - Không đường': 'Dr. Thanh',
        
        'Trà Tea Go': 'Trà Tea Go',
        'Trà Tea Go – Vị Đào': 'Trà Tea Go',
        'Trà Tea Go – Vị Chanh': 'Trà Tea Go',
        
        'Trà sữa ít đường Vinamilk Happy Milktea': 'Trà sữa ít đường Vinamilk Happy Milktea',
        'Trà sữa ít đường Vinamilk Happy Milktea.1': 'Trà sữa ít đường Vinamilk Happy Milktea',
        
        'Trà lá vối Seventy': 'Trà lá vối Seventy',
        'Trà lá vối Seventy.1': 'Trà lá vối Seventy',
        
        'Trà thảo mộc VietFuji': 'Trà thảo mộc VietFuji',
        
        'Trà sữa không độ/ Trà sữa Macchiato': 'Trà sữa không độ/ Trà sữa Macchiato',
        'Trà sữa không độ/ Trà sữa Macchiato.1': 'Trà sữa không độ/ Trà sữa Macchiato',
        
        'Trà TH True Tea': 'Trà TH True Tea',
        'TH True Tea – Trà Oolong Tự Nhiên': 'Trà TH True Tea',
        'TH True Tea – Trà xanh vị chanh Tự Nhiên': 'Trà TH True Tea',
        
        'Trà mật ong Boncha': 'Trà mật ong Boncha',
        'Trà mật ong Boncha.1': 'Trà mật ong Boncha',
        'Trà mật ong Boncha vị chanh': 'Trà mật ong Boncha',
        
        'Trà Jokky': 'Trà Jokky',
        'Trà Jokky chanh sả': 'Trà Jokky',
        'Trà Jokky vị Đào': 'Trà Jokky',
        'Trà Jokky sâm': 'Trà Jokky',
        
        'Trà sữa C2': 'Trà sữa C2',
        
        'Búp non 365': 'Búp non 365',
        'Búp non 365 hương đào': 'Búp non 365',
        'Búp non 365 chanh sả': 'Búp non 365',
        'Búp non 365 mật ong': 'Búp non 365',
        'Búp non 365 mãng cầu': 'Búp non 365'
    }
    
    df['tom_master'] = df['Q1.TOM'].map(brand_to_master)
    df['bumo_master'] = df['Q5.Bumo'].map(brand_to_master)
    return df

def _render_page_content(selected_idx: int, df: pd.DataFrame) -> None:
    """Render corresponding dashboard page based on selection."""
    if selected_idx == 0:
        render_overview(df)
    elif selected_idx == 1:
        render_tab1(df)
    elif selected_idx == 2:
        render_tab2(df)
    elif selected_idx == 3:
        render_tab3(df)
    elif selected_idx == 4:
        render_tab6(df)  # Dịp tiêu dùng & Kênh truyền thông (tab6)
    elif selected_idx == 5:
        render_tab5(df)  # Rào cản sản phẩm (tab5)
    elif selected_idx == 6:
        render_tab4(df)  # Tổng kết chiến lược (tab4)

def main() -> None:
    # 1. Cấu hình màu nền và styles
    _inject_style()
    
    # 2. Vẽ thanh điều hướng Sidebar
    _render_navigation_sidebar()
    
    # 3. Đọc dữ liệu (có caching để đảm bảo hiệu suất cực cao)
    try:
        df = load_dataset()
    except Exception as e:
        st.error(f"❌ Không thể đọc tệp dữ liệu sạch: {e}")
        st.info("Vui lòng đảm bảo tệp dữ liệu sạch đang nằm ở đường dẫn: `data/processed/Dataset_cleaned.csv`")
        return
        
    # 4. Xác định chuyên đề đang chọn (mặc định là chuyên đề đầu tiên)
    selected_idx = st.session_state.get("selected_group", 0)
    selected_group = GROUPS[selected_idx]
    
    # 5. Vẽ Hero Section
    _render_group_hero(selected_group)
    
    # 6. Vẽ nội dung phân tích chi tiết của chuyên đề
    _render_page_content(selected_idx, df)

if __name__ == "__main__":
    main()