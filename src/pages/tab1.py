import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def _apply_cozy_theme(fig: go.Figure) -> go.Figure:
    """Apply Cozy forest green styling to Plotly figures."""
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b2e22", family="sans-serif"),
        legend=dict(
            font=dict(color="#1b2e22", size=10),
            title=dict(font=dict(color="#1b2e22")),
            bgcolor="rgba(255,255,255,0.6)",
        ),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="rgba(21, 104, 53, 0.2)",
            font=dict(color="#1b2e22"),
        ),
    )
    fig.update_xaxes(
        tickfont=dict(color="#4e6556", size=10),
        gridcolor="rgba(21, 104, 53, 0.08)",
        zerolinecolor="rgba(21, 104, 53, 0.12)",
    )
    fig.update_yaxes(
        tickfont=dict(color="#4e6556", size=10),
        gridcolor="rgba(21, 104, 53, 0.08)",
        zerolinecolor="rgba(21, 104, 53, 0.12)",
    )
    return fig

def render_tab1(df: pd.DataFrame) -> None:
    """Render full demographics analysis (Phần 1)."""
    # ===== 1. TÍNH TOÁN CÁC KPI CHỦ CHỐT =====
    total_n = len(df)
    female_pct = (df['gender'].str.lower() == 'female').mean() * 100
    north_n = (df['region'].str.lower() == 'north').sum()
    north_pct = (df['region'].str.lower() == 'north').mean() * 100
    
    mid_income_vars = ['7,500,001 – 15,000,000 VND', '15,000,001 – 30,000,000 VND']
    mid_income_pct = df['income'].isin(mid_income_vars).mean() * 100

    # ===== 2. VẼ CÁC KPI CARDS (Dạng Cozy Glassmorphism) =====
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Tổng số đáp viên (N)</div>
                <div class="kpi-value">{total_n:,} người</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Tỉ lệ Giới tính Nữ</div>
                <div class="kpi-value">{female_pct:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Khu vực trọng tâm (Miền Bắc)</div>
                <div class="kpi-value">{north_n:,} ({north_pct:.1f}%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Tỷ lệ Thu nhập Trung lưu</div>
                <div class="kpi-value">{mid_income_pct:.1f}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # ===== 3. BIỂU ĐỒ HÀNG 1: 3 CỘT ĐỀU NHAU =====
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Region by Wave
        region_cross = pd.crosstab(df['region'], df['wave'])
        # Reorder region for logical flow
        region_order = ['North', 'Central', 'South', 'Mekong']
        region_cross = region_cross.reindex([r for r in region_order if r in region_cross.index])
        
        fig_region = go.Figure()
        fig_region.add_trace(go.Bar(
            x=region_cross.index, y=region_cross[2024],
            name="2024", marker_color="#b0b0b0", text=region_cross[2024], textposition="outside"
        ))
        fig_region.add_trace(go.Bar(
            x=region_cross.index, y=region_cross[2025],
            name="2025", marker_color="#156835", text=region_cross[2025], textposition="outside"
        ))
        fig_region.update_layout(
            title=dict(text="Khu vực Địa lý phỏng vấn (Region)", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="",
            yaxis_title="Số lượng đáp viên (n)",
            height=320,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=1.12, x=0),
            barmode='group'
        )
        st.plotly_chart(_apply_cozy_theme(fig_region), use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Gender by Wave
        gender_cross = pd.crosstab(df['gender'], df['wave'])
        fig_gender = go.Figure()
        fig_gender.add_trace(go.Bar(
            x=gender_cross.index, y=gender_cross[2024],
            name="2024", marker_color="#b0b0b0", text=gender_cross[2024], textposition="outside"
        ))
        fig_gender.add_trace(go.Bar(
            x=gender_cross.index, y=gender_cross[2025],
            name="2025", marker_color="#156835", text=gender_cross[2025], textposition="outside"
        ))
        fig_gender.update_layout(
            title=dict(text="Giới tính đáp viên (Gender)", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="",
            yaxis_title="Số lượng đáp viên (n)",
            height=320,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=1.12, x=0),
            barmode='group'
        )
        st.plotly_chart(_apply_cozy_theme(fig_gender), use_container_width=True, config={"displayModeBar": False})

    with col3:
        # Age Group by Wave
        age_cross = pd.crosstab(df['age_group'], df['wave'])
        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(
            x=age_cross.index, y=age_cross[2024],
            name="2024", marker_color="#b0b0b0", text=age_cross[2024], textposition="outside"
        ))
        fig_age.add_trace(go.Bar(
            x=age_cross.index, y=age_cross[2025],
            name="2025", marker_color="#156835", text=age_cross[2025], textposition="outside"
        ))
        fig_age.update_layout(
            title=dict(text="Nhóm tuổi đáp viên (Age group)", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="",
            yaxis_title="Số lượng đáp viên (n)",
            height=320,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=1.12, x=0),
            barmode='group'
        )
        st.plotly_chart(_apply_cozy_theme(fig_age), use_container_width=True, config={"displayModeBar": False})

    # ===== 4. BIỂU ĐỒ HÀNG 2: 60/40 SPLIT =====
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # Income Distribution (Horizontal Bar Chart)
        income_cross = pd.crosstab(df['income'], df['wave'])
        income_order = [
            '3,000,001 – 4,500,000 VND',
            '4,500,001 – 7,500,000 VND',
            '7,500,001 – 15,000,000 VND',
            '15,000,001 – 30,000,000 VND',
            '30,000,001 – 45,000,000 VND',
            'Above 45,000,001'
        ]
        income_cross = income_cross.reindex([i for i in income_order if i in income_cross.index])
        
        fig_income = go.Figure()
        fig_income.add_trace(go.Bar(
            y=income_cross.index, x=income_cross[2024],
            name="2024", orientation='h', marker_color="#b0b0b0", text=income_cross[2024], textposition="outside"
        ))
        fig_income.add_trace(go.Bar(
            y=income_cross.index, x=income_cross[2025],
            name="2025", orientation='h', marker_color="#156835", text=income_cross[2025], textposition="outside"
        ))
        fig_income.update_layout(
            title=dict(text="Thu nhập hộ gia đình hàng tháng (Income)", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="Số lượng đáp viên (n)",
            yaxis_title="",
            height=340,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=1.12, x=0),
            barmode='group'
        )
        st.plotly_chart(_apply_cozy_theme(fig_income), use_container_width=True, config={"displayModeBar": False})

    with col_right:
        # Wave breakdown comparison
        wave_counts = df['wave'].value_counts()
        fig_wave = go.Figure(data=[go.Pie(
            labels=[f"Năm {w}" for w in wave_counts.index],
            values=wave_counts.values,
            hole=0.55,
            marker=dict(colors=["#156835", "#b0b0b0"]),
            textinfo="value+percent",
            hovertemplate="<b>%{label}</b><br>Cỡ mẫu: %{value:,} người (%{percent})<extra></extra>"
        )])
        fig_wave.update_layout(
            title=dict(text="Quy mô mẫu theo năm thực hiện (Wave)", font=dict(color="#156835", size=14, family="sans-serif")),
            height=340,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=1.12, x=0)
        )
        st.plotly_chart(_apply_cozy_theme(fig_wave), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # ===== 5. BIỂU ĐỒ HÀNG 3: BỔ SUNG CÁC TIÊU CHÍ MỚI (TẦN SUẤT S3B, NGHỀ NGHIỆP, HỌC VẤN) =====
    st.markdown("<h3 style='color: #156835; font-size: 1.25rem; margin-top: 10px; margin-bottom: 20px;'>Hành vi sử dụng nền và Thông tin nhân khẩu bổ sung</h3>", unsafe_allow_html=True)
    col3_1, col3_2, col3_3 = st.columns(3)

    with col3_1:
        # S3b Frequency Analysis
        s3b_col = [c for c in df.columns if 'S3b' in c][0]
        s3b_counts = df[s3b_col].value_counts()
        freq_order = ['Once per day', '4-6 times/ week', '2-3 times/week', 'Once per week', '2-3 times/month', 'Once per month']
        s3b_counts = s3b_counts.reindex([f for f in freq_order if f in s3b_counts.index])

        fig_s3b = go.Figure(data=[go.Pie(
            labels=s3b_counts.index,
            values=s3b_counts.values,
            hole=0.45,
            marker=dict(colors=["#156835", "#227d43", "#3a9357", "#5cb278", "#88cca1", "#bcecd0"]),
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>Số lượng: %{value:,} (%{percent})<extra></extra>"
        )])
        fig_s3b.update_layout(
            title=dict(text="Tần suất uống Trà RTD trong 4 tuần", font=dict(color="#156835", size=14, family="sans-serif")),
            height=320,
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(orientation="h", y=-0.15, x=0)
        )
        st.plotly_chart(_apply_cozy_theme(fig_s3b), use_container_width=True, config={"displayModeBar": False})

    with col3_2:
        # Occupation Analysis
        occ_counts = df['occupation'].value_counts().head(7).sort_values(ascending=True)
        clean_labels = [o.split('. ')[-1] if '. ' in o else o for o in occ_counts.index]

        fig_occ = go.Figure(go.Bar(
            y=clean_labels,
            x=occ_counts.values,
            orientation='h',
            marker_color="#156835",
            text=[f"{v:,}" for v in occ_counts.values],
            textposition="outside",
            hovertemplate="<b>%{y}</b>: %{x:,} người<extra></extra>"
        ))
        fig_occ.update_layout(
            title=dict(text="Cơ cấu Nghề nghiệp đáp viên (Top 7)", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="Số lượng đáp viên (người)",
            height=320,
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(_apply_cozy_theme(fig_occ), use_container_width=True, config={"displayModeBar": False})

    with col3_3:
        # Education Analysis
        edu_counts = df['education'].value_counts().sort_values(ascending=True)
        clean_edu = [e.replace('Studying/Graduated from ', '').split(' and ')[0] for e in edu_counts.index]

        fig_edu = go.Figure(go.Bar(
            y=clean_edu,
            x=edu_counts.values,
            orientation='h',
            marker_color="#3b903e",
            text=[f"{v:,}" for v in edu_counts.values],
            textposition="outside",
            hovertemplate="<b>%{y}</b>: %{x:,} người<extra></extra>"
        ))
        fig_edu.update_layout(
            title=dict(text="Trình độ Học vấn của đáp viên", font=dict(color="#156835", size=14, family="sans-serif")),
            xaxis_title="Số lượng đáp viên (người)",
            height=320,
            margin=dict(l=10, r=10, t=55, b=10)
        )
        st.plotly_chart(_apply_cozy_theme(fig_edu), use_container_width=True, config={"displayModeBar": False})
