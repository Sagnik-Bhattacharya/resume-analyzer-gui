# 🧾 Resume Analyzer GUI

**Resume Analyzer GUI** is a professional desktop application built with **CustomTkinter** that analyzes resumes (PDF/DOCX), extracts skills, matches them against job requirements, and provides interactive visual insights including **multi-page PDF preview**, **skill highlighting**, and detailed scoring — all **offline and free**.

---

## 🚀 Features

✔ **Supports PDF & DOCX resumes**
✔ **Multi-page PDF preview with scroll or page mode**
✔ **Raw vs Parsed resume view toggle**
✔ **Light / Dark theme toggle**
✔ **Skill matching** against job requirements
✔ **Matched & missing skills as pill-shaped tags**
✔ **Match & similarity scores**
✔ **Local resume history** stored via MongoDB
✔ **Interactive UI** (hover effects, clean layouts)
✔ **Offline — no paid APIs required**

---

## 🎛 User Toggles

| Setting     | Options           |
| ----------- | ----------------- |
| UI Theme    | `light` / `dark`  |
| Resume View | `raw` / `parsed`  |
| PDF Mode    | `scroll` / `page` |

All settings persist via `settings.json`.

---

## 📸 Screenshots

**Upload Screen**
![Upload Screen](assets/upload_screen.png)

**Result Screen**
![Result Screen](assets/result_screen.png)

---

## 💻 Tech Stack

**Languages & Frameworks**

* Python 3.12+
* CustomTkinter (UI)
* PyMongo (local DB)

**Parsing / NLP**

* pdfplumber, python-docx
* scikit-learn (TF-IDF similarity)
* NLTK (skills preprocessing)

**Preview / Rendering**

* pdf2image + Pillow (PDF pages)

All dependencies are **free & open-source**.

---

## 🗂 Folder Structure

```
resume-analyzer-gui/
│
├── app/
│   ├── main.py                     # App entry point
│   ├── ui/                         # GUI layer
│   │   ├── app.py                  # Window + screen switching
│   │   ├── components/             # Sidebar, buttons, settings
│   │   │   ├── sidebar.py
│   │   │   └── settings_panel.py
│   │   ├── screens/                # Screen views
│   │   │   ├── upload_screen.py
│   │   │   ├── result_screen.py
│   │   │   └── history_screen.py
│   │   └── theme.py
│   ├── core/                       # Business logic
│   │   ├── analyzer.py
│   │   ├── matcher.py
│   │   └── scorer.py
│   ├── nlp/
│   │   ├── clean.py
│   │   ├── skills.py
│   │   └── similarity.py
│   ├── parsers/
│   │   ├── pdf.py
│   │   └── docx.py
│   ├── db/
│   │   ├── mongodb.py
│   │   ├── collections.py
│   │   └── indexes.py
│   ├── repositories/
│   │   └── resume_repo.py
│   ├── models/
│   │   └── resume.py
│   ├── services/
│   │   └── resume_service.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── file_utils.py
│   │   └── settings.py             # Persist UI settings
│   └── data/
│       └── skills.json             # Skill inventory
├── tests/
├── assets/
│   ├── upload_screen.png
│   └── result_screen.png
├── scripts/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚡ Installation

```bash
git clone https://github.com/Sagnik-Bhattacharya/resume-analyzer-gui.git
cd resume-analyzer-gui
```

### Create virtual environment

```bash
python -m venv venv
source venv/Scripts/activate   # Windows
# or
source venv/bin/activate       # Mac/Linux
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start local MongoDB (optional, for history)

```bash
mongod
```

### Run the app

```bash
python -m app.main
```

---

## 🧩 Usage

1. Launch the app → **Upload Screen** appears

2. Select PDF/DOCX resume → click **Analyze Resume**

3. Result screen shows:

   ✔ PDF page preview (multi-page)
   ✔ Match & similarity scores
   ✔ Matched & missing skills (tag style)

4. Use sidebar to open **History** or **Settings**

---

## 📦 Future Enhancements

🔹 Drag & drop file upload
🔹 Charts for skill match visualization
🔹 Job description input field with NLP parsing
🔹 Export analysis summary to PDF/CSV
🔹 AI skill suggestion using embeddings
🔹 Cloud sync mode (optional)

---

## 🛠 Dependencies

```
customtkinter
pdfplumber
python-docx
pdf2image
Pillow
scikit-learn
nltk
pymongo
pytest
```

---

If you like this repository consider giving it a star.