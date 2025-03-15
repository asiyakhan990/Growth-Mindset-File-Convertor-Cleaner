import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📁🧹File Convertor & Cleaner", layout="wide")
st.markdown(
        """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        /* Apply the font to the entire app */
        html, body, [class*="st-"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Background color */
        .stApp {
            background-color: #EFDECD; /* Brownish Almond Background */
        }

        /* Style the file uploader drag-and-drop box */
        div[data-testid="stFileUploader"] > div {
            background-color: #D2B48C !important; /* Tan/Almond shade */
            border: 2px dashed #8B5A2B !important; /* Darker brown border */
            padding: 10px;
            border-radius: 10px;
        }

        /* Improve text contrast inside the uploader */
        div[data-testid="stFileUploader"] * {
            color: #4B382A !important; /* Dark brown text */
        }

        /* Style headings */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #4B382A; /* Dark Brown */
            font-weight: 600;
        }

        /* Style buttons */
        .stButton button {
            background-color: #8B5A2B !important; /* Dark brown */
            color: white !important;
            font-size: 16px !important;
            border-radius: 8px !important;
        }

        /* Style success messages */
        .stAlert {
            background-color: #F4E1C1 !important; /* Soft Almond Tone */
            border-left: 6px solid #8B5A2B !important; /* Brown Accent */
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("📁🧹File Convertor & Cleaner")
st.write("Easily upload and process your CSV or Excel files. Clean your data, select specific columns, visualize insights, and convert formats—all in one place effortlessly!🚀")

files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"🔍 {file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing values filled successfully!")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            output.seek(0)
            st.download_button("⬇️ Downlaod File", file_name=new_name, data=output, mime=mime)
        st.success("Processing Completed! 🎉")