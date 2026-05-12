# 🔗 LinkedIn Outreach Message Generator

> AI-crafted, hyper-personalized LinkedIn outreach messages that actually get replies — powered by Google Gemini.

---

## 📌 Project Overview

A sleek, dark-mode Streamlit web app that generates **four types of outreach messages** in seconds:

| Message Type | Description |
|---|---|
| **Connection Request** | ≤300-char LinkedIn note — personal & compelling |
| **Cold Outreach** | First DM — value-first, role-specific |
| **Follow-Up** | 5–7 day follow-up — lighter angle, new hook |
| **Email Outreach** | Cold email with subject line (optional) |

Ideal for **SDRs, founders, recruiters, freelancers**, and anyone doing B2B outreach.

---

## ✨ Features

- 🤖 **Gemini AI** — fast, cost-efficient `gemini-1.5-flash` model
- 🎨 **Dark editorial UI** — portfolio-worthy, not generic
- 🎯 **4 tone modes** — Professional / Friendly / Startup / Formal
- 📏 **3 length modes** — Short / Medium / Long
- 📋 **Per-message save** — download each message as `.txt`
- 📦 **Export all** — one-click full export with metadata
- 🔐 **Secure API key** — via Streamlit secrets or environment variable
- ✅ **Input validation** — graceful empty-field handling
- ⚡ **Rate limit handling** — clear error messages on quota hits

---

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit 1.35+ |
| AI Model | Google Gemini 1.5 Flash (`google-generativeai`) |
| Styling | Custom CSS (DM Serif Display + DM Sans + JetBrains Mono) |
| Language | Python 3.10+ |

---

## 🚀 Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourname/linkedin-outreach-generator.git
cd linkedin-outreach-generator
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Gemini API key

**Option A — Streamlit secrets (recommended for deployment)**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "AIza..."
```

**Option B — Environment variable**

```bash
export GEMINI_API_KEY="AIza..."          # macOS/Linux
set GEMINI_API_KEY=AIza...               # Windows CMD
$env:GEMINI_API_KEY="AIza..."            # PowerShell
```

**Option C — Sidebar input**  
Enter your key directly in the app's sidebar at runtime.

> 🔑 Get a free API key at [makersuite.google.com](https://makersuite.google.com/app/apikey)

---

## ▶️ How to Run Locally

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🗂 Project Structure

```
linkedin-outreach-generator/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── secrets.toml        # API key (gitignored)
```

---

## 💡 Sample Prompt Structure

The app sends Gemini a structured prompt like this:

```
You are an expert B2B SaaS sales strategist and LinkedIn copywriter.
Generate highly personalized outreach messages for the following prospect.

─── PROSPECT DETAILS ───
Name:     Sarah Chen
Role:     Head of Growth
Company:  Notion Labs
Industry: B2B SaaS

─── STYLE GUIDELINES ───
Tone:   Energetic, direct startup tone. Bold value props, no fluff.
Length: Keep each message under 80 words.

─── PERSONALIZATION RULES ───
• Reference the prospect's role and company naturally.
• Lead with value — never "I hope this finds you well."
• End with a clear, low-pressure CTA.
• No clichés: synergy, game-changer, circle back, touch base.

─── OUTPUT FORMAT ───
[SECTION:CONNECTION_REQUEST] ...
[SECTION:COLD_OUTREACH] ...
[SECTION:FOLLOW_UP] ...
[SECTION:EMAIL_OUTREACH] ...  (optional)
[END]
```

---

## 🤝 Contributing

PRs welcome. Open an issue first for major changes.

---

## 📄 License

MIT — free to use, fork, and build on.
