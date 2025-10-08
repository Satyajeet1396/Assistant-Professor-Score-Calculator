import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import re
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from io import BytesIO
from functools import lru_cache
from tqdm import tqdm
import qrcode
import base64
import openpyxl
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Assistant Professor Score Calculator", layout="wide")

st.title("🎓 Assistant Professor Eligibility Score Calculator")
st.write("Compute your academic, teaching, and research score based on official evaluation criteria.")

# =========================================================
# ENHANCED APP LINK CONTAINER
# =========================================================
with st.expander("ℹ️ Click here to learn about this Assistant Professor Score Calculator app", expanded=False):
    st.markdown("""
        <style>
        .app-info {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 10px 0;
        }
        .app-info h3 {
            color: #0066cc;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .app-info ul, .app-info ol {
            margin-bottom: 20px;
        }
        </style>
<h2> Assistant Professor Eligibility Score Calculator helps candidates compute their academic, teaching, 
        and research scores based on official evaluation criteria. <h2>

<h2> 🎯 Key Features: </h2> 
        - Calculates weighted scores for Academic Records (UG, PG, M.Phil., Ph.D., NET/SET/JRF)
        - Computes Teaching/Postdoc experience scores
        - Evaluates Research Aptitude & Innovation (Publications, Books/IPRs, Awards)
        - Provides a detailed summary table and final weighted score
        - Gives feedback based on score

<h2> 🚀 How to Use: </h2> 
        1. Fill in your academic details in Section A.
        2. Enter your teaching or postdoctoral experience in Section B.
        3. Add research contributions in Section C.
        4. Review the final score and summary.
    """, unsafe_allow_html=True)

# =========================================================
# SECTION A: Academic Records
# =========================================================
st.header("A. Academic Records (Max: 55 Marks)")

# --- University Type Weighting ---
uni_type = st.selectbox(
    "Select the Type of Degree Awarding University",
    [
        "Institutes of National Importance / Top 200 QS/THE/ARWU",
        "Central/State University with NIRF <100 or Foreign (QS/THE/ARWU 200–500)",
        "Other Central/State Public Universities",
        "Other UGC Approved Universities"
    ]
)
if uni_type == "Institutes of National Importance / Top 200 QS/THE/ARWU":
    uni_factor = 1.0
elif uni_type == "Central/State University with NIRF <100 or Foreign (QS/THE/ARWU 200–500)":
    uni_factor = 0.9
elif uni_type == "Other Central/State Public Universities":
    uni_factor = 0.8
else:
    uni_factor = 0.6

