# 🧠 InsightGenie 2.0 — Your AI-Powered Data Analyst

[![HuggingFace Space](https://img.shields.io/badge/Live%20Demo-HuggingFace-blue?logo=streamlit)](https://huggingface.co/spaces/whisplnspace/InsightGenie2.0)
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Together AI](https://img.shields.io/badge/Powered%20by-Together.ai-800080?logo=OpenAI)](https://together.ai/)

> Upload Files → Ask Questions → Get Insights, Answers & Visuals — Instantly!

---

## 🔗 Live App

👉 **[Try InsightGenie on Hugging Face Spaces →](https://huggingface.co/spaces/whisplnspace/InsightGenie2.0)**

---

## 🎯 What is InsightGenie?

**InsightGenie** is an intuitive AI analyst built with Streamlit that helps you:
- Upload and parse documents (text, spreadsheets, PDFs, images)
- Ask data-related questions
- Get clear LLM-powered answers
- Generate smart, customizable charts
- Export answers and plots in one click

---

## 💡 Features

✅ Upload: `.csv`, `.xlsx`, `.txt`, `.docx`, `.pdf`, `.png`, `.jpg`, `.jpeg`  
🧠 LLM-Powered Answers (Together.ai, LLaMA 4)  
📊 Bar, Line, Scatter, and Pie Chart Generation  
🧼 Filters, Describe Summary, Download CSV/Text/Plots  
📝 Chat History & Re-runs  
🌈 Aesthetic UI with modern theme and icons  

---

## 🖼️ Demo Screenshot

![Image](https://github.com/user-attachments/assets/0c1615bc-4ceb-4966-85c9-eb23b582866d)

---

## 🧪 Tech Stack

| Tech | Role |
|------|------|
| **Streamlit** | UI and interaction |
| **Together.ai API** | LLM querying |
| **pandas, seaborn, matplotlib** | Data analysis & visualizations |
| **PyMuPDF, pytesseract, docx, PIL** | Document & image processing |

---

## 🛠️ Installation

### ✅ Local Setup

```bash
git clone https://github.com/your-username/InsightGenie.git
cd InsightGenie

# (Optional) Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add Together.ai API Key
echo "TOGETHER_API_KEY=your_together_api_key_here" > .env

# Run the app
streamlit run app.py
````

---

### 🚀 Deploy on Hugging Face (Recommended)

> You can deploy InsightGenie to Hugging Face in under 2 minutes!

1. Go to: [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **“Create New Space”**
3. Choose **Streamlit** as SDK
4. Clone or upload this repo
5. In the **“Files” tab**, add `requirements.txt`, `app.py`, and `.env` (set `TOGETHER_API_KEY`)
6. Done! Your app is live.

---

## 📦 Requirements

```txt
streamlit
pandas
python-docx
PyMuPDF
pytesseract
Pillow
matplotlib
seaborn
python-dotenv
together
```

---

## 🤖 LLM Model

Using the powerful:

```
meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8
```

via [Together.ai](https://together.ai/) — for intelligent answers, summaries, and insights.

---

## 🙌 Contribution

Contributions, issues, and stars are always welcome!
Open a PR or start a discussion in the Issues tab.

---


## 🌟 Author

Built with ❤️ by [@whisplnspace](https://huggingface.co/whisplnspace)
Feel free to connect or fork the project for your use.
