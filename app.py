
import streamlit as st
from rag import RAGStore
import textwrap
from planner import generate_plan, extract_pdf_text

_original_st_markdown = st.markdown

def _campusflow_markdown(body, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(body, str):
        body = textwrap.dedent(body)
    return _original_st_markdown(body, *args, **kwargs)

st.markdown = _campusflow_markdown

from datetime import date

# =========================================================
# CAMPUSFLOW LITE — FRONTEND
# Approved visual design: Burgundy | Gold | Ivory | Teal
# =========================================================


import textwrap

_base_markdown = _original_st_markdown if "_original_st_markdown" in globals() else st.markdown

def _campusflow_direct_html(body, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(body, str):
        return st.html(textwrap.dedent(body))
    return _base_markdown(body, *args, **kwargs)

st.markdown = _campusflow_direct_html

st.set_page_config(
    page_title="CampusFlow Lite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN TOKENS --------------------

BURGUNDY = "#300810"
BURGUNDY_2 = "#470D1B"
WINE = "#3A0A16"
GOLD = "#D5B16B"
LIGHT_GOLD = "#E6C889"
IVORY = "#F8F1E7"
CREAM = "#F5EDE1"
TEAL = "#063C38"
TEAL_2 = "#0B514B"
INK = "#111313"
MUTED = "#625951"
BORDER = "#E6DCCF"

# Historic university building photograph
CAMPUS_IMAGE = (
    "https://images.unsplash.com/photo-1562774053-701939374585"
    "?auto=format&fit=crop&w=2200&q=90"
)

# -------------------- SESSION STATE --------------------

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def navigate(page):
    st.session_state.page = page

    sidebar_labels = {
        "Home": "Home",
        "Landing": "Home",
        "Dashboard": "Dashboard",
        "PDF Assistant": "PDF Assistant",
        "Complaint Classifier": "Complaint Classifier",
        "AI Study Planner": "Study Planner",
        "About": "About"
    }

    if "sidebar_navigation_v2" in st.session_state:
        st.session_state.sidebar_navigation_v2 = sidebar_labels.get(page, "Dashboard")

# -------------------- GLOBAL CSS --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --burgundy: #300810;
    --burgundy2: #470D1B;
    --gold: #D5B16B;
    --lightgold: #E6C889;
    --ivory: #F8F1E7;
    --cream: #F5EDE1;
    --teal: #063C38;
    --teal2: #0B514B;
    --ink: #111313;
    --muted: #625951;
    --border: #E6DCCF;
}

.stApp {
    background: var(--ivory);
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

#MainMenu, footer { visibility: hidden; }
[data-testid='stHeader'] { visibility: visible !important; background: transparent !important; }

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: var(--burgundy) !important;
}

p, label, li {
    color: var(--ink);
}

.stButton > button {
    background: var(--burgundy);
    color: white !important;
    border: 1px solid var(--burgundy);
    border-radius: 9px;
    min-height: 43px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: var(--teal);
    border-color: var(--teal);
    color: white !important;
}

.stTextInput input,
.stTextArea textarea,
[data-testid="stDateInput"] input {
    background: #FFFCF7 !important;
    color: var(--ink) !important;
    border: 1px solid #D8CABB !important;
    border-radius: 10px !important;
    font-size: 15px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #827B73 !important;
    opacity: 1 !important;
}

[data-testid="stFileUploader"] {
    background: #FFFCF7;
    border: 1px dashed #B99B69;
    border-radius: 13px;
    padding: 15px;
}

[data-testid="stSidebar"] {
    background: var(--burgundy) !important;
    min-width: 250px;
}

[data-testid="stSidebar"] * {
    color: var(--ivory);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--ivory);
}

[data-testid="stSidebar"] hr {
    border-color: var(--gold);
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: transparent;
    border-radius: 9px;
    padding: 8px 10px;
    margin: 3px 0;
    color: var(--ivory) !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(213,177,107,0.18);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: var(--gold);
    color: var(--burgundy) !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {
    color: var(--burgundy) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none;
}

.brand-name {
    font-family: 'Playfair Display', serif;
    color: var(--lightgold);
    font-size: 23px;
    font-weight: 700;
}

.brand-sub {
    color: var(--ivory);
    font-size: 11px;
    letter-spacing: 1.5px;
}

.landing {
    min-height: 690px;
    padding: 25px 32px 28px;
    border-radius: 4px;
    background:
      linear-gradient(90deg,
        rgba(48,8,16,0.97) 0%,
        rgba(48,8,16,0.90) 40%,
        rgba(48,8,16,0.48) 72%,
        rgba(48,8,16,0.20) 100%),
      url("CAMPUS_IMAGE_PLACEHOLDER");
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    border: 1px solid #A9874D;
    color: white;
}

.landing-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 72px;
}

.landing-brand {
    font-family: 'Playfair Display', serif;
    font-size: 23px;
    font-weight: 700;
    color: white;
}

.landing-brand small {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 400;
    color: var(--lightgold);
    letter-spacing: 1px;
}

.nav-pill {
    background: var(--burgundy);
    border: 1px solid var(--gold);
    color: var(--ivory);
    padding: 10px 21px;
    border-radius: 25px;
    font-size: 13px;
    font-weight: 600;
}

.hero-heading {
    font-family: 'Playfair Display', serif;
    font-size: clamp(38px, 4.5vw, 66px);
    line-height: 1.12;
    color: white;
    margin: 0;
}

.hero-highlight {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 4.4vw, 64px);
    line-height: 1.15;
    font-style: italic;
    color: var(--lightgold);
}

