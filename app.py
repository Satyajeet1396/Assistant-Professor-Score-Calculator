import streamlit as st
import pandas as pd

st.set_page_config(page_title="API Score Calculator", page_icon="🎓", layout="centered")

st.title("🎓 Academic Performance Indicator (API) Score Calculator")

st.markdown("### 🧾 Step 1: Basic Information")
name = st.text_input("Full Name")
designation = st.text_input("Designation")
institute = st.text_input("Institute/University")

st.markdown("---")
st.markdown("### 🎯 Step 2: Degree Information")

degree = st.selectbox("Select Highest Degree", ["Ph.D.", "M.Phil.", "PG with NET/JRF/SET"])
university_type = st.selectbox(
    "Select the Type of Degree Awarding University",
    ["Central/State University", "Deemed/Private University", "Foreign University"]
)

# Marks based on university type
univ_marks = {
    "Central/State University": 20,
    "Deemed/Private University": 15,
    "Foreign University": 25
}
degree_score = univ_marks.get(university_type, 0)

st.success(f"✅ Degree Score: {degree_score} marks")

st.markdown("---")
st.markdown("### 🧠 Step 3: JRF / NET / SET Qualification")

qualifications = st.multiselect(
    "Select all that apply",
    ["NET", "NET with JRF", "SET"],
    help="Select multiple if applicable"
)

# Each qualification gives full marks (no weighting by university)
qualification_scores = {
    "NET": 10,
    "NET with JRF": 12,
    "SET": 8
}
qualification_score = sum(qualification_scores[q] for q in qualifications)
st.success(f"✅ Qualification Score: {qualification_score} marks")

st.markdown("---")
st.markdown("### 🧪 Step 4: Research Publications (Indexed Journals Only)")

st.info(
    "Only publications indexed in **SciFinder, Web of Science, or Scopus** will be counted.\n\n"
    "- Single-author paper: 1 mark per paper.\n"
    "- Multi-author paper: First/Corresponding author gets 50%, rest 50% distributed among co-authors."
)

single_author = st.number_input("Number of Single-author Papers", min_value=0, step=1)
multi_author = st.number_input("Number of Multi-author Papers (You as Co-author)", min_value=0, step=1)
avg_authors = st.number_input("Average Number of Authors per Multi-author Paper", min_value=2, step=1, help="Enter average total number of authors per paper")

# Calculation logic
if avg_authors > 1:
    multi_author_score = multi_author * (0.5 / (avg_authors - 1))
else:
    multi_author_score = 0

research_score = single_author * 1 + multi_author_score
st.success(f"✅ Research Publication Score: {research_score:.2f} marks")

st.markdown("---")
st.markdown("### 🏅 Step 5: Awards & Recognition")

awards = st.multiselect(
    "Select all applicable awards",
    ["State Level", "National Level", "International Level"],
    help="You can select multiple awards"
)
award_scores = {
    "State Level": 5,
    "National Level": 10,
    "International Level": 15
}
award_score = sum(award_scores[a] for a in awards)
st.success(f"✅ Award Score: {award_score} marks")

st.markdown("---")
st.markdown("### 📊 Final Summary")

total_score = degree_score + qualification_score + research_score + award_score

summary_data = {
    "Degree Type": degree,
    "University Type": university_type,
    "Degree Score": degree_score,
    "JRF/NET/SET Score": qualification_score,
    "Research Publications Score": round(research_score, 2),
    "Awards Score": award_score,
    "Total Score": round(total_score, 2)
}

summary_df = pd.DataFrame([summary_data])
st.table(summary_df)

st.markdown(f"## 🧮 Final API Score: **{total_score:.2f} marks** 🎉")

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit")
