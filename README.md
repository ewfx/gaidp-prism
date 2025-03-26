# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#-introduction)
- [Demo](#-demo)
- [Inspiration](#-inspiration)
- [Architecture Diagram](#-architecture-diagram)
- [What It Does](#-what-it-does)
- [How We Built It](#-how-we-built-it)
- [Challenges We Faced](#-challenges-we-faced)
- [How to Run](#-how-to-run)
- [Tech Stack](#-tech-stack)
- [Team](#-team)

---

## 🎯 Introduction
We have developed an **intelligent Data Profiling Agent** that automates **data validation** in the banking sector, ensuring compliance with regulatory standards set by organizations like the **Federal Reserve**. Our solution efficiently processes large datasets, identifying regulatory violations, assessing **risk scores**, detecting **anomalies**, and providing **record-specific remediation actions**. This streamlines compliance, enhances data integrity, and mitigates financial risks for banks.

## 🎥 Demo
🔗 **[Live Demo](#)** *(if applicable)*  
📹 **[Video Demo](#)** *(if applicable)*  
🖼️ **Screenshots:**  
![Screenshot 1](link-to-image)

## 💡 Inspiration
Traditional data validation is a manual, time-consuming process requiring expert knowledge. Investigating validation failures is equally challenging. Given **Generative AI’s** capabilities in handling complex tasks, we leveraged **GenAI** to automate and streamline the validation process, significantly reducing effort and enhancing accuracy.

## 📊 Architecture Diagram
*(Add your architecture diagram here)*

## ⚙️ What It Does
Our application offers the following functionalities:

✅ **Interprets** data validation rules from **Federal Reserve documents** and auto-generates validation scripts.  
✅ **Allows customization** of rules via an **interactive chat interface**.  
✅ **Acts as a Subject Matter Expert (SME)** in **banking regulations**, particularly **Corporate Loan Regulations**, assisting users in clarifying doubts.  
✅ **Performs risk scoring** and **anomaly detection** for deeper insights into customer patterns.  
✅ **Generates detailed reports** on findings and **suggests remediation actions**.  
✅ **Supports PDF report generation** for single records or complete datasets.  
✅ **Ensures responsible AI use** by preventing misuse of GenAI capabilities.

## 🛠️ How We Built It
Our application integrates the following technologies:

🔹 **PDF Processing**: `pdfplumber`, `tabula`, `reportlab` for **data extraction & conversion**.  
🔹 **Data Processing**: `pandas`, `numpy` for **efficient dataframe operations**.  
🔹 **LLM Model**: `Gemini 1.5 Pro` for **content & script generation**.  
🔹 **Prompt Engineering**: Optimized LLM prompts for **accurate script generation & remediation suggestions**.  
🔹 **Anomaly Detection**: `Isolation Forest` for **pattern & anomaly detection**.  
🔹 **UI Framework**: `Streamlit` for **a seamless user experience**.

## 🚧 Challenges We Faced
🔹 **Extracting accurate validation rules** from **bulky Federal Reserve documents** was complex.  
🔹 **Testing limitations** due to API **rate limits & usage constraints** made recursive testing challenging.

## 🏃 How to Run
1️⃣ **Clone the repository**  
```sh
   git clone https://github.com/your-repo.git
```
2️⃣ **Install dependencies**  
```sh
   pip install -r requirements.txt
```
3️⃣ **Run the project**  
Navigate to the `src` folder and run:  
```sh
   streamlit run app.py
```

## 🏗️ Tech Stack
- 🖥️ **Frontend**: `Streamlit`
- 🔧 **Backend**: `Python`
- 📊 **Database**: CSV/Excel files, Text files
- 🤖 **LLM**: `Google Gemini 1.5 Pro`

## 👥 Team
- **Dishita Mohan** - [GitHub](https://github.com/dishitamohan) | [LinkedIn](#)
- **Krithika Ramachandran** - [GitHub](https://github.com/kritatgit) | [LinkedIn](https://www.linkedin.com/in/krithika-ramachandran-42a1471b1)
- **Ronan Lobo**

---

This README now features **better formatting**, **working navigation links**, and **improved readability**. 🚀 Let me know if you'd like further modifications! 🎯

