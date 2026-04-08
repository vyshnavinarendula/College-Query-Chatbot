# 🎓 College Query Chatbot

A Machine Learning–powered chatbot built with **Streamlit** and **scikit-learn** that answers common college-related questions using TF-IDF vectorization and Cosine Similarity.

---

## 📁 Project Structure

```
college_chatbot/
├── app.py               # Streamlit UI (main entry point)
├── chatbot_engine.py    # ML engine (TF-IDF + Cosine Similarity)
├── college_data.csv     # FAQ dataset (20 Q&A pairs across 10 categories)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🧠 How It Works

```
User Query
    │
    ▼
Text Cleaning  (lowercase, remove special chars)
    │
    ▼
TF-IDF Vectorizer  (converts text → numerical vectors)
    │
    ▼
Cosine Similarity  (compares query vector vs all FAQ vectors)
    │
    ▼
Best Match Retrieved  (highest similarity score)
    │
    ▼
Answer + Confidence % displayed
```

### Key ML concepts used:
| Concept | Description |
|---|---|
| **TF-IDF** | Term Frequency–Inverse Document Frequency – weighs rare words higher |
| **N-grams (1,2)** | Considers single words AND two-word phrases for better matching |
| **Cosine Similarity** | Measures the angle between two vectors (0 = unrelated, 1 = identical) |
| **Threshold (0.15)** | Minimum score; below this a fallback message is shown |

---

## 📚 Dataset

`college_data.csv` contains **20 FAQ pairs** across **10 categories**:

- Courses, Fees, Placements, Admissions
- Timings, Hostel, Sports, Contact
- Scholarships, Library, WiFi, Clubs
- Faculty, Labs, Location, Canteen
- Ranking, Loan, Attendance, Exams

To add more Q&A pairs, simply add rows to `college_data.csv` — no code changes needed!

---

## 🖥️ Features

- 💬 Chat-style UI with user/bot message bubbles
- ⚡ Confidence score badge (green/yellow/red)
- 🏷️ Category tag for each answer
- 📂 Sidebar topic browser (filter FAQs by category)
- ✨ Quick-question chips for common queries
- 🗑️ Clear chat button
- 📊 Live query counter

---

## 💡 Extending the Project

| Feature | How |
|---|---|
| Add more FAQs | Add rows to `college_data.csv` |
| Change similarity threshold | Edit `threshold=0.15` in `chatbot_engine.py` |
| Use deep learning | Replace TF-IDF with `sentence-transformers` embeddings |
| Add voice input | Use `streamlit-mic-recorder` library |
| Add login system | Use `streamlit-authenticator` library |
| Deploy online | Push to GitHub → deploy on **Streamlit Cloud** (free) |