# --- UG Percentage ---
ug_percent = st.number_input("UG Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
if ug_percent >= 80:
    ug_score = 11
elif ug_percent >= 60:
    ug_score = 9
elif ug_percent >= 55:
    ug_score = 7
elif ug_percent >= 45:
    ug_score = 4
else:
    ug_score = 0

# --- PG Percentage ---
pg_percent = st.number_input("PG Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
if pg_percent >= 80:
    pg_score = 18
elif pg_percent >= 60:
    pg_score = 16
elif pg_percent >= 55:
    pg_score = 14
else:
    pg_score = 0

# --- M.Phil. and Ph.D. ---
mphil = st.checkbox("Have M.Phil. Degree?")
phd = st.checkbox("Have Ph.D. Degree?")

mphil_score = 0
phd_score = 0
if mphil:
    mphil_percent = st.number_input("Enter M.Phil. Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
    if mphil_percent >= 60:
        mphil_score = 5
    elif mphil_percent >= 55:
        mphil_score = 3

if phd:
    phd_score = 20

mphil_phd_score = min(mphil_score + phd_score, 20)

# --- JRF/NET/SET Multiple Selection ---
st.subheader("Select all that apply for NET with JRF/NET/SET Qualification")
exam_list = st.multiselect("Choose Qualification(s):", ["NET with JRF", "NET", "SET"])
exam_score = 0
if "JRF" in exam_list:
    exam_score += 6
elif "NET" in exam_list:
    exam_score += 4
elif "SET" in exam_list:
    exam_score += 3
exam_score = min(exam_score, 6)

# Apply university weighting to UG, PG, MPhil, PhD (NOT to JRF/NET/SET)
academic_total = min(((ug_score + pg_score + mphil_phd_score) * uni_factor) + exam_score, 55)

st.success(f"Academic Record Score: {academic_total:.2f} / 55")

# =========================================================
# SECTION B: Teaching Experience
# =========================================================
st.header("B. Teaching / Post-Doctoral Experience (Max: 5 Marks)")
teaching_years = st.number_input("Total Approved Teaching/Postdoc Experience (Years)", min_value=0.0, step=0.1)
teaching_score = min(teaching_years * 1.0, 5.0)
st.success(f"Teaching Experience Score: {teaching_score:.2f} / 5")

# =========================================================
# SECTION C: Research Aptitude & Innovation
# =========================================================
st.header("C. Research Aptitude and Innovation Skills (Max: 15 Marks)")

# a. Research Publications
st.subheader("a. Research Publications (Max: 6 Marks)")
st.caption("Only Indexed Journal papers (SciFinder, Web of Science, Scopus) are counted.")

papers_single = st.number_input("Number of Single-author Indexed Papers", min_value=0, step=1)
papers_principal = st.number_input("Number of Multi-author Papers (You as Principal/Corresponding Author)", min_value=0, step=1)
multi_coauthor_papers = st.number_input("Number of Multi-author Papers (You as Co-author)", min_value=0, step=1)
authors_per_paper = st.number_input("Average Total Authors per Multi-author Paper (for Co-author papers)", min_value=1, step=1, value=3)

# Multi-author logic
if authors_per_paper > 1:
    coauthor_share = 0.5 / (authors_per_paper - 1)
else:
    coauthor_share = 0.0

pub_score = (
    papers_single * 1.0
    + papers_principal * 0.5
    + multi_coauthor_papers * coauthor_share
)
pub_score = min(pub_score, 6)

# b. Books / IPR
st.subheader("b. Books / IPR (Max: 6 Marks)")
ref_books = st.number_input("Authored Reference Books (Reputed Publisher, ISBN)", min_value=0, step=1)
edited_books = st.number_input("Edited Books / Chapters / Translated Books", min_value=0, step=1)
iprs = st.number_input("IPRs Granted (Patent / Copyright / Trademark / Design)", min_value=0, step=1)
books_ipr_score = ref_books * 2 + edited_books * 1 + iprs * 2
books_ipr_score = min(books_ipr_score, 6)

# c. Awards
st.subheader("c. Awards (Max: 3 Marks)")
award_level = st.multiselect(
    "Select Highest Level of Award Received:", 
    ["None", "State Level", "National/International Level"]
)

award_points = {"None": 0, "State Level": 2, "National/International Level": 3}

# Sum points for all selected awards
award_score = sum([award_points[level] for level in award_level])
# Cap at 3 (maximum for awards)
award_score = min(award_score, 3)

research_total = min(pub_score + books_ipr_score + award_score, 15)
st.success(f"Research Aptitude & Innovation Score: {research_total:.2f} / 15")

# =========================================================
# FINAL CALCULATION & SUMMARY
# =========================================================
st.header("Final Evaluation Summary")

final_score = academic_total + teaching_score + research_total
max_score = 55 + 5 + 15

st.metric("Total Weighted Score", f"{final_score:.2f} / {max_score}")

# Detailed Summary Table
st.subheader("📊 Score Summary")
summary = {
    "Academic Record (A)": f"{academic_total:.2f} / 55",
    "Teaching Experience (B)": f"{teaching_score:.2f} / 5",
    "Research Aptitude & Innovation (C)": f"{research_total:.2f} / 15",
    "Final Weighted Total": f"{final_score:.2f} / {max_score}"
}
st.table(summary)

# Feedback
if final_score >= 60:
    st.balloons()
    st.success("Excellent! You have a strong academic and research profile for Assistant Professor selection.")
else:
    st.warning("Consider improving your publications, experience, or qualifications to strengthen your profile.")

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | Based on official Assistant Professor evaluation scheme (Academic 55 + Teaching 5 + Research 15 = 75 Marks)")

st.divider()

# Footer and support section
col1, col2 = st.columns([2, 1])
with col1:
    st.info("Created by Dr. Satyajeet Patil")
    st.info("For more research tools visit: https://patilsatyajeet.wixsite.com/home/python")
with col2:
    st.metric("Enhanced Features", "5+", delta="New in this version")

# Support section in expander
with st.expander("🤝 Support Our Research", expanded=False):
    st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin: 1rem 0;'>
            <h3>🙏 Your Support Makes a Difference!</h3>
            <p>Your contribution helps us continue developing free tools for the research community.</p>
            <p>Every donation, no matter how small, fuels our research journey!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Two columns for QR code and Buy Me a Coffee button
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### UPI Payment")
        # Generate UPI QR code
        upi_url = "upi://pay?pa=satyajeet1396@oksbi&pn=Satyajeet Patil&cu=INR"
        qr = qrcode.make(upi_url)
        
        # Save QR code to BytesIO
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Display QR code with message
        st.markdown("Scan to pay: **satyajeet1396@oksbi**")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{qr_base64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("#### Buy Me a Coffee")
        st.markdown("Support through Buy Me a Coffee platform:")
        # Buy Me a Coffee button
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
                    <img src="https://img.buymeacoffee.com/button-api/?text=Support our Research&emoji=&slug=researcher13&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Support our Research"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.info("🚀 A small donation from you can fuel our research journey, turning ideas into breakthroughs that can change lives!")