.hero-tagline {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    color: var(--gold);
    margin-top: 18px;
}

.hero-description {
    font-size: 15px;
    line-height: 1.8;
    color: #FFF9F0;
    max-width: 460px;
    margin-top: 12px;
}

.landing-card {
    background: rgba(48,8,16,0.84);
    border: 1px solid var(--gold);
    border-radius: 13px;
    min-height: 155px;
    padding: 17px 13px;
    text-align: center;
    color: white;
    margin-top: 25px;
}

.landing-card .symbol {
    color: var(--lightgold);
    font-size: 29px;
}

.landing-card h3 {
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    margin: 8px 0;
}

.landing-card p {
    color: #FFF4E4;
    font-size: 12px;
    line-height: 1.5;
}

.landing-footer {
    color: var(--lightgold);
    font-size: 12px;
    margin-top: 28px;
    letter-spacing: 0.4px;
}

.page-heading {
    font-family: 'Playfair Display', serif;
    color: var(--burgundy);
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 4px;
}

.page-subtitle {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 27px;
}

.profile {
    text-align: right;
    color: var(--burgundy);
    font-size: 14px;
    padding-top: 9px;
    font-weight: 600;
}

.dashboard-card {
    min-height: 260px;
    border-radius: 13px;
    padding: 22px 16px;
    text-align: center;
    color: white;
    box-shadow: 0 5px 14px rgba(30,15,15,0.12);
    margin-bottom: 8px;
}

.dashboard-card.teal {
    background: var(--teal);
}

.dashboard-card.wine {
    background: var(--burgundy2);
}

.card-icon {
    height: 76px;
    width: 76px;
    border: 2px solid var(--gold);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 31px;
    margin: 0 auto 15px;
    color: var(--lightgold);
}

.dashboard-card h3 {
    color: white !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 20px !important;
    margin-bottom: 10px;
}

.dashboard-card p {
    color: #FFF8EC;
    font-size: 13px;
    line-height: 1.6;
    min-height: 42px;
}

.dashboard-banner {
    background: linear-gradient(100deg, #111313, #063C38);
    border: 1px solid #47736A;
    color: var(--lightgold);
    border-radius: 13px;
    padding: 25px;
    margin-top: 22px;
    font-family: 'Playfair Display', serif;
    font-size: 19px;
    font-style: italic;
    text-align: center;
}

.upload-panel {
    background: #FFFCF7;
    border: 1px dashed #B99B69;
    border-radius: 14px;
    padding: 25px;
    text-align: center;
}

.upload-panel h3 {
    font-size: 22px !important;
}

.document-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFCF7;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 13px;
    margin: 8px 0;
    font-size: 14px;
}

.category-card {
    background: #FFFCF7;
    border: 1px solid var(--border);
    border-radius: 11px;
    padding: 16px 5px;
    text-align: center;
    min-height: 108px;
    font-size: 13px;
    font-weight: 600;
}

.category-icon {
    font-size: 25px;
    margin-bottom: 8px;
}

