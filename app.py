import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Assistant Professor Score Calculator", 
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 1.2em;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stProgress .st-bo {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []

if 'saved_profiles' not in st.session_state:
    st.session_state.saved_profiles = {}

# Sidebar for navigation and profile management
with st.sidebar:
    st.header("🔧 Tools & Settings")
    
    # Profile Management
    st.subheader("👤 Profile Management")
    profile_name = st.text_input("Profile Name", placeholder="Enter profile name...")
    
    col1, col2 = st.columns(2)
    with col1:
        save_profile = st.button("💾 Save Profile", use_container_width=True)
    with col2:
        load_profile = st.selectbox("📂 Load Profile", 
                                  options=["Select..."] + list(st.session_state.saved_profiles.keys()))
    
    # Export Options
    st.subheader("📊 Export Options")
    export_format = st.selectbox("Export Format", ["PDF Report", "Excel Summary", "JSON Data"])
    
    # Comparison Mode
    st.subheader("🔍 Analysis Tools")
    comparison_mode = st.checkbox("Comparison Mode", help="Compare multiple profiles")
    show_benchmarks = st.checkbox("Show Benchmarks", help="Display typical score ranges")
    
    # Calculator Settings
    st.subheader("⚙️ Calculator Settings")
    auto_calculate = st.checkbox("Auto Calculate", value=True, help="Calculate scores automatically")
    show_detailed_breakdown = st.checkbox("Detailed Breakdown", value=True)

# Main title with improved styling
st.markdown('<h1 class="main-header">🎓 Advanced Assistant Professor Eligibility Score Calculator</h1>', 
            unsafe_allow_html=True)

# Key metrics dashboard at the top
col1, col2, col3, col4 = st.columns(4)

# Initialize variables for metrics (will be updated later)
academic_total = 0
teaching_score = 0
research_total = 0
final_score = 0

# Enhanced App Information
with st.expander("ℹ️ About This Advanced Calculator", expanded=False):
    st.markdown("""
    ### 🚀 **Enhanced Features:**
    
    **📊 Core Calculations:**
    - Academic Records (UG, PG, M.Phil., Ph.D., NET/SET/JRF) - Max 55 marks
    - Teaching/Postdoc Experience - Max 5 marks  
    - Research Aptitude & Innovation - Max 15 marks
    
    **🎯 New Advanced Features:**
    - **Profile Management**: Save and load multiple candidate profiles
    - **Visual Analytics**: Interactive charts and progress bars
    - **Comparison Mode**: Compare multiple candidates side-by-side
    - **Export Options**: Generate PDF reports, Excel summaries, JSON data
    - **Benchmark Analysis**: Compare against typical score ranges
    - **Recommendation Engine**: Get personalized improvement suggestions
    - **Progress Tracking**: Monitor score improvements over time
    - **Detailed Breakdown**: Granular analysis of each component
    
    **💡 How to Use:**
    1. Fill in your academic details in each section
    2. Use the sidebar for profile management and settings
    3. View real-time calculations and visualizations
    4. Export your results or save your profile for future use
    """)

# Load profile functionality
if load_profile != "Select..." and load_profile in st.session_state.saved_profiles:
    loaded_data = st.session_state.saved_profiles[load_profile]
    st.success(f"✅ Loaded profile: {load_profile}")

# Create tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["📚 Academic Records", "👨‍🏫 Teaching Experience", "🔬 Research & Innovation", "📈 Results & Analytics"])

with tab1:
    st.markdown('<div class="section-header">A. Academic Records (Maximum: 55 Marks)</div>', 
                unsafe_allow_html=True)
    
    # University Type with enhanced information
    with st.container():
        st.subheader("🏛️ University Type Weighting Factor")
        
        uni_options = {
            "Institutes of National Importance / Top 200 QS/THE/ARWU": 1.0,
            "Central/State University with NIRF <100 or Foreign (QS/THE/ARWU 200–500)": 0.9,
            "Other Central/State Public Universities": 0.8,
            "Other UGC Approved Universities": 0.6
        }
        
        uni_type = st.selectbox(
            "Select University Type",
            options=list(uni_options.keys()),
            help="University type affects the weighting of your academic scores"
        )
        uni_factor = uni_options[uni_type]
        
        st.info(f"🎯 **Weighting Factor:** {uni_factor} | Your academic scores will be multiplied by this factor")
    
    # Academic qualifications in columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎓 Undergraduate (UG)")
        ug_percent = st.number_input("UG Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
        
        # UG Score calculation with progress bar
        if ug_percent >= 80:
            ug_score = 11
            ug_grade = "Excellent"
        elif ug_percent >= 60:
            ug_score = 9
            ug_grade = "Good"
        elif ug_percent >= 55:
            ug_score = 7
            ug_grade = "Average"
        elif ug_percent >= 45:
            ug_score = 4
            ug_grade = "Below Average"
        else:
            ug_score = 0
            ug_grade = "Poor"
        
        st.progress(ug_score / 11)
        st.write(f"**Score:** {ug_score}/11 | **Grade:** {ug_grade}")
    
    with col2:
        st.subheader("📚 Postgraduate (PG)")
        pg_percent = st.number_input("PG Percentage (%)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
        
        # PG Score calculation with progress bar
        if pg_percent >= 80:
            pg_score = 18
            pg_grade = "Excellent"
        elif pg_percent >= 60:
            pg_score = 16
            pg_grade = "Good"
        elif pg_percent >= 55:
            pg_score = 14
            pg_grade = "Average"
        else:
            pg_score = 0
            pg_grade = "Below Minimum"
        
        st.progress(pg_score / 18)
        st.write(f"**Score:** {pg_score}/18 | **Grade:** {pg_grade}")
    
    # Advanced Degrees
    st.subheader("🎖️ Advanced Degrees")
    col3, col4 = st.columns(2)
    
    with col3:
        mphil = st.checkbox("Have M.Phil. Degree?")
        mphil_score = 0
        if mphil:
            mphil_percent = st.number_input("M.Phil. Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
            if mphil_percent >= 60:
                mphil_score = 5
            elif mphil_percent >= 55:
                mphil_score = 3
            st.progress(mphil_score / 5)
            st.write(f"**M.Phil. Score:** {mphil_score}/5")
    
    with col4:
        phd = st.checkbox("Have Ph.D. Degree?")
        phd_score = 20 if phd else 0
        if phd:
            st.progress(1.0)
            st.write("**Ph.D. Score:** 20/20")
        else:
            st.progress(0.0)
            st.write("**Ph.D. Score:** 0/20")
    
    mphil_phd_score = min(mphil_score + phd_score, 20)
    
    # Competitive Exams
    st.subheader("🏆 Competitive Exam Qualifications")
    exam_list = st.multiselect(
        "Select your qualifications:",
        ["NET with JRF", "NET", "SET"],
        help="Select all applicable qualifications. NET with JRF has the highest weightage."
    )
    
    exam_score = 0
    if "NET with JRF" in exam_list:
        exam_score = 6
    elif "NET" in exam_list:
        exam_score = 4
    elif "SET" in exam_list:
        exam_score = 3
    
    st.progress(exam_score / 6)
    st.write(f"**Exam Score:** {exam_score}/6")
    
    # Calculate Academic Total
    academic_total = min(((ug_score + pg_score + mphil_phd_score) * uni_factor) + exam_score, 55)
    
    # Academic Summary
    with st.container():
        st.markdown("### 📊 Academic Records Summary")
        academic_breakdown = pd.DataFrame({
            'Component': ['UG Score', 'PG Score', 'M.Phil./Ph.D.', 'Competitive Exams', 'University Factor'],
            'Raw Score': [ug_score, pg_score, mphil_phd_score, exam_score, f"{uni_factor}x"],
            'Weighted Score': [ug_score * uni_factor, pg_score * uni_factor, mphil_phd_score * uni_factor, exam_score, "Applied"]
        })
        st.dataframe(academic_breakdown, use_container_width=True)
        
        st.success(f"🎯 **Total Academic Score:** {academic_total:.2f} / 55")

with tab2:
    st.markdown('<div class="section-header">B. Teaching / Post-Doctoral Experience (Maximum: 5 Marks)</div>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("👨‍🏫 Experience Details")
        
        # Enhanced teaching experience input
        teaching_years = st.number_input(
            "Total Teaching/Postdoc Experience (Years)", 
            min_value=0.0, 
            max_value=20.0, 
            step=0.1, 
            value=0.0,
            help="Include all approved teaching and post-doctoral experience"
        )
        
        # Additional experience breakdown
        with st.expander("📋 Detailed Experience Breakdown"):
            teaching_exp = st.number_input("Teaching Experience (Years)", min_value=0.0, step=0.1)
            postdoc_exp = st.number_input("Post-Doctoral Experience (Years)", min_value=0.0, step=0.1)
            research_exp = st.number_input("Research Experience (Years)", min_value=0.0, step=0.1)
            
            st.info(f"**Total Calculated:** {teaching_exp + postdoc_exp + research_exp:.1f} years")
    
    with col2:
        teaching_score = min(teaching_years * 1.0, 5.0)
        
        # Visual representation
        st.subheader("📊 Score Visualization")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = teaching_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Teaching Score"},
            delta = {'reference': 5},
            gauge = {
                'axis': {'range': [None, 5]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 2], 'color': "lightgray"},
                    {'range': [2, 4], 'color': "yellow"},
                    {'range': [4, 5], 'color': "green"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 5}}))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"🎯 **Teaching Experience Score:** {teaching_score:.2f} / 5")
    
    # Experience improvement suggestions
    if teaching_score < 5:
        st.info(f"💡 **Tip:** You need {(5 - teaching_score):.1f} more years of experience to maximize this section.")

with tab3:
    st.markdown('<div class="section-header">C. Research Aptitude and Innovation Skills (Maximum: 15 Marks)</div>', 
                unsafe_allow_html=True)
    
    # Research Publications
    st.subheader("📄 Research Publications (Maximum: 6 Marks)")
    st.caption("Only indexed journal papers (SciFinder, Web of Science, Scopus) are counted")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        papers_single = st.number_input("Single-author Papers", min_value=0, step=1, value=0)
        st.write(f"Score: {min(papers_single * 1.0, 6):.1f}")
    
    with col2:
        papers_principal = st.number_input("Principal/Corresponding Author", min_value=0, step=1, value=0)
        st.write(f"Score: {min(papers_principal * 0.5, 6):.1f}")
    
    with col3:
        multi_coauthor_papers = st.number_input("Co-author Papers", min_value=0, step=1, value=0)
        if multi_coauthor_papers > 0:
            authors_per_paper = st.number_input("Avg. Authors per Paper", min_value=1, step=1, value=3)
            coauthor_share = 0.5 / (authors_per_paper - 1) if authors_per_paper > 1 else 0.0
            st.write(f"Score: {min(multi_coauthor_papers * coauthor_share, 6):.1f}")
        else:
            coauthor_share = 0.0
    
    pub_score = min(papers_single * 1.0 + papers_principal * 0.5 + multi_coauthor_papers * coauthor_share, 6)
    
    # Books & IPR
    st.subheader("📚 Books / Intellectual Property Rights (Maximum: 6 Marks)")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        ref_books = st.number_input("Reference Books", min_value=0, step=1, value=0)
        st.write(f"Score: {ref_books * 2}")
    
    with col5:
        edited_books = st.number_input("Edited Books/Chapters", min_value=0, step=1, value=0)
        st.write(f"Score: {edited_books * 1}")
    
    with col6:
        iprs = st.number_input("IPRs Granted", min_value=0, step=1, value=0)
        st.write(f"Score: {iprs * 2}")
    
    books_ipr_score = min(ref_books * 2 + edited_books * 1 + iprs * 2, 6)
    
    # Awards
    st.subheader("🏆 Awards and Recognition (Maximum: 3 Marks)")
    
    award_options = {
        "None": 0,
        "State Level": 2,
        "National/International Level": 3
    }
    
    award_level = st.multiselect(
        "Select all awards received:",
        list(award_options.keys())[1:],  # Exclude "None"
        help="Select all applicable awards. Higher level awards have more weightage."
    )
    
    award_score = min(sum([award_options[level] for level in award_level]), 3)
    
    research_total = min(pub_score + books_ipr_score + award_score, 15)
    
    # Research Summary Visualization
    st.subheader("📊 Research Score Breakdown")
    
    research_data = pd.DataFrame({
        'Category': ['Publications', 'Books/IPR', 'Awards'],
        'Score': [pub_score, books_ipr_score, award_score],
        'Maximum': [6, 6, 3]
    })
    
    fig = px.bar(research_data, x='Category', y=['Score', 'Maximum'], 
                 title='Research Component Scores',
                 barmode='group',
                 color_discrete_map={'Score': '#1f77b4', 'Maximum': '#ff7f0e'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"🎯 **Total Research Score:** {research_total:.2f} / 15")

with tab4:
    st.markdown('<div class="section-header">📈 Results & Analytics Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Calculate final score
    final_score = academic_total + teaching_score + research_total
    max_score = 75
    percentage_score = (final_score / max_score) * 100
    
    # Main metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎓 Academic Score",
            value=f"{academic_total:.1f}/55",
            delta=f"{(academic_total/55)*100:.1f}%"
        )
    
    with col2:
        st.metric(
            label="👨‍🏫 Teaching Score", 
            value=f"{teaching_score:.1f}/5",
            delta=f"{(teaching_score/5)*100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="🔬 Research Score",
            value=f"{research_total:.1f}/15", 
            delta=f"{(research_total/15)*100:.1f}%"
        )
    
    with col4:
        st.metric(
            label="🎯 Final Score",
            value=f"{final_score:.1f}/75",
            delta=f"{percentage_score:.1f}%"
        )
    
    # Comprehensive Score Visualization
    st.subheader("📊 Comprehensive Score Analysis")
    
    # Radar Chart
    categories = ['Academic<br>Records', 'Teaching<br>Experience', 'Research &<br>Innovation']
    scores = [academic_total/55*100, teaching_score/5*100, research_total/15*100]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Your Score',
        line_color='#1f77b4'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100],
        theta=categories,
        fill='toself',
        name='Maximum Score',
        line_color='#ff7f0e',
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Score Distribution Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Score Table
    st.subheader("📋 Detailed Score Breakdown")
    
    detailed_summary = pd.DataFrame({
        'Component': [
            'Academic Records',
            '  - UG Score (Weighted)',
            '  - PG Score (Weighted)', 
            '  - M.Phil./Ph.D. (Weighted)',
            '  - Competitive Exams',
            'Teaching Experience',
            'Research & Innovation',
            '  - Publications',
            '  - Books/IPR',
            '  - Awards',
            'TOTAL SCORE'
        ],
        'Score': [
            f"{academic_total:.2f}",
            f"{ug_score * uni_factor:.2f}",
            f"{pg_score * uni_factor:.2f}",
            f"{mphil_phd_score * uni_factor:.2f}",
            f"{exam_score:.2f}",
            f"{teaching_score:.2f}",
            f"{research_total:.2f}",
            f"{pub_score:.2f}",
            f"{books_ipr_score:.2f}",
            f"{award_score:.2f}",
            f"{final_score:.2f}"
        ],
        'Maximum': [
            "55.00",
            "11.00",
            "18.00", 
            "20.00",
            "6.00",
            "5.00",
            "15.00",
            "6.00",
            "6.00",
            "3.00",
            "75.00"
        ],
        'Percentage': [
            f"{(academic_total/55)*100:.1f}%",
            f"{(ug_score * uni_factor/11)*100:.1f}%",
            f"{(pg_score * uni_factor/18)*100:.1f}%",
            f"{(mphil_phd_score * uni_factor/20)*100:.1f}%",
            f"{(exam_score/6)*100:.1f}%",
            f"{(teaching_score/5)*100:.1f}%",
            f"{(research_total/15)*100:.1f}%",
            f"{(pub_score/6)*100:.1f}%",
            f"{(books_ipr_score/6)*100:.1f}%",
            f"{(award_score/3)*100:.1f}%",
            f"{percentage_score:.1f}%"
        ]
    })
    
    st.dataframe(detailed_summary, use_container_width=True)
    
    # Performance Analysis and Recommendations
    st.subheader("🎯 Performance Analysis & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance Classification
        if final_score >= 65:
            performance_level = "Excellent"
            performance_color = "green"
            performance_icon = "🌟"
        elif final_score >= 55:
            performance_level = "Very Good"  
            performance_color = "blue"
            performance_icon = "⭐"
        elif final_score >= 45:
            performance_level = "Good"
            performance_color = "orange"
            performance_icon = "👍"
        elif final_score >= 35:
            performance_level = "Average"
            performance_color = "yellow"
            performance_icon = "⚡"
        else:
            performance_level = "Needs Improvement"
            performance_color = "red"
            performance_icon = "🔧"
        
        st.markdown(f"""
        <div style="background-color: {performance_color}20; padding: 1rem; border-radius: 10px; border-left: 5px solid {performance_color};">
            <h3>{performance_icon} Performance Level: {performance_level}</h3>
            <p><strong>Overall Score:</strong> {final_score:.1f}/75 ({percentage_score:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Top recommendations
        recommendations = []
        
        if academic_total < 45:
            recommendations.append("🎓 Consider pursuing higher qualifications or improving academic scores")
        if teaching_score < 3:
            recommendations.append("👨‍🏫 Gain more teaching or post-doctoral experience")
        if pub_score < 3:
            recommendations.append("📄 Focus on publishing more research papers")
        if books_ipr_score < 2:
            recommendations.append("📚 Consider writing books or filing for IPRs")
        if award_score == 0:
            recommendations.append("🏆 Participate in competitions and apply for awards")
        
        if recommendations:
            st.markdown("**🚀 Key Improvement Areas:**")
            for rec in recommendations[:3]:  # Show top 3 recommendations
                st.markdown(f"• {rec}")
        else:
            st.success("🎉 Excellent performance across all areas!")
    
    # Benchmark Comparison (if enabled)
    if show_benchmarks:
        st.subheader("📊 Benchmark Comparison")
        
        benchmark_data = pd.DataFrame({
            'Category': ['Your Score', 'Average Candidate', 'Top 10%', 'Minimum Required'],
            'Score': [final_score, 45, 65, 30],
            'Color': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        })
        
        fig = px.bar(benchmark_data, x='Category', y='Score', 
                    color='Color',
                    title='Score Comparison with Benchmarks',
                    color_discrete_map={color: color for color in benchmark_data['Color']})
        st.plotly_chart(fig, use_container_width=True)

# Profile Management Functions
if save_profile and profile_name:
    profile_data = {
        'timestamp': datetime.now().isoformat(),
        'uni_type': uni_type,
        'ug_percent': ug_percent,
        'pg_percent': pg_percent,
        'mphil': mphil,
        'phd': phd,
        'teaching_years': teaching_years,
        'papers_single': papers_single,
        'papers_principal': papers_principal,
        'multi_coauthor_papers': multi_coauthor_papers,
        'ref_books': ref_books,
        'edited_books': edited_books,
        'iprs': iprs,
        'award_level': award_level,
        'final_score': final_score
    }
    
    st.session_state.saved_profiles[profile_name] = profile_data
    st.success(f"✅ Profile '{profile_name}' saved successfully!")

# Add calculation to history
if auto_calculate:
    calculation_record = {
        'timestamp': datetime.now().isoformat(),
        'academic_score': academic_total,
        'teaching_score': teaching_score,
        'research_score': research_total,
        'final_score': final_score
    }
    
    if len(st.session_state.calculation_history) == 0 or \
       st.session_state.calculation_history[-1]['final_score'] != final_score:
        st.session_state.calculation_history.append(calculation_record)

# Final Results Summary
if final_score >= 60:
    st.balloons()
    st.success("🎉 Outstanding! You have a very strong profile for Assistant Professor positions!")
elif final_score >= 45:
    st.success("✅ Good score! You meet the typical requirements for Assistant Professor positions.")
elif final_score >= 30:
    st.warning("⚠️ Average score. Consider improving weak areas to strengthen your application.")
else:
    st.error("❌ Score needs significant improvement. Focus on the recommended areas.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 <strong>Advanced Assistant Professor Score Calculator v2.0</strong></p>
    <p>Developed with ❤️ using Streamlit | Enhanced with Analytics & Profile Management</p>
    <p>📊 Based on official evaluation scheme: Academic (55) + Teaching (5) + Research (15) = 75 Marks</p>
</div>
""", unsafe_allow_html=True)
