import streamlit as st

st.set_page_config(page_title="Assistant Professor Score Calculator", layout="wide")

st.title("🎓 Assistant Professor Eligibility Score Calculator")
st.write("Calculate your academic, teaching, and research score based on the official evaluation criteria.")

# -------------------------
# SECTION A: Academic Records
# -------------------------
st.header("A. Academic Records (Max: 55 Marks)")

# University Type (Weightage factor)
uni_type = st.selectbox(
    "Select the Type of Degree Awarding University",
    [
        "Institutes of National Importance / Top 200 QS/THE/ARWU",
        "Central/State University with NIRF <100 or Foreign (QS/THE/ARWU 200-500)",
        "Other Central/State Public Universities",
        "Other UGC Approved Universities"
    ]
)
if uni_type == "Institutes of National Importance / Top 200 QS/THE/ARWU":
    uni_factor = 1.0
elif uni_type == "Central/State University with NIRF <100 or Foreign (QS/THE/ARWU 200-500)":
    uni_factor = 0.9
elif uni_type == "Other Central/State Public Universities":
    uni_factor = 0.8
else:
    uni_factor = 0.6

# --- UG Percentage
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

# --- PG Percentage
pg_percent = st.number_input("PG Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
if pg_percent >= 80:
    pg_score = 18
elif pg_percent >= 60:
    pg_score = 16
elif pg_percent >= 55:
    pg_score = 14
else:
    pg_score = 0

# --- M.Phil. and Ph.D.
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

# --- NET/JRF/SET
exam_type = st.selectbox("Select JRF/NET/SET Qualification", ["None", "SET", "NET", "NET with JRF"])
exam_score = {"None": 0, "SET": 3, "NET": 4, "NET with JRF": 6}[exam_type]

academic_total = (ug_score + pg_score + mphil_phd_score + exam_score) * uni_factor
academic_total = min(academic_total, 55)

st.success(f"Academic Record Score: {academic_total:.2f} / 55")

# -------------------------
# SECTION B: Teaching Experience
# -------------------------
st.header("B. Teaching / Post-Doctoral Experience (Max: 5 Marks)")
teaching_years = st.number_input("Total Approved Teaching/Postdoc Experience (Years)", min_value=0.0, step=0.1)
teaching_score = min(teaching_years * 1.0, 5.0)
st.success(f"Teaching Experience Score: {teaching_score:.2f} / 5")

# -------------------------
# SECTION C: Research Aptitude & Innovation
# -------------------------
st.header("C. Research Aptitude and Innovation Skills (Max: 15 Marks)")

# a. Research Publications
st.subheader("a. Research Publications (Max: 6 Marks)")
papers_single = st.number_input("Number of Single-author Indexed Papers", min_value=0, step=1)
papers_principal = st.number_input("Number of Multi-author Papers (You as Principal Author)", min_value=0, step=1)
papers_coauthor = st.number_input("Number of Multi-author Papers (You as Co-author)", min_value=0, step=1)

pub_score = papers_single * 1 + papers_principal * 0.5 + papers_coauthor * 0.25
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
award_level = st.selectbox(
    "Select Highest Level of Award Received",
    ["None", "State Level", "National/International Level"]
)
award_score = {"None": 0, "State Level": 2, "National/International Level": 3}[award_level]

research_total = min(pub_score + books_ipr_score + award_score, 15)
st.success(f"Research Aptitude & Innovation Score: {research_total:.2f} / 15")

# -------------------------
# FINAL CALCULATION
# -------------------------
st.header("Final Evaluation")

final_score = academic_total + teaching_score + research_total
max_score = 55 + 5 + 15
st.metric("Total Weighted Score", f"{final_score:.2f} / {max_score}")

if final_score >= 60:
    st.balloons()
    st.success("Excellent! You have a strong academic profile for Assistant Professor selection.")
else:
    st.warning("You can improve your score by enhancing publications or qualifications.")

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | Logic based on official evaluation scheme (Academic 55 + Teaching 5 + Research 15 = 75 Marks)")