.empty-state {
    background: #FFFCF7;
    border: 1px solid var(--border);
    border-radius: 12px;
    text-align: center;
    padding: 30px 15px;
    margin-top: 10px;
}

.empty-state .symbol {
    font-size: 35px;
    color: #A77B4C;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 23px;
    color: var(--burgundy);
    font-weight: 700;
    margin: 22px 0 12px;
}

.gold-divider {
    border: 0;
    border-top: 1px solid var(--gold);
    margin: 23px 0;
}

.footer {
    text-align: center;
    color: #827B73;
    font-size: 11px;
    margin-top: 40px;
    padding-bottom: 10px;
}

@media (max-width: 800px) {
    .landing {
        padding: 20px;
        min-height: auto;
    }
    .landing-nav {
        margin-bottom: 45px;
    }
    .hero-heading {
        font-size: 38px;
    }
    .hero-highlight {
        font-size: 36px;
    }
    .page-heading {
        font-size: 29px;
    }
}


/* CAMPUSFLOW NAVIGATION REPAIR */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    min-width: 17rem !important;
}
[data-testid="stSidebar"] > div {
    visibility: visible !important;
}
[data-testid="stHeader"] {
    display: flex !important;
    visibility: visible !important;
    height: auto !important;
}
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
}
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
}

</style>
""".replace("CAMPUS_IMAGE_PLACEHOLDER", CAMPUS_IMAGE), unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------


def render_sidebar(active_page):
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center;padding:12px 0 18px;">'
            '<div style="font-size:38px;color:#E6C889;">🎓</div>'
            '<div class="brand-name">CampusFlow Lite</div>'
            '<div class="brand-sub">AI STUDENT ASSISTANT</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        pages = [
            "Dashboard",
            "Home",
            "PDF Assistant",
            "Complaint Classifier",
            "Study Planner",
            "About"
        ]

        radio_key = "sidebar_navigation_v2"

        selected = st.radio(
            "Navigation",
            pages,
            index=pages.index(active_page) if active_page in pages else 0,
            key=radio_key,
            label_visibility="collapsed"
        )

        page_map = {
            "Dashboard": "Dashboard",
            "Home": "Home",
            "PDF Assistant": "PDF Assistant",
            "Complaint Classifier": "Complaint Classifier",
            "Study Planner": "AI Study Planner",
            "About": "About"
        }

        target_page = page_map[selected]

        if target_page != st.session_state.page:
            st.session_state.page = target_page
            st.rerun()

        st.markdown("---")
        st.markdown(
            '<div style="color:#D5B16B;font-size:24px;">❧</div>'
            '<div style="color:#E6C889;font-size:12px;">'
            'Learn · Grow · Succeed</div>',
            unsafe_allow_html=True
        )

# -------------------- PROFILE HEADER --------------------

def profile_header():
    # Profile name intentionally hidden.
    return


def landing_page():
    _, top_start_col = st.columns([5, 1])
    with top_start_col:
        st.button("Get Started →", key="landing_top_get_started", use_container_width=True, on_click=navigate, args=("Home",))

    st.markdown(f"""
    <div class="landing">
        <div class="landing-nav">
            <div class="landing-brand">
                🎓 CampusFlow Lite
                <small>AI STUDENT ASSISTANT</small>
            </div>
            
        </div>

        <div class="hero-heading">Your Campus Life,</div>
        <div class="hero-highlight">Simplified with AI</div>

        <div class="hero-tagline">Ask. Classify. Plan.</div>

        <div class="hero-description">
            Your all-in-one AI assistant for college documents,
            complaints and study planning.
        </div>

        <div style="display:flex;gap:14px;flex-wrap:wrap;">
            <div class="landing-card" style="width:30%;">
                <div class="symbol">▤</div>
                <h3>PDF-based AI Assistant</h3>
                <p>Get answers from your college documents.</p>
            </div>

            <div class="landing-card" style="width:30%;">
                <div class="symbol">▤</div>
                <h3>Smart Complaint Classifier</h3>
                <p>Automatically categorize your complaints.</p>
            </div>

            <div class="landing-card" style="width:30%;">
                <div class="symbol">♙</div>
                <h3>AI Study Planner</h3>
                <p>Create personalized study schedules.</p>
            </div>
        </div>

        <div class="landing-footer">
            Smarter Students &nbsp; • &nbsp; Better Campus
            &nbsp; • &nbsp; Brighter Future
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    _, center, _ = st.columns([2, 2, 2])
    with center:
        st.button("Get Started →", key="landing_bottom_get_started", use_container_width=True, on_click=navigate, args=("Home",))

