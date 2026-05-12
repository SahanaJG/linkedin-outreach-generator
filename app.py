"""
LinkedIn Outreach Message Generator
Powered by Google Gemini AI
"""

import streamlit as st
import google.generativeai as genai
import os
import time
from datetime import datetime


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LinkedIn Outreach Generator",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS – refined dark editorial aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --surface2:  #1a1e28;
    --border:    #252a38;
    --accent:    #4f8ef7;
    --accent2:   #a78bfa;
    --gold:      #f0c040;
    --text:      #e8eaf0;
    --muted:     #7a8099;
    --success:   #34d399;
    --font-head: 'DM Serif Display', Georgia, serif;
    --font-body: 'DM Sans', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --radius:    12px;
    --radius-lg: 20px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer {
    visibility: hidden;
}

/* Keep header visible so sidebar toggle works */
header {
    background: transparent !important;
}

/* Hide deploy button only */
.stDeployButton {
    display: none;
}

/* Sidebar toggle styling */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 99999 !important;
}

[data-testid="collapsedControl"] button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── Main container ── */
.main .block-container {
    padding: 2.5rem 2.5rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Hero header ── */
.hero-title {
    font-family: var(--font-head);
    font-size: 3.2rem;
    line-height: 1.1;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #e8eaf0 30%, #4f8ef7 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    font-family: var(--font-body);
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 300;
    margin-bottom: 2.5rem;
    letter-spacing: 0.3px;
}

/* ── Section labels ── */
.section-label {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Input cards ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}
label, .stSelectbox label, .stTextInput label {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.4px !important;
    text-transform: uppercase !important;
}

/* ── Generate button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, #6366f1 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.85rem 2rem !important;
    font-family: var(--font-body) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Output message cards ── */
.msg-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    transition: border-color 0.2s;
}
.msg-card:hover { border-color: #353a50; }
.msg-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
.msg-badge {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 500;
}
.badge-connect  { background: rgba(79,142,247,0.15); color: var(--accent); border: 1px solid rgba(79,142,247,0.3); }
.badge-cold     { background: rgba(167,139,250,0.15); color: var(--accent2); border: 1px solid rgba(167,139,250,0.3); }
.badge-followup { background: rgba(240,192,64,0.15);  color: var(--gold);   border: 1px solid rgba(240,192,64,0.3); }
.badge-email    { background: rgba(52,211,153,0.15);  color: var(--success); border: 1px solid rgba(52,211,153,0.3); }
.msg-body {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.75;
    color: var(--text);
    white-space: pre-wrap;
    background: var(--surface2);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    border: 1px solid var(--border);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.sidebar-logo {
    font-family: var(--font-head);
    font-size: 1.5rem;
    background: linear-gradient(135deg, #4f8ef7, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.sidebar-pill {
    display: inline-block;
    background: rgba(79,142,247,0.1);
    border: 1px solid rgba(79,142,247,0.25);
    color: var(--accent) !important;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 1.4rem;
}
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
    color: var(--muted) !important;
    line-height: 1.5;
}
.tip-icon { flex-shrink: 0; font-size: 1rem; margin-top: 1px; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 1rem !important;
    border-radius: 8px !important;
    width: auto !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Success / error msgs ── */
.stAlert { border-radius: var(--radius) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GEMINI SETUP
# ─────────────────────────────────────────────
def get_gemini_client():
    """
    Load Gemini API key from Streamlit secrets or environment variable.
    Priority: st.secrets → os.environ → user input in sidebar.
    """
    api_key = None
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = os.environ.get("GEMINI_API_KEY")
    return api_key


def configure_gemini(api_key: str):
    """Configure the Gemini SDK with the given key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",           # fast + low token cost
        generation_config=genai.types.GenerationConfig(
            temperature=0.85,
            max_output_tokens=8192,
        ),
    )


# ─────────────────────────────────────────────
# PROMPT BUILDER
# ─────────────────────────────────────────────
LENGTH_GUIDE = {
    "Short":  "Keep each message under 80 words.",
    "Medium": "Keep each message between 80–150 words.",
    "Long":   "Write detailed messages of 150–220 words each.",
}

TONE_GUIDE = {
    "Professional": "Write in a polished, credible, third-person-aware professional tone. No slang.",
    "Friendly":     "Write in a warm, conversational, first-name-basis tone. Approachable but still business-focused.",
    "Startup":      "Write in an energetic, direct, slightly informal startup tone. Bold value props, no fluff.",
    "Formal":       "Write in a highly formal, structured business tone. Full sentences, respectful salutations.",
}

def build_prompt(name, role, company, industry, tone, length, include_email):
    """
    Construct a structured prompt for Gemini to generate all outreach messages.
    Returns a single prompt string requesting JSON-like delimited sections.
    """
    email_section = """
4. EMAIL_OUTREACH
   A cold outreach email with Subject line on the first line (prefix with "Subject: "),
   then a blank line, then the email body. Keep it crisp and compelling.
""" if include_email else ""

    prompt = f"""
You are an expert B2B SaaS sales strategist and LinkedIn copywriter.
Generate highly personalized outreach messages for the following prospect.

─── PROSPECT DETAILS ───
Name:     {name}
Role:     {role}
Company:  {company}
Industry: {industry}

─── STYLE GUIDELINES ───
Tone:   {TONE_GUIDE[tone]}
Length: {LENGTH_GUIDE[length]}

─── PERSONALIZATION RULES ───
• Reference the prospect's role and company naturally — do NOT be generic.
• Lead with value or a relevant insight, never "I hope this message finds you well."
• End each message with a clear, low-pressure call-to-action.
• Avoid clichés: "synergy", "game-changer", "circle back", "touch base".
• Sound human. No corporate fluff.

─── OUTPUT FORMAT ───
Return EXACTLY four (or five) labeled sections separated by [SECTION] markers.
Do NOT include any other text outside these sections.

[SECTION:CONNECTION_REQUEST]
A LinkedIn connection note (≤300 characters, platform limit). Crisp, personal, compelling.

[SECTION:COLD_OUTREACH]
A LinkedIn direct message for cold outreach. Value-first, specific to their role/industry.

[SECTION:FOLLOW_UP]
A follow-up message assuming the first went unanswered (5–7 days later). Lighter touch, different angle.
{email_section}
[END]
"""
    return prompt.strip()


# ─────────────────────────────────────────────
# RESPONSE PARSER
# ─────────────────────────────────────────────
def parse_sections(raw: str) -> dict:
    """
    Parse Gemini's delimited output into a dict keyed by section name.
    Falls back gracefully if markers are missing.
    """
    sections = {}
    # Normalise line endings and strip any markdown code fences Gemini may add
    raw = raw.replace("```", "").strip()
    parts = raw.split("[SECTION:")
    for part in parts[1:]:                      # skip everything before first marker
        if "]" in part:
            key, _, body = part.partition("]")
            # Remove the [END] sentinel and any trailing noise
            body = body.split("[END]")[0]
            # Also strip any next [SECTION: marker that leaked in
            body = body.split("[SECTION:")[0]
            sections[key.strip()] = body.strip()
    return sections


# ─────────────────────────────────────────────
# GENERATION FUNCTION
# ─────────────────────────────────────────────
def generate_messages(model, name, role, company, industry, tone, length, include_email):
    """Call Gemini and return parsed sections dict."""
    prompt = build_prompt(name, role, company, industry, tone, length, include_email)
    response = model.generate_content(prompt)
    return parse_sections(response.text)


# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────
def render_message_card(title: str, badge_class: str, content: str, key: str):
    """Render a styled message card with copy-to-clipboard button."""
    st.markdown(f"""
    <div class="msg-card">
        <div class="msg-card-header">
            <span class="msg-badge {badge_class}">{title}</span>
        </div>
        <div class="msg-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)

    # Copy-to-clipboard via a text_area trick (hidden) + native st button
    col1, col2 = st.columns([4, 1])
    with col2:
        st.download_button(
            label="⬇ Save",
            data=content,
            file_name=f"{key}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            key=f"dl_{key}",
        )


def build_export_text(sections: dict, name: str, company: str) -> str:
    """Build a full export .txt from all generated sections."""
    lines = [
        f"LinkedIn Outreach Messages",
        f"Prospect: {name} @ {company}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        "",
    ]
    label_map = {
        "CONNECTION_REQUEST": "CONNECTION REQUEST",
        "COLD_OUTREACH":      "COLD OUTREACH MESSAGE",
        "FOLLOW_UP":          "FOLLOW-UP MESSAGE",
        "EMAIL_OUTREACH":     "EMAIL OUTREACH",
    }
    for key, label in label_map.items():
        if key in sections:
            lines += [f"── {label} ──", sections[key], ""]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔗 OutreachAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-pill">Powered by Gemini</div>', unsafe_allow_html=True)

    st.markdown("**About**")
    st.markdown("""
    <div style="font-size:0.88rem; color:#7a8099; line-height:1.7; margin-bottom:1.2rem;">
    Generate personalized LinkedIn connection requests, cold outreach messages,
    follow-ups, and cold emails in seconds — tailored to your prospect's role,
    company, and industry.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Tips for Best Results**")
    tips = [
        ("🎯", "Be specific — exact job titles outperform generic ones"),
        ("✍️", "Use 'Startup' tone for early-stage company contacts"),
        ("⏱️", "Short messages get higher response rates on LinkedIn"),
        ("📧", "Enable email section for multi-channel outreach"),
        ("🔄", "Regenerate 2–3 times to find the best variant"),
    ]
    for icon, tip in tips:
        st.markdown(f'<div class="tip-item"><span class="tip-icon">{icon}</span>{tip}</div>',
                    unsafe_allow_html=True)

    st.divider()

    # API Key input (fallback if not in secrets/env)
    sidebar_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza… (leave blank if set in env)",
        help="Get your free key at makersuite.google.com",
    )


# ─────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────
st.markdown('<h1 class="hero-title">LinkedIn Outreach<br>Message Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">AI-crafted, hyper-personalized outreach that actually gets replies.</p>', unsafe_allow_html=True)

# ── Resolve API key ──────────────────────────
api_key = get_gemini_client() or sidebar_api_key
if not api_key:
    st.warning("⚠️  Enter your Gemini API key in the sidebar to get started.")

# ── Input form ──────────────────────────────
st.markdown('<div class="section-label">01 / Prospect Details</div>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        prospect_name = st.text_input("Prospect Name", placeholder="e.g. Sarah Chen")
        company_name  = st.text_input("Company Name",  placeholder="e.g. Notion Labs")
    with col2:
        job_role = st.text_input("Job Role",  placeholder="e.g. Head of Growth")
        industry = st.text_input("Industry", placeholder="e.g. B2B SaaS / FinTech")

st.markdown('<div class="section-label" style="margin-top:1.5rem;">02 / Message Style</div>', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    tone   = st.selectbox("Tone", ["Professional", "Friendly", "Startup", "Formal"])
with col4:
    length = st.selectbox("Message Length", ["Short", "Medium", "Long"])
with col5:
    include_email = st.selectbox("Include Email Outreach?", ["Yes", "No"]) == "Yes"

st.markdown("")
generate_btn = st.button("✦ Generate Outreach Messages", use_container_width=True)


# ─────────────────────────────────────────────
# GENERATION LOGIC
# ─────────────────────────────────────────────
if generate_btn:
    # Validation
    missing = [f for f, v in [
        ("Prospect Name", prospect_name),
        ("Job Role",      job_role),
        ("Company Name",  company_name),
        ("Industry",      industry),
    ] if not v.strip()]

    if missing:
        st.error(f"Please fill in: {', '.join(missing)}")
    elif not api_key:
        st.error("Add your Gemini API key in the sidebar first.")
    else:
        try:
            model = configure_gemini(api_key)

            with st.spinner("Crafting your personalized messages…"):
                start = time.time()
                sections = generate_messages(
                    model, prospect_name, job_role, company_name,
                    industry, tone, length, include_email
                )
                elapsed = round(time.time() - start, 1)

            if not sections:
                st.error("Couldn't parse Gemini's response. Try regenerating.")
            else:
                # Store in session state for export
                st.session_state["sections"]  = sections
                st.session_state["meta_name"] = prospect_name
                st.session_state["meta_co"]   = company_name

                st.success(f"Generated in {elapsed}s — {len(sections)} message(s) ready.")

        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "429" in err:
                st.error("Rate limit hit. Wait a minute and try again, or use a different API key.")
            elif "api_key" in err.lower() or "401" in err or "403" in err:
                st.error("Invalid API key. Check your key at makersuite.google.com.")
            else:
                st.error(f"Error: {err}")


# ─────────────────────────────────────────────
# OUTPUT DISPLAY
# ─────────────────────────────────────────────
if "sections" in st.session_state and st.session_state["sections"]:
    sections = st.session_state["sections"]
    st.divider()
    st.markdown('<div class="section-label">03 / Generated Messages</div>', unsafe_allow_html=True)

    CARD_CONFIG = [
        ("CONNECTION_REQUEST", "Connection Request",   "badge-connect"),
        ("COLD_OUTREACH",      "Cold Outreach",        "badge-cold"),
        ("FOLLOW_UP",          "Follow-Up Message",    "badge-followup"),
        ("EMAIL_OUTREACH",     "Email Outreach",       "badge-email"),
    ]

    for key, label, badge in CARD_CONFIG:
        if key in sections:
            render_message_card(label, badge, sections[key], key.lower())

    # ── Export all ──────────────────────────
    st.divider()
    export_txt = build_export_text(
        sections,
        st.session_state["meta_name"],
        st.session_state["meta_co"],
    )
    st.download_button(
        label="⬇ Export All Messages as TXT",
        data=export_txt,
        file_name=f"outreach_{st.session_state['meta_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
    )
