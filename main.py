import os
import base64
import io
import pandas as pd
import docx
import fitz
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dotenv import load_dotenv
from together import Together

# Load environment and API key
load_dotenv()
together_api_key = os.getenv("TOGETHER_API_KEY")
MODEL = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
together = Together(api_key=together_api_key)

def extract_text(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext == ".txt":
        return file.read().decode("utf-8"), None
    elif ext == ".docx":
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs]), None
    elif ext == ".csv":
        df = pd.read_csv(file)
        return df.to_csv(index=False), df
    elif ext == ".xlsx":
        df = pd.read_excel(file)
        return df.to_csv(index=False), df
    elif ext == ".pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc]), None
    elif ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file)
        return pytesseract.image_to_string(image), None
    else:
        raise ValueError("Unsupported file type")

def query_llm(prompt):
    try:
        response = together.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"TogetherAI Error: {e}"

def get_download_link(content, filename, filetype):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/{filetype};base64,{b64}" download="{filename}">📥 Download {filetype.upper()}</a>'

def get_image_download_link(fig, filename="plot.png"):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return f'<a href="data:file/png;base64,{b64}" download="{filename}">📥 Download Plot</a>'

def main():
    st.set_page_config(page_title="InsightGenie | AI Data Analyst", page_icon="🧠", layout="wide")
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f8fa;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #114B5F;
            margin-bottom: 5px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            margin-bottom: 25px;
        }
        .stButton>button {
            background-color: #114B5F;
            color: white;
            font-weight: 600;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #0d3a47;
            color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="title">🧠 InsightGenie</div>
        <div class="subtitle">Smart Data Upload → Instant Analysis → Insightful Visuals</div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("📂 Upload & Ask")
        uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "txt", "docx", "pdf", "png", "jpg", "jpeg"])
        question = st.text_area("Ask a question", height=120)
        submit = st.button("🔍 Analyze")
        st.markdown("---")
        if st.session_state.history:
            st.subheader("📝 History")
            for i, qa in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**Q{i}:** {qa['question']}")
                st.markdown(f"**A{i}:** {qa['answer']}")
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.experimental_rerun()

    if uploaded_file:
        try:
            raw_text, df = extract_text(uploaded_file)
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            if df is not None:
                st.markdown("### 🔍 Data Preview")
                st.dataframe(df.head(10))
                st.markdown(get_download_link(df.to_csv(index=False), "data.csv", "csv"), unsafe_allow_html=True)
            else:
                st.markdown("### 🔍 Text Extract Preview")
                st.text(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)
        except Exception as e:
            st.error(f"Error: {e}")
            return
    else:
        raw_text, df = None, None

    if submit:
        if not uploaded_file:
            st.warning("Please upload a file first.")
            return
        if not question:
            st.warning("Please type a question.")
            return
        with st.spinner("🤖 Thinking..."):
            try:
                prompt = f"You are a helpful data analyst. Here's the data: {raw_text}\n\nNow answer this question: {question}"
                answer = query_llm(prompt)
                st.markdown("## 💡 Answer")
                st.markdown(answer)
                st.markdown(get_download_link(answer, "answer.txt", "txt"), unsafe_allow_html=True)
                st.session_state.history.append({"question": question, "answer": answer})
            except Exception as e:
                st.error(f"LLM Error: {e}")

    if df is not None:
        st.markdown("---")
        st.subheader("📊 Visualize Your Data")

        with st.expander("Show summary and filters"):
            st.write(df.describe(include='all').T)
            filter_col = st.selectbox("Filter by column", [None] + list(df.columns), index=0)
            filtered_df = df
            if filter_col:
                selected_vals = st.multiselect(f"Select values for {filter_col}", options=df[filter_col].dropna().unique())
                if selected_vals:
                    filtered_df = df[df[filter_col].isin(selected_vals)]
            st.dataframe(filtered_df.head(10))

        col1, col2, col3, col4 = st.columns([3, 3, 3, 2])
        with col1:
            x_col = st.selectbox("X-Axis", filtered_df.columns)
        with col2:
            y_col = st.selectbox("Y-Axis", filtered_df.columns)
        with col3:
            chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Pie"])
        with col4:
            size = st.slider("Plot Size", 5, 15, 8)

        if st.button("📈 Generate Plot"):
            try:
                fig, ax = plt.subplots(figsize=(size, size * 0.6))
                sns.set(style="whitegrid")
                if chart_type == "Bar":
                    sns.barplot(data=filtered_df, x=x_col, y=y_col, ax=ax)
                elif chart_type == "Line":
                    sns.lineplot(data=filtered_df, x=x_col, y=y_col, ax=ax)
                elif chart_type == "Scatter":
                    sns.scatterplot(data=filtered_df, x=x_col, y=y_col, ax=ax)
                elif chart_type == "Pie":
                    ax.clear()
                    grouped = filtered_df.groupby(x_col)[y_col].sum()
                    ax.pie(grouped, labels=grouped.index, autopct="%1.1f%%")
                    ax.axis("equal")
                st.pyplot(fig)
                st.markdown(get_image_download_link(fig), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Plot Error: {e}")

if __name__ == "__main__":
    main()