# -------------------- DASHBOARD --------------------

def dashboard_page():
    profile_header()

    st.markdown(
        '<div class="page-heading">Welcome to CampusFlow Lite</div>'
        '<div class="page-subtitle">'
        'Your AI-powered student assistant</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(3, gap="medium")

    cards = [
        {
            "class": "teal",
            "icon": "▤",
            "title": "PDF-based AI Assistant",
            "description": "Upload college PDFs and get instant answers.",
            "button": "Start Chat →",
            "page": "PDF Assistant"
        },
        {
            "class": "wine",
            "icon": "☏",
            "title": "Smart Complaint Classifier",
            "description": "Enter your complaint and get automatic categorization.",
            "button": "Classify Now →",
            "page": "Complaint Classifier"
        },
        {
            "class": "teal",
            "icon": "▦",
            "title": "AI Study Planner",
            "description": "Plan your studies with an AI-powered schedule.",
            "button": "Create Plan →",
            "page": "AI Study Planner"
        }
    ]

    for col, card in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="dashboard-card {card['class']}">
                <div class="card-icon">{card['icon']}</div>
                <h3>{card['title']}</h3>
                <p>{card['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.button(
                card["button"],
                key="dashboard_" + card["page"],
                use_container_width=True,
                on_click=navigate,
                args=(card["page"],)
            )

    st.markdown("""
    <div class="dashboard-banner">
        ✦ &nbsp; Because every student deserves the right support
        at the right time. &nbsp; ❧
    </div>
    """, unsafe_allow_html=True)

# -------------------- PDF ASSISTANT --------------------
def sync_store(files):
    """Keep the FAISS index in step with the files shown in the UI."""
    if "rag_store" not in st.session_state:
        with st.spinner("Loading AI models (first time only)..."):
            st.session_state.rag_store = RAGStore()
        st.session_state.indexed_keys = set()

    store = st.session_state.rag_store
    current = {(f.name, f.size): f for f in files}

    # A file was removed: clear the index and re-add what remains
    if not st.session_state.indexed_keys.issubset(current.keys()):
        store.reset()
        st.session_state.indexed_keys = set()

    for key, f in current.items():
        if key not in st.session_state.indexed_keys:
            with st.spinner(f"Reading {f.name}..."):
                try:
                    n = store.add_pdf(f, f.name)
                except Exception as e:
                    st.error(f"Could not read {f.name}: {e}")
                    continue
            if n == 0:
                st.warning(f"No readable text in {f.name}. It may be a scanned PDF.")
            else:
                st.session_state.indexed_keys.add(key)
    return store

def pdf_page():
    profile_header()

    st.markdown(
        '<div class="page-heading">PDF-based AI Assistant</div>'
        '<div class="page-subtitle">'
        'Upload your college PDFs and ask questions. '
        'Get accurate answers from your documents using AI.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="upload-panel">
        <div style="font-size:38px;color:#B42D2D;">▤</div>
        <h3>Upload PDF Documents</h3>
        <p>Drag and drop your files here or click to browse.</p>
        <p style="font-size:12px;color:#827B73;">
        Supports PDF files · Maximum 10MB each
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "pdf_saved_files" not in st.session_state:
        st.session_state.pdf_saved_files = []

    new_uploads = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="pdf_upload_widget"
    )

    if new_uploads:
        saved = {
            (f.name, f.size): f
            for f in st.session_state.pdf_saved_files
        }
        for f in new_uploads:
            saved[(f.name, f.size)] = f
        st.session_state.pdf_saved_files = list(saved.values())

    uploaded_files = st.session_state.pdf_saved_files

    st.markdown(
        '<div class="section-heading">Your Documents</div>',
        unsafe_allow_html=True
    )

    if uploaded_files:
        for index, uploaded in enumerate(uploaded_files):
            left, right = st.columns([5, 1])
            with left:
                st.markdown(
                    f'<div class="document-row">'
                    f'<span>📕 &nbsp; {uploaded.name}</span>'
                    f'<span>{uploaded.size / 1024:.1f} KB</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with right:
                if st.button("Remove", key=f"remove_pdf_{index}"):
                    st.session_state.pdf_saved_files.pop(index)
                    st.rerun()
    else:
        st.caption("Your uploaded documents will appear here.")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    with st.form("pdf_question_form", clear_on_submit=True):
        question = st.text_input(
            "Ask a question",
            placeholder="Ask a question about your documents..."
        )
        submitted = st.form_submit_button("➤ Send Question")

    if "pdf_chat" not in st.session_state:
        st.session_state.pdf_chat = []

    if submitted:
        if not uploaded_files:
            st.warning("Please upload a PDF document first.")
        elif not question.strip():
            st.warning("Please enter your question.")
        else:
            store = sync_store(uploaded_files)
            history = [(m["q"], m["answer"]) for m in st.session_state.pdf_chat]
            with st.spinner("Thinking..."):
                try:
                    result = store.answer(question, history=history)
                    st.session_state.pdf_chat.append({
                        "q": question,
                        "answer": result["answer"],
                        "sources": result["sources"],
                    })
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    # newest first, since the input box is above
    for m in reversed(st.session_state.pdf_chat):
        st.markdown(f"**Q:** {m['q']}")
        st.markdown(m["answer"])
        if m["sources"]:
            pages = sorted({(s["source"], s["page"]) for s in m["sources"]})
            st.caption("Sources: " + ", ".join(f"{a} (p.{b})" for a, b in pages))
        st.divider()

    if st.session_state.pdf_chat and st.button("Clear chat", key="pdf_clear_chat"):
        st.session_state.pdf_chat = []
        st.rerun()
# -------------------- COMPLAINT CLASSIFIER --------------------


def complaint_page():
    profile_header()

    st.markdown(
        '<div class="page-heading">Smart Complaint Classifier</div>'
        '<div class="page-subtitle">'
        'Enter your complaint and let AI automatically categorize it.'
        '</div>',
        unsafe_allow_html=True
    )

    complaint = st.text_area(
        "Your complaint",
        placeholder="Type your complaint here...",
        height=180,
        max_chars=1000,
        key="complaint_text"
    )

    st.caption(f"{len(complaint)} / 1000 characters")

    if st.button("✦ Classify", use_container_width=True,
                 key="classify_complaint"):
        if not complaint.strip():
            st.warning("Please enter your complaint.")
        else:
            st.info(
                "The trained machine-learning classifier "
                "will be connected here."
            )

    st.markdown(
        '<div class="section-heading">Possible Categories</div>',
        unsafe_allow_html=True
    )

    category_options = [
        "🎓  Examination",
        "🪙  Fees",
        "▣  IT",
        "⌂  Hostel",
        "•••  Other"
    ]

    st.markdown(
        '<p style="color:#827B73;font-size:13px;">'
        'Select a category to explore it. This selection does not '
        'represent an AI classification result.'
        '</p>',
        unsafe_allow_html=True
    )

    selected_category = st.radio(
        "Select a category",
        category_options,
        horizontal=True,
        label_visibility="collapsed",
        key="selected_complaint_category"
    )

    st.session_state["complaint_category_selection"] = selected_category

# -------------------- STUDY PLANNER --------------------


def planner_page():
    profile_header()

    st.markdown(
        '<div class="page-heading">AI Study Planner</div>'
        '<div class="page-subtitle">'
        'Enter your subjects, syllabus and exam date '
        'to get a personalized study schedule.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Subjects**")

    subjects = st.text_area(
        "Subjects",
        placeholder="e.g. Data Structures, DBMS, Operating Systems",
        height=95,
        label_visibility="collapsed",
        key="planner_subjects"
    )

    st.markdown("**Exam Date**")

    exam_date = st.date_input(
        "Exam date",
        value=date.today(),
        min_value=date.today(),
        format="DD/MM/YYYY",
        label_visibility="collapsed",
        key="planner_exam_date"
    )

    st.markdown("**Syllabus / Important Topics**")

    syllabus = st.text_area(
        "Syllabus",
        placeholder="Enter your syllabus and important topics...",
        height=110,
        label_visibility="collapsed",
        key="planner_syllabus"
    )

    st.markdown("**Upload PDF Notes / Syllabus (Optional)**")

    if "planner_saved_pdfs" not in st.session_state:
        st.session_state.planner_saved_pdfs = []

    planner_uploads = st.file_uploader(
        "Upload PDF notes",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="planner_pdf_upload"
    )

    if planner_uploads:
        saved = {
            (f.name, f.size): f
            for f in st.session_state.planner_saved_pdfs
        }
        for f in planner_uploads:
            saved[(f.name, f.size)] = f
        st.session_state.planner_saved_pdfs = list(saved.values())

    for index, pdf in enumerate(st.session_state.planner_saved_pdfs):
        left, right = st.columns([5, 1])
        with left:
            st.caption(f"📕 {pdf.name} · {pdf.size / 1024:.1f} KB")
        with right:
            if st.button("Remove", key=f"planner_remove_pdf_{index}"):
                st.session_state.planner_saved_pdfs.pop(index)
                st.rerun()

    st.markdown("**Study Hours Per Day**")
    hours_per_day = st.slider(
        "Hours per day", 1, 12, 4,
        label_visibility="collapsed",
        key="planner_hours"
    )

    if st.button(
        "✦ Generate Study Plan",
        use_container_width=True,
        key="generate_study_plan"
    ):
        if not subjects.strip() or not syllabus.strip():
            st.warning("Please enter your subjects and syllabus.")
        elif exam_date <= date.today():
            st.warning("Please choose an exam date after today.")
        else:
            with st.spinner("Creating your study plan..."):
                try:
                    notes = extract_pdf_text(st.session_state.planner_saved_pdfs)
                    st.session_state.study_plan = generate_plan(
                        subjects, syllabus, exam_date, hours_per_day, notes
                    )
                except Exception as e:
                    st.error(f"Could not generate the plan: {e}")

    st.markdown(
        '<div class="section-heading">Your Study Plan</div>',
        unsafe_allow_html=True
        )

    if st.session_state.get("study_plan"):
        st.markdown(st.session_state.study_plan)
        st.download_button(
            "⬇ Download plan",
            st.session_state.study_plan,
            file_name="study_plan.md",
            key="download_study_plan"
        )
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="symbol">▦</div>
            <h3 style="font-size:20px;">No plan yet.</h3>
            <p>Fill in the details and get your personalized study schedule.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- ABOUT --------------------

def about_page():
    profile_header()

    st.markdown(
        '<div class="page-heading">About CampusFlow Lite</div>',
        unsafe_allow_html=True
    )

    st.write(
        "CampusFlow Lite is an AI-powered student assistant "
        "designed to simplify everyday academic activities."
    )

    st.markdown("### Our three core modules")

    st.write("1. PDF-based AI Assistant — document-based question answering.")
    st.write("2. Smart Complaint Classifier — machine-learning-based classification.")
    st.write("3. AI Study Planner — personalized study scheduling.")

    st.markdown("### Technology Stack")

    st.write(
        "Python · Streamlit · Scikit-learn · Embeddings · FAISS · "
        "Generative AI · SQLite"
    )

# -------------------- APP ROUTING --------------------


st.markdown("""
<style>
div.stButton > button {
    color: #FFFFFF !important;
    background: #470D1B !important;
    border: 1px solid #D5B16B !important;
    font-weight: 700 !important;
}
div.stButton > button:hover {
    color: #FFFFFF !important;
    background: #300810 !important;
    border-color: #E6C889 !important;
}
div.stButton > button p,
div.stButton > button span {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

current_page = st.session_state.page

if current_page == "Dashboard":
    landing_page()
else:
    sidebar_names = {
        "Dashboard": "Dashboard",
        "Landing": "Home",
        "PDF Assistant": "PDF Assistant",
        "Complaint Classifier": "Complaint Classifier",
        "AI Study Planner": "Study Planner",
        "About": "About"
    }

    render_sidebar(sidebar_names.get(current_page, "Home"))

    if current_page != "Dashboard":
        st.sidebar.button("← Back to Dashboard", key="back_to_home", use_container_width=True, on_click=navigate, args=("Dashboard",))

    if current_page in ("Home", "Landing"):
        dashboard_page()
    elif current_page == "PDF Assistant":
        pdf_page()
    elif current_page == "Complaint Classifier":
        complaint_page()
    elif current_page == "AI Study Planner":
        planner_page()
    elif current_page == "About":
        about_page()

st.markdown(
    '<div class="footer">CAMPUSFLOW LITE · LEARN · GROW · SUCCEED</div>',
    unsafe_allow_html=True
)
