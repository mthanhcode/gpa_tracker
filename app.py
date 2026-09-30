import streamlit as st
import pandas as pd
from src.grading import calculate_final_score, convert_score, calculate_gpa, classify, predict_score
from src.storage import load_courses, save_courses
import plotly.express as px

# 1. Cấu hình trang Web
st.set_page_config(
    page_title="GPA Tracker - HITC",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Neon Glow & Electric Blue Theme
st.markdown("""
<style>
    @keyframes neonPulse {
        0%, 100% {
            text-shadow: 0 0 7px #00d2ff, 0 0 10px #00d2ff, 0 0 21px #00d2ff, 0 0 42px #0066ff;
        }
        50% {
            text-shadow: 0 0 2px #00d2ff, 0 0 5px #00d2ff, 0 0 10px #00d2ff, 0 0 15px #0066ff;
        }
    }

    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Gradient & Neon Title */
    .main-title {
        font-size: 2.3rem;
        font-weight: 900;
        color: #00d2ff;
        animation: neonPulse 2.5s infinite alternate;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-title {
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    /* Cyber Neon Metric Card Wrapper */
    .neon-card-wrapper {
        position: relative;
        border-radius: 14px;
        padding: 2px;
        background: linear-gradient(60deg, #00d2ff, #3a7bd5, #00f2fe, #4facfe);
        background-size: 300% 300%;
        animation: borderGlow 4s ease infinite;
        box-shadow: 0 0 12px rgba(0, 210, 255, 0.35);
        transition: all 0.3s ease;
    }
    .neon-card-wrapper:hover {
        box-shadow: 0 0 22px rgba(0, 210, 255, 0.7);
        transform: translateY(-3px);
    }

    /* Card Inner Body */
    .neon-card-body {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Tải dữ liệu
courses = load_courses()

# --- HEADER SECTION ---
st.markdown('<p class="main-title">🎓 HITC ACADEMIC DASHBOARD</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Hệ thống quản lý điểm tích lũy & dự đoán mục tiêu GPA chuẩn quy chế HITC</p>', unsafe_allow_html=True)

# --- SIDEBAR: THÊM MÔN HỌC ---
with st.sidebar:
    st.markdown("<h2 style='margin-bottom: 0px;'>📝 Thêm Môn Học Mới</h2>", unsafe_allow_html=True)
    st.caption("Nhập thông tin môn học để ghi vào hệ thống")
    
    with st.form("add_course_form", clear_on_submit=True):
        name = st.text_input("Tên môn học", placeholder="Ví dụ: Lập trình Python")
        semester = st.selectbox("Học kỳ", ["HK1", "HK2", "HK3", "HK4", "HK5", "HK6"])
        credits = st.number_input("Số tín chỉ", min_value=1, max_value=10, value=3)
        midterm = st.number_input("Điểm TBTK (40%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
        final = st.number_input("Điểm Cuối Kỳ (60%)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        counts_in_gpa = st.checkbox("Tính vào GPA tích lũy", value=True)
        
        submitted = st.form_submit_button("➕ Thêm Môn Học", use_container_width=True, type="primary")
        
        if submitted:
            if name.strip():
                final_score = calculate_final_score(midterm, final)
                letter, gpa4 = convert_score(final_score)
                new_course = {
                    "name": name,
                    "credits": credits,
                    "midterm": midterm,
                    "final": final,
                    "final_score": final_score,
                    "semester": semester,
                    "counts_in_gpa": counts_in_gpa
                }
                courses.append(new_course)
                save_courses(courses)
                st.toast(f"Đã thêm thành công: **{name}**", icon="🎉")
                st.rerun()
            else:
                st.error("Vui lòng nhập tên môn học!")

# --- METRICS DASHBOARD (NEON EFFECT) ---
gpa10, gpa4 = calculate_gpa(courses)
academic_rank = classify(gpa4)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="neon-card-wrapper">
        <div class="neon-card-body">
            <div class="metric-label">GPA Hệ 10</div>
            <div class="metric-value">{gpa10:.2f}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="neon-card-wrapper">
        <div class="neon-card-body">
            <div class="metric-label">GPA Hệ 4</div>
            <div class="metric-value" style="color: #0088ff;">{gpa4:.2f}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="neon-card-wrapper">
        <div class="neon-card-body">
            <div class="metric-label">Xếp Loại Học Tập</div>
            <div class="metric-value" style="color: #10b981;">{academic_rank}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="neon-card-wrapper">
        <div class="neon-card-body">
            <div class="metric-label">Tổng Môn Học</div>
            <div class="metric-value">{len(courses)}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN CONTENT TABS ---
tab1, tab2, tab3 = st.tabs(["📋 Bảng Điểm Tích Lũy", "📊 Biểu Đồ Điểm Số", "🔮 Dự Đoán Mục Tiêu"])

with tab1:
    if not courses:
        st.info("📌 Chưa có môn học nào trong danh sách. Hãy thêm môn học ở góc bên trái!")
    else:
        display_data = []
        for idx, c in enumerate(courses):
            letter, system4 = convert_score(c["final_score"])
            display_data.append({
                "STT": idx + 1,
                "Học kỳ": c.get("semester", "N/A"),
                "Tên môn học": c["name"],
                "Tín chỉ": c["credits"],
                "TBTK (40%)": c["midterm"],
                "Cuối kỳ (60%)": c["final"],
                "Tổng kết": c["final_score"],
                "Điểm chữ": letter,
                "Điểm hệ 4": system4,
                "Tính GPA": "✅" if c.get("counts_in_gpa", True) else "❌"
            })
        
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        col_del1, col_del2 = st.columns([3, 1])
        with col_del1:
            selected_idx = st.selectbox(
                "Chọn môn học muốn xóa khỏi bảng điểm:", 
                range(len(courses)), 
                format_func=lambda i: f"{courses[i]['name']} ({courses[i].get('semester', '')}) - Điểm TK: {courses[i]['final_score']}"
            )
        with col_del2:
            st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Xóa Môn Học", type="primary", use_container_width=True):
                removed = courses.pop(selected_idx)
                save_courses(courses)
                st.toast(f"Đã xóa môn {removed['name']}", icon="🗑️")
                st.rerun()

with tab2:
    if not courses:
        st.info("Cần ít nhất 1 môn học để hiển thị biểu đồ phân tích!")
    else:
        st.subheader("📈 So Sánh Điểm Tổng Kết Các Môn")
        
        chart_data = pd.DataFrame({
            "Môn học": [c["name"] for c in courses],
            "Điểm Tổng Kết": [c["final_score"] for c in courses],
            "Học kỳ": [c.get("semester", "HK1") for c in courses]
        })
        
        fig = px.bar(
            chart_data,
            x="Môn học",
            y="Điểm Tổng Kết",
            text="Điểm Tổng Kết",
            color_discrete_sequence=["#00d2ff"],
            hover_data={"Học kỳ": True, "Điểm Tổng Kết": ":.2f"}
        )
        
        fig.update_traces(
            texttemplate='%{text:.2f}', 
            textposition='outside',
            marker_line_color='#00f2fe',
            marker_line_width=1.5,
            opacity=0.9
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#e2e8f0", size=13),
            xaxis=dict(
                title=dict(text="<b>Môn học</b>", font=dict(size=14, color="#94a3b8")),
                tickangle=0,
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Điểm Tổng Kết</b>", font=dict(size=14, color="#94a3b8")),
                range=[0, 10.5],
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            margin=dict(l=20, r=20, t=30, b=50),
            height=420
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🎯 Tính Điểm Thi Cuối Kỳ Cần Đạt")
    st.write("Nhập điểm TBTK hiện tại và điểm Tổng kết mong muốn để hệ thống tính toán điểm thi tối thiểu bạn cần đạt.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_midterm = st.number_input("Điểm TBTK hiện tại (40%)", min_value=0.0, max_value=10.0, value=6.5, step=0.1, key="predict_midterm_input")
    with col_p2:
        p_target = st.number_input("Điểm Tổng kết mục tiêu", min_value=0.0, max_value=10.0, value=7.5, step=0.1, key="predict_target_input")

    if st.button("🔮 Tính Toán Điểm Cần Đạt", type="primary"):
        needed = predict_score(p_midterm, p_target)
        
        if needed > 10.0:
            max_possible_final = round(0.4 * p_midterm + 0.6 * 10.0, 2)
            
            st.markdown(f'''
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-radius: 10px; padding: 16px 20px; color: #dc2626; box-shadow: 0 0 12px rgba(239, 68, 68, 0.3); font-weight: 600;">
                ⚠️ <b>Mục tiêu không thể đạt được!</b> Với điểm TBTK hiện tại ({p_midterm:.1f}), dù bạn thi cuối kỳ đạt điểm tuyệt đối <b>10.0</b> thì điểm tổng kết tối đa cũng chỉ đạt <b>{max_possible_final:.2f}</b> (không thể đạt mục tiêu {p_target:.1f}).
            </div>
            ''', unsafe_allow_html=True)
            
        elif needed <= 0.0:
            st.balloons()
            st.markdown(f'''
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 10px; padding: 16px 20px; color: #047857; box-shadow: 0 0 12px rgba(16, 185, 129, 0.3); font-weight: 600;">
                🎉 <b>Mục tiêu đã sẵn sàng!</b> Với điểm TBTK là <b>{p_midterm:.1f}</b>, bạn đã chắc chắn đạt mục tiêu <b>{p_target:.1f}</b> mà không cần lo điểm thi cuối kỳ!
            </div>
            ''', unsafe_allow_html=True)
            
        else:
            st.markdown(f'''
            <div style="background: rgba(0, 210, 255, 0.1); border: 1px solid #00d2ff; border-radius: 10px; padding: 16px 20px; color: #0369a1; box-shadow: 0 0 12px rgba(0, 210, 255, 0.35); font-weight: 600;">
                💡 Để đạt mục tiêu <b>{p_target:.1f}</b>, điểm thi cuối kỳ tối thiểu bạn cần đạt là: <span style="font-size: 1.3rem; color: #0284c7;">{needed:.2f}</span> điểm.
            </div>
            ''', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding-top: 10px; padding-bottom: 20px; color: #64748B;'>
    <p style='font-size: 15px; margin-bottom: 10px;'>
        🧑‍💻 <b>mthanhcode</b> · Sinh viên HITC · Capstone Project Python Journey 🎓
    </p>
    <a href='https://github.com/mthanhcode/gpa_tracker' target='_blank' style='
        color: #00d2ff; 
        text-decoration: none; 
        font-weight: 600; 
        padding: 8px 16px; 
        border: 1px solid #00d2ff; 
        border-radius: 8px; 
        display: inline-block; 
        transition: all 0.3s ease;
        box-shadow: 0 0 8px rgba(0, 210, 255, 0.2);
    '>
        <span style='margin-right: 5px;'>⭐</span> Xem mã nguồn trên GitHub
    </a>
</div>
""", unsafe_allow_html=True)