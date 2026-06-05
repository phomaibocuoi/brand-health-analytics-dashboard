# Cozy RTD Tea — Brand Health Dashboard

> **End-to-End Analytics Project | Python · Streamlit · Plotly**  
> Phân tích sức khỏe thương hiệu trà đóng chai (RTD Tea) **Cozy** tại thị trường Việt Nam, dựa trên dữ liệu khảo sát **2,600 đáp viên** toàn quốc (2024–2025).

🌐 **Live Dashboard:** [cozy-rtd-brand-health.streamlit.app](https://cozy-rtd-brand-health.streamlit.app)

---

## Project Summary

Dự án xây dựng dashboard phân tích thương hiệu tương tác, phục vụ đánh giá vị thế cạnh tranh của **Cozy** so với 7 đối thủ trực tiếp: C2, OLong Tea Plus, Không Độ, Dr. Thanh, Boncha, TH True Tea và Búp Non 365.

**Key Finding:** Cozy đạt mức độ nhận biết (Aided Awareness) rất cao ở Wave 2025 là **94.2%** (gần tương đương C2 là **97.5%**), nhưng tỷ lệ trung thành (BUMO) chỉ đạt **9.3%** (so với C2 là **31.1%**). Điểm nghẽn lớn nhất nằm ở bước Cân nhắc (Consideration) của Cozy chỉ đạt **38.1%** (trong khi C2 đạt **79.5%**), cho thấy khoảng trống lớn cần tháo gỡ về mặt định vị sản phẩm và hình ảnh thương hiệu.

---

## Analysis Pillars

| # | Topic | Nội dung |
|---|-------|----------|
| 1 | **Demographics & Behavior** | Chân dung khách hàng: vùng miền, độ tuổi, thu nhập, tần suất dùng |
| 2 | **Brand Health Funnel** | Phễu chuyển đổi: Awareness → Trial (P3M) → Regular Use (P4W) → BUMO |
| 3 | **Brand Imagery Mapping** | Bản đồ 18 thuộc tính lý tính & cảm tính |
| 4 | **Occasions & Media Touchpoints** | Bối cảnh tiêu dùng & hiệu quả kênh truyền thông |
| 5 | **Product Barriers & Switching Source** | Rào cản mua hàng & nguồn dịch chuyển thị phần |
| 6 | **Strategic ODTO Roadmap** | Khuyến nghị hành động tăng trưởng cho Cozy |

---

## Repository Structure

```text
cozy/
├── data/
│   ├── raw/                        # Dữ liệu gốc (immutable)
│   │   ├── Brandlist_RTDT.csv
│   │   ├── Dataset.csv             # 2,600 respondents
│   │   └── QNR_Reference.csv
│   └── processed/
│       └── Dataset_cleaned.csv     # File chính chạy Dashboard (6.3MB)
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb      # EDA, xử lý lỗi định dạng, làm sạch dữ liệu
│   └── 02_brand_health_analysis.ipynb
│
├── references/
│   ├── Brandlist_cleaned.csv
│   ├── QNR_Reference_cleaned.csv
│   ├── column_to_brand_mapping.csv
│   ├── cleaning_report_myInsight2026.xlsx
│   └── data_dictionary_cleaning_log.xlsx
│
├── src/
│   └── pages/
│       ├── overview.py             # Executive Summary
│       ├── tab1.py                 # Demographics & Behavior
│       ├── tab2.py                 # Brand Health Funnel
│       ├── tab3.py                 # Brand Imagery
│       ├── tab4.py                 # Strategic ODTO Roadmap
│       ├── tab5.py                 # Barriers & Switching Source
│       └── tab6.py                 # Occasions & Media Touchpoints
│
├── app.py                          # Entry point
└── requirements.txt
```

---

## Data Pipeline — Key Challenges Solved

### 1. Duplicate Removal Without Data Loss

Cột `Serial number` trong file thô được lưu dạng chuỗi có dấu phẩy (`1,00`, `2,00`). Ép kiểu số trực tiếp bằng `pd.to_numeric` sẽ chuyển toàn bộ thành `NaN`, khiến bước drop_duplicates xóa ~99.9% dòng dữ liệu.

**Giải pháp:** Thay `,` → `.` trước khi chuyển kiểu, bảo toàn đủ 2,600 dòng.

```python
df['serial'] = df['serial'].str.replace(',', '.').pipe(pd.to_numeric)
df.drop_duplicates(subset='serial', inplace=True)
```

### 2. Survey Routing Logic — Correct Base Calculation

Các ô `#NULL!` đại diện cho câu hỏi bị bỏ qua theo routing logic (đáp viên không nhận biết thương hiệu X sẽ không trả lời câu hỏi về rào cản của X). Impute bừa vào đây làm sai mẫu số tính toán.

**Giải pháp:** Map `#NULL!` → `np.nan`, tính tỷ lệ % dựa trên **base thực tế** của từng câu hỏi — không chia cho tổng 2,600.

```python
df.replace('#NULL!', np.nan, inplace=True)

# Tính % trên base thực tế
base = df['Q_barrier_cozy'].notna().sum()
rate = df['Q_barrier_cozy'].value_counts(normalize=False) / base * 100
```

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.9+ |
| Data Processing | `pandas`, `numpy`, `openpyxl` |
| EDA & Static Charts | `matplotlib`, `seaborn` |
| Interactive Dashboard | `streamlit==1.56.0` |
| Interactive Charts | `plotly==6.7.0` |

---

## Getting Started

**Prerequisites:** Python 3.9+

```bash
# 1. Clone repo
git clone https://github.com/phomaibocuoi/brand-health-analytics-dashboard.git
cd cozy

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run dashboard
streamlit run app.py
```

Ứng dụng mở tại `http://localhost:8501`.

---

## About

Dự án cá nhân — thực hiện toàn bộ quy trình: data cleaning, survey logic mapping, EDA, đến xây dựng dashboard tương tác phục vụ ra quyết định thương hiệu.

**Contact:** [LinkedIn](https://linkedin.com/in/hokhongtuyetnhu) · [Email](mailto:hokhongtuyetnhu0807@gmail.com)