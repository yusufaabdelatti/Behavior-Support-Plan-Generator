# -*- coding: utf-8 -*-
"""
Individual Behavior Support Plan Generator
============================================
Streamlit app for nursery/child development professionals.
Generates premium PDF and Word (.docx) reports.
"""

import streamlit as st
import io
import base64
from datetime import datetime, date
from PIL import Image

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Behavior Support Plan Generator",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# GLOBAL STYLES
# -----------------------------------------------------------------------------
def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap');

    :root {
        --sand:    #F5F0E8;
        --linen:   #F0EBE1;
        --cream:   #FAF8F4;
        --bark:    #8B7355;
        --bark-lt: #B09A7A;
        --stone:   #6B6456;
        --ink:     #2A2520;
        --border:  #DDD8CE;
        --sage:    #7A8A72;
        --radius:  12px;
        --shadow:  0 2px 24px rgba(42,37,32,0.08);
    }

    html, body, [class*="css"] {
        font-family: 'Jost', sans-serif !important;
        background-color: var(--sand) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--cream) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: 'Jost', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        color: var(--bark) !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Main area */
    .main .block-container {
        padding: 1.5rem 2rem 3rem !important;
        max-width: 100% !important;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* App header */
    .app-header {
        display: flex; align-items: center; gap: 0.75rem;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .app-header-mark {
        width: 40px; height: 40px;
        background: var(--ink); border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; color: #fff;
    }
    .app-header-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.5rem; font-weight: 500;
        color: var(--ink); line-height: 1.2;
    }
    .app-header-sub { font-size: 0.78rem; color: var(--stone); }

    /* Buttons */
    .stButton > button {
        font-family: 'Jost', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 9px !important;
        transition: all 0.18s !important;
    }
    .stDownloadButton > button {
        font-family: 'Jost', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 9px !important;
        width: 100% !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select,
    .stNumberInput input, .stDateInput input {
        border-radius: 8px !important;
        font-family: 'Jost', sans-serif !important;
    }

    /* Section dividers in sidebar */
    .sidebar-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 0.5rem 0;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Jost', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        background: var(--linen) !important;
        border-radius: 8px !important;
    }

    /* Info box */
    .stInfo { border-radius: 10px !important; }

    /* Document preview container */
    .doc-preview-wrap {
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 8px 40px rgba(42,37,32,0.12);
        overflow: hidden;
        max-width: 820px;
        margin: 0 auto;
        font-family: 'Cormorant Garamond', serif;
    }

    .doc-hdr {
        background: #2A2520;
        padding: 2.5rem 3rem 2rem;
        color: #fff;
        position: relative;
    }
    .doc-hdr-top {
        display: flex; justify-content: space-between;
        align-items: flex-start; margin-bottom: 1.75rem;
    }
    .doc-nursery-nm {
        font-family: 'Jost', sans-serif;
        font-size: 0.85rem; font-weight: 300;
        letter-spacing: 0.1em; text-transform: uppercase;
        color: rgba(255,255,255,0.6);
    }
    .doc-badge {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 4px; padding: 0.2rem 0.6rem;
        font-family: 'Jost', sans-serif;
        font-size: 0.65rem; letter-spacing: 0.12em;
        text-transform: uppercase; color: rgba(255,255,255,0.5);
    }
    .doc-main-title {
        font-size: 2.1rem; font-weight: 300; line-height: 1.2;
        margin-bottom: 0.3rem;
    }
    .doc-main-sub {
        font-size: 0.95rem; font-weight: 300;
        color: rgba(255,255,255,0.6); font-style: italic;
    }

    .doc-info-bar {
        display: grid; grid-template-columns: repeat(4, 1fr);
        background: #F0EBE1;
        border-bottom: 1px solid #DDD8CE;
    }
    .doc-info-cell {
        padding: 0.9rem 1.1rem;
        border-right: 1px solid #DDD8CE;
    }
    .doc-info-cell:last-child { border-right: none; }
    .doc-info-lbl {
        font-family: 'Jost', sans-serif;
        font-size: 0.6rem; font-weight: 600;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: #8B7355; margin-bottom: 0.2rem;
    }
    .doc-info-val {
        font-size: 0.95rem; font-weight: 400; color: #2A2520;
    }

    .doc-body { padding: 2.2rem 3rem; }

    .doc-sec { margin-bottom: 2rem; }
    .doc-sec-hdr {
        display: flex; align-items: center; gap: 0.65rem;
        margin-bottom: 0.85rem; padding-bottom: 0.5rem;
        border-bottom: 1px solid #DDD8CE;
    }
    .doc-sec-num {
        width: 24px; height: 24px;
        background: #2A2520; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Jost', sans-serif;
        font-size: 0.68rem; font-weight: 600; color: #fff;
        flex-shrink: 0;
    }
    .doc-sec-title {
        font-size: 1.2rem; font-weight: 400; color: #2A2520;
    }

    .doc-p {
        font-size: 0.94rem; line-height: 1.8; color: #3A3530;
        font-weight: 300; margin-bottom: 0.5rem;
    }

    .doc-skill-blk {
        background: #F0EBE1; border-radius: 9px;
        padding: 1rem 1.2rem; margin-bottom: 0.7rem;
        border-left: 3px solid #8B7355;
    }
    .doc-skill-title {
        font-size: 1rem; font-weight: 500; color: #2A2520;
        margin-bottom: 0.3rem;
    }
    .doc-skill-body {
        font-size: 0.87rem; line-height: 1.7;
        color: #4A4540; font-weight: 300;
    }

    .doc-bullet-item {
        display: flex; align-items: flex-start; gap: 0.55rem;
        padding: 0.45rem 0; border-bottom: 1px solid #F0EBE1;
        font-size: 0.9rem; line-height: 1.65; color: #3A3530; font-weight: 300;
    }
    .doc-bullet-item:last-child { border-bottom: none; }
    .doc-dot {
        width: 5px; height: 5px; background: #8B7355;
        border-radius: 50%; margin-top: 0.6rem; flex-shrink: 0;
    }

    .doc-tag {
        display: inline-block; padding: 0.2rem 0.6rem;
        border-radius: 99px; background: #F0EBE1;
        border: 1px solid #DDD8CE;
        font-family: 'Jost', sans-serif; font-size: 0.75rem;
        color: #6B6456; margin: 0.15rem;
    }
    .doc-level {
        display: inline-block; padding: 0.15rem 0.55rem;
        border-radius: 99px; font-family: 'Jost', sans-serif;
        font-size: 0.72rem; font-weight: 500; text-transform: capitalize;
        margin-left: 0.3rem;
    }
    .doc-level-low    { background: #EAF2E8; color: #4A6A42; }
    .doc-level-moderate { background: #FEF6E4; color: #8A6420; }
    .doc-level-high   { background: #FAECE8; color: #8A3A2A; }

    .doc-monitor-tbl { width: 100%; border-collapse: collapse; }
    .doc-monitor-tbl th {
        background: #2A2520; color: #fff; padding: 0.5rem 0.8rem;
        font-family: 'Jost', sans-serif; font-size: 0.67rem;
        font-weight: 500; letter-spacing: 0.07em; text-transform: uppercase;
        text-align: left;
    }
    .doc-monitor-tbl td {
        padding: 0.6rem 0.8rem; font-size: 0.9rem;
        border-bottom: 1px solid #DDD8CE; color: #2A2520;
    }
    .doc-monitor-tbl tr:nth-child(even) td { background: #F5F0E8; }

    .doc-progress-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
    }
    .doc-progress-card {
        background: #F0EBE1; border-radius: 9px;
        padding: 0.85rem 1rem; border: 1px solid #DDD8CE;
    }
    .doc-progress-icon { font-size: 1.1rem; margin-bottom: 0.25rem; }
    .doc-progress-title {
        font-family: 'Jost', sans-serif;
        font-size: 0.82rem; font-weight: 500; color: #2A2520; margin-bottom: 0.15rem;
    }
    .doc-progress-body {
        font-size: 0.8rem; line-height: 1.55; color: #6B6456; font-weight: 300;
    }

    .doc-collab-grid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.6rem;
    }
    .doc-collab-card {
        background: #F0EBE1; border-radius: 9px;
        padding: 0.9rem; text-align: center; border: 1px solid #DDD8CE;
    }
    .doc-collab-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
    .doc-collab-title {
        font-family: 'Jost', sans-serif;
        font-size: 0.85rem; font-weight: 500; color: #2A2520; margin-bottom: 0.25rem;
    }
    .doc-collab-body {
        font-size: 0.78rem; line-height: 1.55; color: #6B6456; font-weight: 300;
    }

    .doc-footer {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1rem 3rem; background: #F0EBE1;
        border-top: 1px solid #DDD8CE;
        font-family: 'Jost', sans-serif; font-size: 0.7rem; color: #6B6456;
    }

    /* Export section */
    .export-box {
        background: var(--cream);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1.5rem;
    }
    .export-title {
        font-family: 'Jost', sans-serif;
        font-size: 0.65rem; font-weight: 600;
        letter-spacing: 0.14em; text-transform: uppercase;
        color: var(--bark); margin-bottom: 0.75rem;
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SKILL DEFINITIONS
# -----------------------------------------------------------------------------
SKILL_DETAILS = {
    "Emotional Regulation": (
        "Emotional Regulation",
        "The child will develop the ability to identify, understand, and manage emotional responses in a "
        "developmentally appropriate manner. Activities will focus on building an internal emotional vocabulary, "
        "recognizing physiological cues of dysregulation, and applying self-soothing strategies with guided adult "
        "support before transitioning toward greater independence."
    ),
    "Impulse Control": (
        "Impulse Control (Inhibitory Control)",
        "Inhibitory control — the capacity to pause, reflect, and redirect an impulse before acting — is a "
        "foundational executive function skill. Sessions will target this through structured stop-and-think games, "
        "delayed gratification activities, and consistent adult modeling of reflective pausing. Progress will be "
        "measured by an observable increase in the child's latency between trigger and behavioral response."
    ),
    "Frustration Tolerance": (
        "Frustration Tolerance",
        "The child will be gradually and safely exposed to manageable frustration experiences within a supported "
        "environment. Sessions will teach the child to recognize frustration as a temporary, tolerable state, and "
        "to deploy a toolkit of coping strategies — including verbal expression, physical regulation activities, "
        "and requesting adult support — rather than escalating to disruptive behavior."
    ),
    "Communication Skills": (
        "Functional Communication Skills",
        "A primary driver of challenging behavior in early childhood is limited access to functional communication. "
        "This plan will prioritize the development of verbal and non-verbal communication pathways that allow the "
        "child to express needs, preferences, and distress in socially acceptable ways. Replacement behavior "
        "training will be central to this goal."
    ),
    "Social Skills": (
        "Social Skills and Peer Interaction",
        "The child will develop age-appropriate skills in reading social cues, turn-taking, cooperative play, and "
        "conflict resolution. Sessions will use structured peer interaction activities, social stories, and "
        "role-play scenarios to build a repertoire of positive social behaviors that can be generalized to the "
        "classroom environment."
    ),
    "Self-Awareness": (
        "Self-Awareness and Emotional Literacy",
        "The child will build an increasing awareness of their own emotional states, bodily sensations associated "
        "with emotion, and the impact of their behavior on others. This foundational skill supports all other "
        "targeted areas and will be developed through reflective activities, visual tools, and consistent, "
        "non-judgmental adult dialogue."
    ),
    "Coping Strategies": (
        "Coping Strategy Development",
        "The child will be introduced to and will practice a personalized toolkit of coping strategies appropriate "
        "to their developmental level. Strategies may include deep breathing techniques, movement breaks, sensory "
        "regulation tools, and structured calming corners. The goal is for the child to begin accessing these "
        "tools with decreasing levels of adult support over time."
    ),
}

BEHAVIOR_OPTIONS = [
    "Throwing objects", "Hitting / kicking others", "Dropping to the floor",
    "Tantrums / meltdowns", "Biting", "Screaming / shouting",
    "Refusing transitions", "Destroying materials", "Running away / elopement",
    "Self-injurious behavior", "Spitting", "Verbal aggression",
]

MONITORING_ROWS = [
    ("Behavior type and topography",
     "Description of the specific behavior observed, its physical characteristics, and the context in which it occurred."),
    ("Trigger identification",
     "The antecedent events or conditions (internal and environmental) that preceded the behavior."),
    ("Response intensity",
     "Severity of the behavioral episode rated on a consistent 1–5 scale to track changes over time."),
    ("Recovery time",
     "Time elapsed from onset of behavioral escalation to return to a regulated, engaged baseline state."),
    ("Use of replacement behaviors",
     "Whether the child initiated or responded to prompts to use a replacement behavior, and the degree of adult support required."),
    ("Adult response fidelity",
     "Whether the planned intervention protocol was implemented as designed during the session."),
]

PROGRESS_CARDS = [
    ("⏱", "Increased Latency to Reaction",
     "An observable pause between the trigger event and the behavioral response, indicating developing inhibitory control."),
    ("📉", "Reduced Behavioral Intensity",
     "A measurable decrease in the severity of behavioral episodes over a consistent time period."),
    ("🔄", "Faster Recovery",
     "A progressive reduction in the time required to return to a calm, engaged state following dysregulation."),
    ("💬", "Improved Communication",
     "Increased frequency of using verbal or non-verbal communication to express needs, particularly in high-demand situations."),
    ("✋", "Spontaneous Replacement Behaviors",
     "The child independently initiating a replacement behavior without adult prompting in the natural environment."),
    ("🌍", "Generalisation Across Settings",
     "Transfer of skill use beyond the formal session context into the broader nursery environment and, where reported, the home setting."),
]

ACTIVITY_ITEMS = [
    ("Co-regulation activities",
     "Guided breathing techniques, sensory regulation tools, and calming rituals to help the child experience and "
     "internalise regulated states before working toward independent regulation."),
    ("Inhibitory control games",
     "Stop-and-go games, impulse delay exercises, and structured waiting activities that build the neurological "
     "pathways underlying self-control."),
    ("Structured play challenges",
     "Activities deliberately designed to include manageable difficulty, turn-taking requirements, and peer "
     "interaction to build frustration tolerance and social competence."),
    ("Replacement behavior rehearsal",
     "Explicit teaching and repeated practice of socially acceptable replacement behaviors for each identified "
     "concern behavior (e.g., using words instead of hitting; requesting a break instead of throwing)."),
    ("Positive reinforcement systems",
     "Consistent, specific, and immediate reinforcement of target behaviors and approximations toward target "
     "behaviors, using individually motivating reinforcers identified in collaboration with the child and family."),
    ("Reflective dialogue",
     "Age-appropriate post-incident discussion to build the child's capacity for emotional retrospection "
     "and self-awareness without shame or blame."),
]


# -----------------------------------------------------------------------------
# DOCUMENT PREVIEW (HTML)
# -----------------------------------------------------------------------------
def render_html_preview(d):
    """Render the full document as HTML for the Streamlit preview."""
    today = datetime.now().strftime("%d %B %Y")
    start = (d["start_date"].strftime("%d %B %Y")
             if d.get("start_date") else "—")
    all_behaviors = d["behaviors"] + ([d["custom_behavior"]] if d.get("custom_behavior") else [])

    # Logo
    logo_html = ""
    if d.get("logo_bytes"):
        b64 = base64.b64encode(d["logo_bytes"]).decode()
        logo_html = f'<img src="data:image/png;base64,{b64}" style="max-height:48px;max-width:130px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.85;" />'
    else:
        logo_html = f'<span class="doc-nursery-nm">{d.get("nursery_name","Nursery Name")}</span>'

    # Behaviors
    tag_html = "".join(f'<span class="doc-tag">{b}</span>' for b in all_behaviors) if all_behaviors \
               else '<span class="doc-tag" style="opacity:0.4">None specified</span>'

    level_cls = {"low":"doc-level-low","moderate":"doc-level-moderate","high":"doc-level-high"}
    freq_badge = f'<span class="doc-level {level_cls.get(d["frequency"],"")}">{d["frequency"]}</span>'
    int_badge  = f'<span class="doc-level {level_cls.get(d["intensity"],"")}">{d["intensity"]}</span>'

    # Skills
    skills_html = ""
    for s in d.get("skills", []):
        if s in SKILL_DETAILS:
            title, body = SKILL_DETAILS[s]
            skills_html += f"""
            <div class="doc-skill-blk">
                <div class="doc-skill-title">{title}</div>
                <div class="doc-skill-body">{body}</div>
            </div>"""
    if not skills_html:
        skills_html = '<p class="doc-p" style="opacity:0.4">No skills selected.</p>'

    # Activities
    activities_html = "".join(
        f'<div class="doc-bullet-item"><div class="doc-dot"></div>'
        f'<div><strong>{t}:</strong> {b}</div></div>'
        for t, b in ACTIVITY_ITEMS
    )

    # Monitoring table
    monitor_rows = "".join(
        f'<tr><td><strong>{d_}</strong></td><td>{r}</td></tr>'
        for d_, r in MONITORING_ROWS
    )

    # Progress cards
    progress_cards = "".join(
        f'<div class="doc-progress-card"><div class="doc-progress-icon">{ic}</div>'
        f'<div class="doc-progress-title">{t}</div>'
        f'<div class="doc-progress-body">{b}</div></div>'
        for ic, t, b in PROGRESS_CARDS
    )

    # Notes
    notes_html = ""
    if d.get("notes") and d["notes"].strip():
        notes_html = f"""
        <div style="margin-top:1.2rem;padding:1rem 1.2rem;background:#F0EBE1;border-radius:9px;border:1px solid #DDD8CE;">
            <strong style="font-family:'Jost',sans-serif;font-size:0.82rem;color:#8B7355;">Additional Notes</strong>
            <p class="doc-p" style="margin-top:0.4rem;">{d["notes"]}</p>
        </div>"""

    footer_text = d.get("footer_text") or "Confidential — For internal and family use only."
    child_name  = d.get("child_name") or "—"
    nursery     = d.get("nursery_name") or "Nursery"
    pattern     = d.get("pattern") or "No specific pattern noted."

    html = f"""
    <div class="doc-preview-wrap">
        <!-- HEADER -->
        <div class="doc-hdr">
            <div class="doc-hdr-top">
                {logo_html}
                <span class="doc-badge">Confidential</span>
            </div>
            <div class="doc-main-title">Individual Behavior<br>Support Plan</div>
            <div class="doc-main-sub">Developmental Support Programme — {nursery}</div>
        </div>

        <!-- INFO BAR -->
        <div class="doc-info-bar">
            <div class="doc-info-cell">
                <div class="doc-info-lbl">Child Name</div>
                <div class="doc-info-val">{child_name}</div>
            </div>
            <div class="doc-info-cell">
                <div class="doc-info-lbl">Date of Birth</div>
                <div class="doc-info-val">{d["date_of_birth"].strftime("%d %B %Y") if d.get("date_of_birth") else "—"}</div>
            </div>
            <div class="doc-info-cell">
                <div class="doc-info-lbl">Age</div>
                <div class="doc-info-val">{d.get("age","—")}</div>
            </div>
            <div class="doc-info-cell">
                <div class="doc-info-lbl">Class / Group</div>
                <div class="doc-info-val">{d.get("class_group","—")}</div>
            </div>
        </div>

        <!-- BODY -->
        <div class="doc-body">

            <!-- 1. PURPOSE -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">1</div>
                    <div class="doc-sec-title">Programme Purpose &amp; Scope</div>
                </div>
                <p class="doc-p">This Individual Behavior Support Plan has been developed to provide structured,
                evidence-informed support for <strong>{child_name}'s</strong> developmental needs. It is important
                to note that this plan is <em>not</em> a diagnostic document, nor does it imply the presence of any
                clinical condition or disorder.</p>
                <p class="doc-p">The purpose of this programme is to build specific developmental skills — including
                emotional regulation, impulse control, frustration tolerance, and functional communication — within
                the safe, consistent, and nurturing environment of the nursery setting.</p>
                <p class="doc-p">All interventions are grounded in a positive, strengths-based framework that
                emphasises the child's capacity for growth. Progress is expected to occur gradually and
                non-linearly; the programme is designed to be responsive and adaptive based on ongoing observation
                and collaboration with the family.</p>
                <p class="doc-p" style="font-family:'Jost',sans-serif;font-size:0.85rem;color:#6B6456;">
                    <strong>Sessions per month:</strong> {d.get("sessions_per_month","—")} &nbsp;&nbsp;
                    <strong>Frequency:</strong> {d.get("session_frequency","—")}
                </p>
            </div>

            <!-- 2. BEHAVIORAL CONCERNS -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">2</div>
                    <div class="doc-sec-title">Identified Behavioral Concerns</div>
                </div>
                <p class="doc-p">The following behaviors have been identified as current areas of focus. These
                behaviors are understood as the child's current best attempt to communicate unmet needs or to manage
                experiences that exceed their present regulatory capacity:</p>
                <div style="margin:0.6rem 0 0.8rem;">{tag_html}</div>
                <p class="doc-p">
                    <strong>Frequency:</strong>{freq_badge} &nbsp;&nbsp;
                    <strong>Intensity:</strong>{int_badge}
                </p>
                <p class="doc-p"><strong>Recent Pattern / Context:</strong> {pattern}</p>
            </div>

            <!-- 3. SKILLS -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">3</div>
                    <div class="doc-sec-title">Core Skills Targeted</div>
                </div>
                <p class="doc-p">The following skill areas have been selected as the primary targets for this
                programme. Each skill area is interconnected; progress in one domain typically supports development
                across others.</p>
                {skills_html}
            </div>

            <!-- 4. ACTIVITIES -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">4</div>
                    <div class="doc-sec-title">Session Activities</div>
                </div>
                <p class="doc-p">Sessions will incorporate a variety of structured, play-based, and reflective
                activities designed to build the targeted skills in an engaging and developmentally appropriate
                manner:</p>
                {activities_html}
            </div>

            <!-- 5. MONITORING -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">5</div>
                    <div class="doc-sec-title">Session Monitoring Framework</div>
                </div>
                <p class="doc-p">Each session will be monitored using the following framework to track behavioral
                patterns, responses to intervention, and progress over time:</p>
                <table class="doc-monitor-tbl">
                    <thead>
                        <tr><th>Monitoring Dimension</th><th>What Is Recorded</th></tr>
                    </thead>
                    <tbody>{monitor_rows}</tbody>
                </table>
            </div>

            <!-- 6. PROGRESS -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">6</div>
                    <div class="doc-sec-title">Indicators of Progress</div>
                </div>
                <p class="doc-p">Progress will be evaluated through direct observation, session notes, and regular
                review meetings. The following indicators will be used as primary markers of meaningful progress:</p>
                <div class="doc-progress-grid">{progress_cards}</div>
            </div>

            <!-- 7. COLLABORATION -->
            <div class="doc-sec">
                <div class="doc-sec-hdr">
                    <div class="doc-sec-num">7</div>
                    <div class="doc-sec-title">Family &amp; Team Collaboration</div>
                </div>
                <p class="doc-p">This programme operates on the understanding that meaningful and lasting
                developmental change occurs when the child's key environments are aligned in their approach and
                consistent in their response.</p>
                <div class="doc-collab-grid">
                    <div class="doc-collab-card">
                        <div class="doc-collab-icon">🏫</div>
                        <div class="doc-collab-title">Nursery Team</div>
                        <div class="doc-collab-body">Teaching staff are briefed on programme goals and monitoring
                        frameworks. Fortnightly check-ins ensure responsiveness and fidelity to the plan.</div>
                    </div>
                    <div class="doc-collab-card">
                        <div class="doc-collab-icon">👩‍🏫</div>
                        <div class="doc-collab-title">Behavioral Therapist</div>
                        <div class="doc-collab-body">The assigned behavioral therapist maintains session monitoring records
                        and serves as primary liaison between the programme and the classroom environment.{f" Therapist: <strong>{d.get('therapist_name')}</strong>." if d.get('therapist_name') else ""}</div>
                    </div>
                    <div class="doc-collab-card">
                        <div class="doc-collab-icon">👨‍👩‍👧</div>
                        <div class="doc-collab-title">Family Partnership</div>
                        <div class="doc-collab-body">Parents receive regular written updates and recommended home
                        reinforcement strategies. Family input is actively valued and integral to all reviews.</div>
                    </div>
                </div>
                {notes_html}
            </div>

        </div><!-- /doc-body -->

        <!-- FOOTER -->
        <div class="doc-footer">
            <span>{footer_text}</span>
            <span style="color:#8B7355;">Generated: {today} | {nursery}</span>
        </div>
    </div>
    """
    return html


# -----------------------------------------------------------------------------
# PDF GENERATION  (reportlab)
# -----------------------------------------------------------------------------
def build_pdf(d) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, KeepTogether, Image as RLImage
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from io import BytesIO

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=2.2*cm, rightMargin=2.2*cm,
                             topMargin=2.5*cm, bottomMargin=2.5*cm)

    # Palette
    INK        = colors.HexColor("#2A2520")
    BARK       = colors.HexColor("#8B7355")
    BARK_LT    = colors.HexColor("#B09A7A")
    STONE      = colors.HexColor("#6B6456")
    LINEN      = colors.HexColor("#F0EBE1")
    WARM       = colors.HexColor("#FAF8F4")
    WARM2      = colors.HexColor("#F5F0E8")
    BORDER     = colors.HexColor("#DDD8CE")
    WHITE      = colors.white
    LEVEL_COLS = {
        "low":      (colors.HexColor("#EAF2E8"), colors.HexColor("#4A6A42")),
        "moderate": (colors.HexColor("#FEF6E4"), colors.HexColor("#8A6420")),
        "high":     (colors.HexColor("#FAECE8"), colors.HexColor("#8A3A2A")),
    }

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sTitle   = S("T",  fontName="Helvetica-Bold",  fontSize=20, textColor=INK,
                       leading=26, alignment=TA_CENTER, spaceAfter=4)
    sSub2    = S("Su", fontName="Helvetica",        fontSize=10, textColor=STONE,
                       leading=14, alignment=TA_CENTER, spaceAfter=2)
    sSection = S("Se", fontName="Helvetica-Bold",   fontSize=10, textColor=BARK,
                       leading=14, spaceBefore=14, spaceAfter=4)
    sBody    = S("Bo", fontName="Helvetica",         fontSize=9.5, textColor=INK,
                       leading=15, spaceAfter=4)
    sBullet  = S("Bu", fontName="Helvetica",         fontSize=9.5, textColor=INK,
                       leading=15, leftIndent=14, spaceAfter=3)
    sSmall   = S("Sm", fontName="Helvetica",         fontSize=8.5, textColor=STONE, leading=13)
    sFooter  = S("Fo", fontName="Helvetica-Oblique", fontSize=7.5, textColor=STONE,
                       alignment=TA_CENTER)
    sSkillT  = S("ST", fontName="Helvetica-Bold",    fontSize=10, textColor=INK, leading=14, spaceAfter=2)
    sSkillB  = S("SB", fontName="Helvetica",         fontSize=9,  textColor=colors.HexColor("#4A4540"),
                       leading=14, spaceAfter=2)

    def hr(c=BARK, t=0.8):
        return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=5, spaceBefore=5)
    def sp(h=0.25):
        return Spacer(1, h*cm)

    today = datetime.now().strftime("%d %B %Y")
    start = d["start_date"].strftime("%d %B %Y") if d.get("start_date") else "—"
    all_behaviors = d["behaviors"] + ([d["custom_behavior"]] if d.get("custom_behavior") else [])
    nursery   = d.get("nursery_name") or "Nursery"
    child     = d.get("child_name")   or "—"
    footer_t  = d.get("footer_text")  or "Confidential — For internal and family use only."

    story = []

    # -- Title block ------------------------------------------------------------
    story += [
        Paragraph("Individual Behavior Support Plan", sTitle),
        Paragraph(f"Developmental Support Programme — {nursery}", sSub2),
        sp(0.3), hr(INK, 1.5), sp(0.2),
    ]

    # -- Logo (if uploaded) ----------------------------------------------------
    if d.get("logo_bytes"):
        try:
            img_buf = BytesIO(d["logo_bytes"])
            img = RLImage(img_buf, width=3*cm, height=1.8*cm, kind="proportional")
            img.hAlign = "CENTER"
            story += [img, sp(0.2)]
        except Exception:
            pass

    # -- Demographic table ------------------------------------------------------
    dob_str = d["date_of_birth"].strftime("%d %B %Y") if d.get("date_of_birth") else "—"
    therapist = d.get("therapist_name") or "—"

    demo_rows = [
        [Paragraph("<b>Child Name</b>",     sSmall), Paragraph(child,                       sBody),
         Paragraph("<b>Date of Birth</b>",  sSmall), Paragraph(dob_str,                     sBody)],
        [Paragraph("<b>Age</b>",            sSmall), Paragraph(d.get("age","—"),            sBody),
         Paragraph("<b>Class / Group</b>",  sSmall), Paragraph(d.get("class_group","—"),    sBody)],
        [Paragraph("<b>Therapist</b>",      sSmall), Paragraph(therapist,                   sBody),
         Paragraph("<b>Start Date</b>",     sSmall), Paragraph(start,                       sBody)],
        [Paragraph("<b>Sessions/month</b>", sSmall), Paragraph(str(d.get("sessions_per_month","—")), sBody),
         Paragraph("<b>Frequency</b>",      sSmall), Paragraph(d.get("session_frequency","—"), sBody)],
    ]
    demo_tbl = Table(demo_rows, colWidths=[3.0*cm, 6.0*cm, 3.0*cm, 4.2*cm])
    demo_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,-1), LINEN),
        ("BACKGROUND",   (2,0),(2,-1), LINEN),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WARM, WARM2, WARM, WARM2]),
        ("GRID",         (0,0),(-1,-1), 0.4, BORDER),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 7),
    ]))
    story += [demo_tbl, sp(0.4)]

    # -- Confidential badge -----------------------------------------------------
    badge_row = [[Paragraph("<b>  CONFIDENTIAL DOCUMENT  </b>",
        S("CB", fontName="Helvetica-Bold", fontSize=9, textColor=BARK, alignment=TA_CENTER))]]
    badge_tbl = Table(badge_row, colWidths=[16.2*cm])
    badge_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LINEN),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("BOX",          (0,0),(-1,-1), 0.5, BARK),
    ]))
    story += [badge_tbl, sp(0.5)]

    def sec_hdr(num, title):
        row = [[Paragraph(str(num),
                S("SN", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, alignment=TA_CENTER)),
                Paragraph(f"<b>{title}</b>",
                S("ST2", fontName="Helvetica-Bold", fontSize=11, textColor=INK))]]
        t = Table(row, colWidths=[0.7*cm, 15.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(0,0), INK),
            ("BACKGROUND",    (1,0),(1,0), LINEN),
            ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",    (0,0),(-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("LEFTPADDING",   (0,0),(0,0), 0),
            ("LEFTPADDING",   (1,0),(1,0), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("LINEBELOW",     (0,0),(-1,-1), 0.5, BARK),
        ]))
        return t

    def bullet_p(title, body):
        return Paragraph(f"<b>{title}:</b> {body}", sBullet)

    # -- Section 1 — Purpose ----------------------------------------------------
    story += [sec_hdr(1, "Programme Purpose & Scope"), sp(0.15)]
    story += [
        Paragraph(f"This Individual Behavior Support Plan has been developed to provide structured, "
                  f"evidence-informed support for <b>{child}'s</b> developmental needs. It is important to note "
                  f"that this plan is not a diagnostic document, nor does it imply the presence of any clinical "
                  f"condition or disorder.", sBody),
        Paragraph("The purpose of this programme is to build specific developmental skills — including "
                  "emotional regulation, impulse control, frustration tolerance, and functional communication — "
                  "within the safe, consistent, and nurturing environment of the nursery setting.", sBody),
        Paragraph("All interventions are grounded in a positive, strengths-based framework that emphasises "
                  "the child's capacity for growth. Progress is expected to occur gradually and non-linearly; "
                  "the programme is designed to be responsive and adaptive based on ongoing observation and "
                  "collaboration with the family.", sBody),
        sp(0.4),
    ]

    # -- Section 2 — Behavioral Concerns ----------------------------------------
    story += [sec_hdr(2, "Identified Behavioral Concerns"), sp(0.15)]
    story.append(Paragraph("The following behaviors have been identified as current areas of focus. "
                            "These behaviors are understood as the child's current best attempt to communicate "
                            "unmet needs or to manage experiences that exceed their present regulatory capacity:", sBody))

    if all_behaviors:
        beh_text = " | ".join(all_behaviors)
        story.append(Paragraph(beh_text, S("BT", fontName="Helvetica-Oblique", fontSize=9.5,
                                            textColor=STONE, leading=14, spaceBefore=4, spaceAfter=4,
                                            leftIndent=10, borderPad=4)))

    freq_bg, freq_fg = LEVEL_COLS.get(d.get("frequency","moderate"), LEVEL_COLS["moderate"])
    int_bg,  int_fg  = LEVEL_COLS.get(d.get("intensity","moderate"),  LEVEL_COLS["moderate"])

    level_row = [
        [Paragraph("<b>Frequency</b>", sSmall),
         Paragraph(d.get("frequency","—").capitalize(),
                   S("LV", fontName="Helvetica-Bold", fontSize=9, textColor=freq_fg)),
         Paragraph("<b>Intensity</b>", sSmall),
         Paragraph(d.get("intensity","—").capitalize(),
                   S("LV2", fontName="Helvetica-Bold", fontSize=9, textColor=int_fg))],
    ]
    lv_tbl = Table(level_row, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 3.5*cm])
    lv_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (1,0),(1,0), freq_bg),
        ("BACKGROUND",   (3,0),(3,0), int_bg),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("BOX",          (1,0),(1,0), 0.4, BORDER),
        ("BOX",          (3,0),(3,0), 0.4, BORDER),
    ]))
    story += [lv_tbl, sp(0.1)]

    if d.get("pattern"):
        story.append(Paragraph(f"<b>Recent Pattern / Context:</b> {d['pattern']}", sBody))
    story.append(sp(0.4))

    # -- Section 3 — Skills -----------------------------------------------------
    story += [sec_hdr(3, "Core Skills Targeted"), sp(0.15)]
    story.append(Paragraph("The following skill areas have been selected as the primary targets for this "
                            "programme. Each skill area is interconnected; progress in one domain typically "
                            "supports development across others.", sBody))

    for s in d.get("skills", []):
        if s in SKILL_DETAILS:
            title, body = SKILL_DETAILS[s]
            skill_row = [[
                Paragraph(f"<b>{title}</b>", sSkillT),
                Paragraph(body, sSkillB),
            ]]
            st2 = Table(skill_row, colWidths=[4.0*cm, 12.2*cm])
            st2.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), LINEN),
                ("LINEAFTER",    (0,0),(0,0), 3, BARK),
                ("TOPPADDING",   (0,0),(-1,-1), 8),
                ("BOTTOMPADDING",(0,0),(-1,-1), 8),
                ("LEFTPADDING",  (0,0),(-1,-1), 10),
                ("VALIGN",       (0,0),(-1,-1), "TOP"),
            ]))
            story += [st2, sp(0.15)]
    story.append(sp(0.3))

    # -- Section 4 — Activities -------------------------------------------------
    story += [sec_hdr(4, "Session Activities"), sp(0.15)]
    story.append(Paragraph("Sessions will incorporate a variety of structured, play-based, and reflective "
                            "activities designed to build the targeted skills in an engaging and developmentally "
                            "appropriate manner:", sBody))
    for t_, b_ in ACTIVITY_ITEMS:
        story.append(bullet_p(t_, b_))
    story.append(sp(0.4))

    # -- Section 5 — Monitoring -------------------------------------------------
    story += [sec_hdr(5, "Session Monitoring Framework"), sp(0.15)]
    story.append(Paragraph("Each session will be monitored using the following framework to track behavioral "
                            "patterns, responses to intervention, and progress over time:", sBody))

    mon_data = [[Paragraph("<b>Monitoring Dimension</b>",
                            S("MH", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE)),
                  Paragraph("<b>What Is Recorded</b>",
                            S("MH2", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE))]]
    for d_, r in MONITORING_ROWS:
        mon_data.append([Paragraph(f"<b>{d_}</b>", sBody), Paragraph(r, sBody)])

    mon_tbl = Table(mon_data, colWidths=[5.5*cm, 10.7*cm])
    mon_tbl.setStyle(TableStyle([
        ("BACKGROUND",       (0,0),(-1,0), INK),
        ("ROWBACKGROUNDS",   (0,1),(-1,-1), [WARM, LINEN]),
        ("GRID",             (0,0),(-1,-1), 0.4, BORDER),
        ("TOPPADDING",       (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",    (0,0),(-1,-1), 6),
        ("LEFTPADDING",      (0,0),(-1,-1), 8),
        ("VALIGN",           (0,0),(-1,-1), "MIDDLE"),
    ]))
    story += [mon_tbl, sp(0.4)]

    # -- Section 6 — Progress ---------------------------------------------------
    story += [sec_hdr(6, "Indicators of Progress"), sp(0.15)]
    story.append(Paragraph("Progress will be evaluated through direct observation, session notes, and regular "
                            "review meetings. The following indicators will be used as primary markers of "
                            "meaningful progress:", sBody))

    prog_pairs = list(zip(PROGRESS_CARDS[::2], PROGRESS_CARDS[1::2]))
    for left, right in prog_pairs:
        row = [
            [Paragraph(f"<b>{left[0]} {left[1]}</b>",
              S("PC", fontName="Helvetica-Bold", fontSize=9, textColor=INK)),
             Paragraph(left[2], sSmall)],
            [Paragraph(f"<b>{right[0]} {right[1]}</b>",
              S("PC2", fontName="Helvetica-Bold", fontSize=9, textColor=INK)),
             Paragraph(right[2], sSmall)],
        ]
        pt = Table(
            [[row[0][0], row[1][0]], [row[0][1], row[1][1]]],
            colWidths=[8.1*cm, 8.1*cm]
        )
        pt.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), LINEN),
            ("BOX",          (0,0),(0,-1), 0.4, BORDER),
            ("BOX",          (1,0),(1,-1), 0.4, BORDER),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ]))
        story += [pt, sp(0.1)]
    story.append(sp(0.3))

    # -- Section 7 — Collaboration ---------------------------------------------
    story += [sec_hdr(7, "Family & Team Collaboration"), sp(0.15)]
    story.append(Paragraph("This programme operates on the understanding that meaningful and lasting "
                            "developmental change occurs when the child's key environments are aligned in their "
                            "approach and consistent in their response.", sBody))

    collab = [
        ("Nursery Team", "Teaching staff are briefed on programme goals and monitoring frameworks. "
                         "Fortnightly check-ins ensure responsiveness and fidelity to the plan."),
        ("Behavioral Therapist", f"{'The therapist assigned to this programme is ' + d.get('therapist_name') + '.' if d.get('therapist_name') else 'The assigned behavioral therapist'} maintains session monitoring records and serves as "
                         "primary liaison between the programme and the classroom environment."),
        ("Family Partnership", "Parents receive regular written updates and recommended home reinforcement "
                               "strategies. Family input is actively valued and integral to all reviews."),
    ]
    col_data = [[
        [Paragraph(f"<b>{t}</b>", S("CT", fontName="Helvetica-Bold", fontSize=9, textColor=INK)),
         Paragraph(b, sSmall)]
        for t, b in collab
    ]]
    flat = [[col_data[0][i][0] for i in range(3)], [col_data[0][i][1] for i in range(3)]]
    ctbl = Table(flat, colWidths=[5.4*cm, 5.4*cm, 5.4*cm])
    ctbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LINEN),
        ("GRID",         (0,0),(-1,-1), 0.4, BORDER),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story += [ctbl, sp(0.2)]

    if d.get("notes") and d["notes"].strip():
        story += [
            Paragraph("<b>Additional Notes</b>",
                      S("AN", fontName="Helvetica-Bold", fontSize=9.5, textColor=BARK,
                        spaceBefore=10, spaceAfter=4)),
            Paragraph(d["notes"], sBody),
        ]

    # -- Footer ----------------------------------------------------------------
    story += [
        sp(0.5), hr(STONE, 0.5),
        Paragraph(f"{footer_t}  |  Generated: {today}  |  {nursery}", sFooter),
    ]

    def add_page_number(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(STONE)
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.drawRightString(A4[0] - 2.2*cm, 1.2*cm, text)
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return buf.getvalue()


# -----------------------------------------------------------------------------
# SUGGESTED BEHAVIORAL ACTIVITIES (for staff PDF)
# -----------------------------------------------------------------------------
SUGGESTED_ACTIVITIES = [
    (
        "Emotion Volcano 🌋",
        "Emotional Regulation / Self-Awareness",
        "Draw a volcano together and label the stages: calm (bottom), building up (middle), erupting (top). "
        "Ask the child to identify where they are on the volcano throughout the session. "
        "Practice 'cooling lava' strategies: slow belly breaths, squeezing a stress ball, or shaking hands and letting go. "
        "Over time, aim for the child to self-identify and self-regulate before reaching the 'eruption' stage.",
    ),
    (
        "Freeze & Think 🛑",
        "Impulse Control",
        "Play music and move around the room. When the music stops, freeze completely. "
        "While frozen, the child must answer a 'think' question (e.g. 'What would you do if a friend took your toy?'). "
        "Gradually extend freeze time. Use visual stop/go cards to generalise the skill to classroom triggers.",
    ),
    (
        "The Waiting Jar ⏳",
        "Frustration Tolerance / Delayed Gratification",
        "Place a small treat or sticker inside a clear jar. Tell the child they can have it at the end of the session "
        "if they practice waiting when something feels hard. Each time the child waits without escalating, add a "
        "marble or token to a second jar so they can see progress visually. Celebrate each success explicitly.",
    ),
    (
        "Feelings Detectives 🔍",
        "Emotional Literacy / Communication",
        "Use picture cards of faces showing different emotions. Ask the child to guess the feeling and think of a time "
        "they felt that way. Role-play what that character could say or do instead of acting out. "
        "Progress to using cartoon scenarios closer to real classroom situations.",
    ),
    (
        "The Replacement Behavior Rehearsal 🔄",
        "Functional Communication / Replacement Behaviors",
        "Identify the top two or three problem behaviors and their typical triggers. "
        "Explicitly teach and rehearse one replacement behavior for each (e.g., tapping the table instead of hitting; "
        "saying 'I need a break' instead of running away). Practice in low-stakes role-play first, "
        "then gradually introduce mild stressors to build generalisation.",
    ),
    (
        "Compliment Catch 🌟",
        "Social Skills / Peer Interaction",
        "Sit with the child and, where safe, a peer or nursery adult. Each person catches a soft ball and must say "
        "one genuine compliment to the next person before throwing. Begin therapist-to-child only, then introduce "
        "a trusted peer. Debrief: 'How did it feel to give/receive a compliment?'",
    ),
    (
        "Calm Corner Design 🎨",
        "Coping Strategy Development / Self-Regulation",
        "Collaboratively design the child's own 'calm corner' toolkit on paper or in a small box. "
        "Include: a chosen breathing exercise card, a sensory item, a picture of something calming, and a feelings chart. "
        "Practice using each item during the session so the child can access them independently in the classroom.",
    ),
    (
        "Puppet Problem-Solving 🎭",
        "Social Skills / Conflict Resolution",
        "Use puppets or soft toys to act out a common conflict scenario (e.g., two puppets want the same toy). "
        "Guide the child to direct the puppets to a solution step-by-step: stop → feel → think → act. "
        "Switch roles so the child also plays the 'problem-solving coach'. Link solutions to real nursery situations.",
    ),
    (
        "Body Check-In 🧘",
        "Emotional Regulation / Physiological Awareness",
        "Begin each session with a brief 'body scan': starting at the feet, notice what each part of the body feels. "
        "Introduce vocabulary (tight shoulders = nervous; heavy arms = tired; wobbly tummy = worried). "
        "Create a simple body map and mark where feelings live. "
        "Repeat at the end of the session to notice any changes after regulation practice.",
    ),
    (
        "The Success Story Book 📖",
        "Self-Awareness / Progress Tracking",
        "Each session, help the child dictate or draw one thing they did well this week — however small. "
        "Collect these in a personalised booklet. Review together to build a narrative of competence and growth. "
        "Share (with the child's permission) one page with parents each fortnight to reinforce the message at home.",
    ),
]


# -----------------------------------------------------------------------------
# STAFF PDF (with suggested activities appended)
# -----------------------------------------------------------------------------
def build_pdf_staff(d) -> bytes:
    """Wraps build_pdf and appends a 'Suggested Behavioral Activities' section."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, PageBreak
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from io import BytesIO

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=2.2*cm, rightMargin=2.2*cm,
                             topMargin=2.5*cm, bottomMargin=2.5*cm)

    INK   = colors.HexColor("#2A2520")
    BARK  = colors.HexColor("#8B7355")
    STONE = colors.HexColor("#6B6456")
    LINEN = colors.HexColor("#F0EBE1")
    WARM  = colors.HexColor("#FAF8F4")
    WARM2 = colors.HexColor("#F5F0E8")
    BORDER= colors.HexColor("#DDD8CE")
    SAGE  = colors.HexColor("#7A8A72")
    WHITE = colors.white

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sTitle  = S("AT", fontName="Helvetica-Bold",  fontSize=18, textColor=INK,
                      leading=24, alignment=TA_CENTER, spaceAfter=4)
    sSub    = S("AS", fontName="Helvetica",        fontSize=10, textColor=STONE,
                      leading=14, alignment=TA_CENTER, spaceAfter=10)
    sHead   = S("AH", fontName="Helvetica-Bold",   fontSize=11, textColor=INK,
                      leading=15, spaceBefore=6, spaceAfter=3)
    sDomain = S("AD", fontName="Helvetica-Oblique",fontSize=9,  textColor=BARK,
                      leading=13, spaceAfter=4)
    sBody   = S("AB", fontName="Helvetica",         fontSize=9.5, textColor=INK,
                      leading=15, spaceAfter=4)
    sFooter = S("AF", fontName="Helvetica-Oblique", fontSize=7.5, textColor=STONE,
                      alignment=TA_CENTER)
    sNum    = S("AN2",fontName="Helvetica-Bold",    fontSize=22, textColor=BARK,
                      leading=26, spaceAfter=0)

    def hr(c=BARK, t=0.8):
        return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=5, spaceBefore=5)
    def sp(h=0.25):
        return Spacer(1, h*cm)

    # Reuse the main plan story from build_pdf, then append activities
    # We rebuild here using build_pdf as source but add the activities section
    # First get the main PDF bytes and then append — but since ReportLab doesn't
    # support merging easily, we rebuild fully: call build_pdf internals inline.

    today = datetime.now().strftime("%d %B %Y")
    nursery = d.get("nursery_name") or "Nursery"
    footer_t = d.get("footer_text") or "Confidential — For internal use only."
    child = d.get("child_name") or "—"

    # Get main plan story by calling the internal build
    main_bytes = build_pdf(d)

    # Now build the activities-only supplement and merge with PyPDF
    act_buf = BytesIO()
    act_doc = SimpleDocTemplate(act_buf, pagesize=A4,
                                 leftMargin=2.2*cm, rightMargin=2.2*cm,
                                 topMargin=2.5*cm, bottomMargin=2.5*cm)

    story = []
    story += [
        Paragraph("Suggested Behavioral Activities", sTitle),
        Paragraph(f"Session Resource Supplement — {child} — {nursery}", sSub),
        sp(0.2), hr(INK, 1.5), sp(0.3),
        Paragraph(
            "The following activities are recommended as structured, evidence-informed tools to support "
            "the skills targeted in this behaviour support plan. Each activity is designed to be engaging, "
            "developmentally appropriate, and adaptable to the child's current level. Activities should be "
            "selected based on the child's focus areas and may be used across multiple sessions.",
            sBody),
        sp(0.4),
    ]

    for i, (name, domain, description) in enumerate(SUGGESTED_ACTIVITIES, 1):
        act_row = [[
            Paragraph(str(i), sNum),
            [Paragraph(name, sHead),
             Paragraph(f"Target Area: {domain}", sDomain),
             Paragraph(description, sBody)]
        ]]
        act_tbl = Table(act_row, colWidths=[1.2*cm, 15.0*cm])
        act_tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), LINEN if i % 2 == 1 else WARM2),
            ("LINEAFTER",    (0,0),(0,0), 3, BARK),
            ("TOPPADDING",   (0,0),(-1,-1), 10),
            ("BOTTOMPADDING",(0,0),(-1,-1), 10),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
            ("BOX",          (0,0),(-1,-1), 0.4, BORDER),
        ]))
        story += [act_tbl, sp(0.2)]

    story += [
        sp(0.5), hr(STONE, 0.5),
        Paragraph(f"{footer_t}  |  Behavioral Activities Supplement  |  Generated: {today}  |  {nursery}", sFooter),
    ]

    def add_page_num(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(STONE)
        canvas_obj.drawRightString(A4[0] - 2.2*cm, 1.2*cm, f"Page {canvas_obj.getPageNumber()}")
        canvas_obj.restoreState()

    act_doc.build(story, onFirstPage=add_page_num, onLaterPages=add_page_num)
    act_bytes = act_buf.getvalue()

    # Merge: main plan + activities supplement
    try:
        from pypdf import PdfWriter, PdfReader
        writer = PdfWriter()
        for src in [main_bytes, act_bytes]:
            reader = PdfReader(BytesIO(src))
            for page in reader.pages:
                writer.add_page(page)
        merged = BytesIO()
        writer.write(merged)
        return merged.getvalue()
    except Exception:
        # Fallback: just return the main PDF if merge fails
        return main_bytes


# -----------------------------------------------------------------------------
# PARENT-FRIENDLY PDF
# -----------------------------------------------------------------------------
def build_pdf_parent(d) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, Image as RLImage
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from io import BytesIO

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=2.5*cm, rightMargin=2.5*cm,
                             topMargin=2.5*cm, bottomMargin=2.5*cm)

    INK   = colors.HexColor("#2A2520")
    BARK  = colors.HexColor("#8B7355")
    STONE = colors.HexColor("#6B6456")
    LINEN = colors.HexColor("#F0EBE1")
    WARM  = colors.HexColor("#FAF8F4")
    WARM2 = colors.HexColor("#F5F0E8")
    BORDER= colors.HexColor("#DDD8CE")
    SAGE  = colors.HexColor("#7A8A72")
    WHITE = colors.white
    SAGE_BG = colors.HexColor("#EEF2EC")

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sTitle  = S("PT", fontName="Helvetica-Bold",  fontSize=22, textColor=INK,
                      leading=28, alignment=TA_CENTER, spaceAfter=6)
    sSub    = S("PS", fontName="Helvetica",        fontSize=11, textColor=STONE,
                      leading=16, alignment=TA_CENTER, spaceAfter=4)
    sLead   = S("PL", fontName="Helvetica",        fontSize=11, textColor=INK,
                      leading=18, spaceAfter=8, alignment=TA_JUSTIFY)
    sSecHdr = S("PH", fontName="Helvetica-Bold",   fontSize=13, textColor=BARK,
                      leading=18, spaceBefore=14, spaceAfter=6)
    sBody   = S("PB", fontName="Helvetica",         fontSize=10.5, textColor=INK,
                      leading=17, spaceAfter=6, alignment=TA_JUSTIFY)
    sBullet = S("PBu",fontName="Helvetica",         fontSize=10.5, textColor=INK,
                      leading=17, leftIndent=14, spaceAfter=4)
    sEmph   = S("PE", fontName="Helvetica-Bold",    fontSize=10.5, textColor=BARK,
                      leading=17, spaceAfter=4)
    sSmall  = S("PSm",fontName="Helvetica",         fontSize=9,  textColor=STONE, leading=13)
    sFooter = S("PF", fontName="Helvetica-Oblique", fontSize=8,  textColor=STONE,
                      alignment=TA_CENTER)
    sBox    = S("PBx",fontName="Helvetica",         fontSize=10.5, textColor=INK,
                      leading=17, leftIndent=6, spaceAfter=4, alignment=TA_JUSTIFY)

    def hr(c=BARK, t=0.8):
        return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=6, spaceBefore=6)
    def sp(h=0.3):
        return Spacer(1, h*cm)

    today    = datetime.now().strftime("%d %B %Y")
    child    = d.get("child_name") or "Your child"
    nursery  = d.get("nursery_name") or "Nursery"
    therapist= d.get("therapist_name") or "the assigned behavioral therapist"
    dob_str  = d["date_of_birth"].strftime("%d %B %Y") if d.get("date_of_birth") else "—"
    age      = d.get("age", "—")
    group    = d.get("class_group", "—")
    start    = d["start_date"].strftime("%d %B %Y") if d.get("start_date") else "—"
    freq     = d.get("session_frequency", "—")
    spm      = str(d.get("sessions_per_month", "—"))
    pattern  = d.get("pattern", "")
    notes    = d.get("notes", "")
    all_behaviors = d.get("behaviors", []) + ([d["custom_behavior"]] if d.get("custom_behavior") else [])
    skills   = d.get("skills", [])
    footer_t = d.get("footer_text") or "Confidential — For family use."

    story = []

    # -- Header ----------------------------------------------------------------
    story += [
        Paragraph(f"Your Child's Support Plan", sTitle),
        Paragraph(f"{nursery} — Individual Behaviour Support Programme", sSub),
        sp(0.15), hr(INK, 1.5), sp(0.3),
    ]

    # Logo
    if d.get("logo_bytes"):
        try:
            img = RLImage(BytesIO(d["logo_bytes"]), width=3*cm, height=1.8*cm, kind="proportional")
            img.hAlign = "CENTER"
            story += [img, sp(0.2)]
        except Exception:
            pass

    # Warm intro
    story += [
        Paragraph(
            f"Dear Parent / Guardian,",
            S("PG", fontName="Helvetica-Bold", fontSize=11, textColor=INK, spaceAfter=6)),
        Paragraph(
            f"We are so glad to share this with you. This document has been prepared to keep you fully informed "
            f"about the individual support programme we have put in place for <b>{child}</b>. "
            f"It is written in plain language — no jargon — so that you can understand exactly what we are doing, "
            f"why we are doing it, and how you can be part of {child}'s journey.",
            sLead),
        Paragraph(
            f"Please know that this plan is a sign of our care and commitment, not a cause for worry. "
            f"Many children benefit enormously from a little extra, focused support during their early years. "
            f"We are here as partners every step of the way.",
            sLead),
        sp(0.2),
    ]

    # Child info table
    info_data = [
        [Paragraph("<b>Child</b>", sSmall),       Paragraph(child, sBody),
         Paragraph("<b>Date of Birth</b>", sSmall), Paragraph(dob_str, sBody)],
        [Paragraph("<b>Age</b>", sSmall),          Paragraph(age, sBody),
         Paragraph("<b>Class / Group</b>", sSmall), Paragraph(group, sBody)],
        [Paragraph("<b>Therapist</b>", sSmall),    Paragraph(therapist, sBody),
         Paragraph("<b>Programme Start</b>", sSmall), Paragraph(start, sBody)],
        [Paragraph("<b>Sessions / Month</b>", sSmall), Paragraph(spm, sBody),
         Paragraph("<b>Session Frequency</b>", sSmall), Paragraph(freq, sBody)],
    ]
    info_tbl = Table(info_data, colWidths=[3.5*cm, 5.5*cm, 3.5*cm, 4.0*cm])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), LINEN),
        ("BACKGROUND",    (2,0),(2,-1), LINEN),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WARM, WARM2, WARM, WARM2]),
        ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story += [info_tbl, sp(0.5)]

    # -- Section 1: What is this plan? ----------------------------------------
    story += [Paragraph("What Is This Support Plan?", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    story += [
        Paragraph(
            f"This is an <b>Individual Behaviour Support Plan</b> — a personalised programme designed specifically "
            f"for <b>{child}</b>. It brings together structured sessions, targeted skill-building, and close teamwork "
            f"between our team and your family.",
            sBody),
        Paragraph(
            f"<b>It is important to understand:</b> this plan is <i>not</i> a diagnosis. It does not mean something "
            f"is 'wrong' with {child}. It simply means we have noticed some areas where a little extra support "
            f"could make a big difference — and we want to provide that support in the most effective way possible.",
            sBody),
        sp(0.2),
    ]

    # -- Section 2: What behaviors are we focusing on? -------------------------
    story += [Paragraph("What Are We Working On?", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    story += [
        Paragraph(
            f"Our team has observed the following behaviours that we would like to support {child} with. "
            f"Please remember — these behaviours are <i>not</i> 'bad behaviour'. They are {child}'s way of telling "
            f"us that something feels hard right now. Our job is to help build the skills to handle those "
            f"hard moments better:",
            sBody),
    ]
    if all_behaviors:
        for b in all_behaviors:
            story.append(Paragraph(f"• {b}", sBullet))
    else:
        story.append(Paragraph("• To be specified with the team.", sBullet))

    freq_label = d.get("frequency", "moderate").capitalize()
    int_label  = d.get("intensity", "moderate").capitalize()
    story += [
        sp(0.1),
        Paragraph(f"<b>How often:</b> {freq_label} &nbsp;&nbsp; <b>Intensity:</b> {int_label}", sBody),
    ]
    if pattern:
        story += [
            Paragraph(f"<b>When does it tend to happen?</b> {pattern}", sBody),
        ]
    story.append(sp(0.3))

    # -- Section 3: What skills are we building? -------------------------------
    story += [Paragraph("What Skills Are We Building?", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    story += [
        Paragraph(
            f"Our sessions are designed to build specific skills that will help {child} feel more confident, "
            f"calm, and capable. Here is what we are working on and what it means:",
            sBody),
    ]
    if skills:
        for sk in skills:
            if sk in SKILL_DETAILS:
                _, body = SKILL_DETAILS[sk]
                story += [
                    Paragraph(f"✦  {sk}", sEmph),
                    Paragraph(body, sBox),
                    sp(0.1),
                ]
    else:
        story.append(Paragraph("Skills will be confirmed in your first review meeting.", sBody))
    story.append(sp(0.2))

    # -- Section 4: What do sessions look like? --------------------------------
    story += [Paragraph("What Happens in a Session?", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    story += [
        Paragraph(
            f"Sessions are warm, playful, and child-led as much as possible. {child} will not know they are in "
            f"a 'behaviour session' — they will just be playing and connecting with {therapist}. "
            f"Sessions happen <b>{freq}</b> ({spm} times per month).",
            sBody),
    ]
    for t_, b_ in ACTIVITY_ITEMS:
        story.append(Paragraph(f"• <b>{t_}:</b> {b_}", sBullet))
    story.append(sp(0.3))

    # -- Section 5: How will we know it's working? ----------------------------
    story += [Paragraph("How Will We Know It's Working?", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    story += [
        Paragraph(
            f"Progress in early childhood is rarely a straight line — and that is completely normal. "
            f"We will look for small, meaningful signs that {child} is growing. Here is what to watch for:",
            sBody),
    ]
    for _, t_, b_ in PROGRESS_CARDS:
        story.append(Paragraph(f"• <b>{t_}:</b> {b_}", sBullet))
    story.append(sp(0.3))

    # -- Section 6: How can YOU help at home? ----------------------------------
    story += [Paragraph("How Can You Help at Home?", sSecHdr), hr(BARK, 0.5), sp(0.1)]

    home_tips = [
        ("Stay consistent", f"Try to use the same calm, non-reactive approach when {child} struggles at home as we use here. "
                            "Consistency between home and nursery is one of the most powerful things you can do."),
        ("Name feelings out loud", f"When {child} seems upset, try saying 'I can see you feel frustrated' rather than 'stop that'. "
                                   "This builds emotional vocabulary and makes feelings feel safe to express."),
        ("Celebrate the small wins", "Every time you notice {child} waiting, communicating, or calming down — even a little — "
                                     "name it and celebrate it. 'I noticed you took a deep breath — that was brilliant.'"),
        ("Tell us what you notice", "You know your child best. If you see something at home — a new trigger, a new strategy that "
                                    "works, or a breakthrough — please share it with us. Your insights shape the programme."),
        ("Keep routines predictable", "Many children who struggle with regulation find surprise and change very hard. "
                                      "Where possible, give {child} advance notice of any changes to routine."),
        ("Ask for support too", "This can feel a lot for parents. Please reach out to us any time you need guidance, "
                                "reassurance, or just a conversation."),
    ]
    for title, tip in home_tips:
        tip_filled = tip.replace("{child}", child)
        story.append(Paragraph(f"✦  <b>{title}</b>", sEmph))
        story.append(Paragraph(tip_filled, sBox))
        story.append(sp(0.1))
    story.append(sp(0.2))

    # -- Section 7: Who to contact --------------------------------------------
    story += [Paragraph("Your Team", sSecHdr), hr(BARK, 0.5), sp(0.1)]
    contact_data = [
        [Paragraph("<b>🏫 Nursery Team</b>", sEmph),
         Paragraph("<b>👩‍🏫 Behavioral Therapist</b>", sEmph),
         Paragraph("<b>👨‍👩‍👧 You — the Family</b>", sEmph)],
        [Paragraph("The nursery team will keep you informed and support the plan throughout the day.", sSmall),
         Paragraph(f"{therapist} leads the sessions and will provide you with regular written updates.", sSmall),
         Paragraph(f"Your voice matters. Regular review meetings will include your feedback and observations.", sSmall)],
    ]
    ct = Table(contact_data, colWidths=[5.2*cm, 5.2*cm, 5.2*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), INK),
        ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
        ("BACKGROUND",    (0,1),(-1,-1), LINEN),
        ("GRID",          (0,0),(-1,-1), 0.4, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story += [ct, sp(0.3)]

    # Notes
    if notes and notes.strip():
        story += [
            Paragraph("<b>Additional Notes from the Team</b>",
                      S("PN", fontName="Helvetica-Bold", fontSize=10.5, textColor=BARK,
                        spaceBefore=8, spaceAfter=4)),
            Paragraph(notes, sBody),
            sp(0.2),
        ]

    # Closing warm message
    closing_row = [[Paragraph(
        f"We are proud to support {child} and grateful to have you as a partner in this journey. "
        f"Together, we can make a real difference. Please don't hesitate to reach out — our door is always open.",
        S("PC2", fontName="Helvetica-Oblique", fontSize=10.5, textColor=STONE, leading=17, alignment=TA_CENTER))]]
    ct2 = Table(closing_row, colWidths=[15.5*cm])
    ct2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAGE_BG),
        ("BOX",           (0,0),(-1,-1), 0.5, SAGE),
        ("TOPPADDING",    (0,0),(-1,-1), 14),
        ("BOTTOMPADDING", (0,0),(-1,-1), 14),
        ("LEFTPADDING",   (0,0),(-1,-1), 16),
        ("RIGHTPADDING",  (0,0),(-1,-1), 16),
    ]))
    story += [ct2, sp(0.4)]

    # Footer
    story += [
        hr(STONE, 0.5),
        Paragraph(f"{footer_t}  |  Prepared for family of {child}  |  {today}  |  {nursery}", sFooter),
    ]

    def add_page_num(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(STONE)
        canvas_obj.drawRightString(A4[0] - 2.5*cm, 1.2*cm, f"Page {canvas_obj.getPageNumber()}")
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=add_page_num, onLaterPages=add_page_num)
    return buf.getvalue()



def build_docx(d) -> bytes:
    from docx import Document as DocxDoc
    from docx.shared import Pt, Cm, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    import copy

    doc = DocxDoc()

    # Page margins
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # -- Helpers ----------------------------------------------------------------
    def set_para_spacing(para, before=0, after=6, line=None):
        pPr = para._p.get_or_add_pPr()
        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:before"), str(before))
        spacing.set(qn("w:after"),  str(after))
        if line:
            spacing.set(qn("w:line"), str(line))
            spacing.set(qn("w:lineRule"), "auto")
        pPr.append(spacing)

    def add_heading(text, level=1):
        p = doc.add_paragraph()
        p.style = doc.styles["Normal"]
        run = p.add_run(text)
        run.bold = True
        run.font.color.rgb = RGBColor(0x8B, 0x73, 0x55) if level == 2 else RGBColor(0x2A, 0x25, 0x20)
        run.font.size = Pt(14 if level == 1 else 11)
        set_para_spacing(p, before=120, after=60)
        return p

    def add_section_header(num, title):
        p = doc.add_paragraph()
        p.style = doc.styles["Normal"]
        run_num = p.add_run(f"{num}. ")
        run_num.bold = True
        run_num.font.color.rgb = RGBColor(0x8B, 0x73, 0x55)
        run_num.font.size = Pt(11)
        run_title = p.add_run(title)
        run_title.bold = True
        run_title.font.color.rgb = RGBColor(0x2A, 0x25, 0x20)
        run_title.font.size = Pt(11)
        set_para_spacing(p, before=160, after=60)
        # Bottom border
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "8B7355")
        pBdr.append(bottom)
        pPr.append(pBdr)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.style = doc.styles["Normal"]
        run = p.add_run(text)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x3A, 0x35, 0x30)
        set_para_spacing(p, after=60, line=276)
        return p

    def add_bullet(title, body_text):
        p = doc.add_paragraph(style="List Bullet")
        r1 = p.add_run(f"{title}: ")
        r1.bold = True
        r1.font.size = Pt(10)
        r2 = p.add_run(body_text)
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0x3A, 0x35, 0x30)
        set_para_spacing(p, after=40)
        return p

    def add_spacer():
        p = doc.add_paragraph()
        set_para_spacing(p, after=40)
        return p

    def shade_cell(cell, hex_color):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  hex_color)
        tcPr.append(shd)

    def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcMar = OxmlElement("w:tcMar")
        for side, val in [("top",top),("bottom",bottom),("left",left),("right",right)]:
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:w"),    str(val))
            el.set(qn("w:type"), "dxa")
            tcMar.append(el)
        tcPr.append(tcMar)

    today  = datetime.now().strftime("%d %B %Y")
    start  = d["start_date"].strftime("%d %B %Y") if d.get("start_date") else "—"
    all_b  = d["behaviors"] + ([d["custom_behavior"]] if d.get("custom_behavior") else [])
    nursery = d.get("nursery_name") or "Nursery"
    child   = d.get("child_name")   or "—"
    footer_t = d.get("footer_text") or "Confidential — For internal and family use only."

    # -- Title -----------------------------------------------------------------
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Individual Behavior Support Plan")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(0x2A, 0x25, 0x20)
    set_para_spacing(t, after=40)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = sub.add_run(f"Developmental Support Programme — {nursery}")
    rs.font.size = Pt(10)
    rs.font.color.rgb = RGBColor(0x6B, 0x64, 0x56)
    rs.italic = True
    set_para_spacing(sub, after=100)

    # -- Info table -------------------------------------------------------------
    tbl = doc.add_table(rows=3, cols=4)
    tbl.style = "Table Grid"
    info_data = [
        ("Child Name", child,                      "Date",           today),
        ("Age",        d.get("age","—"),            "Class / Group",  d.get("class_group","—")),
        ("Start Date", start,                       "Sessions/month", str(d.get("sessions_per_month","—"))),
    ]
    col_w = [Cm(3.0), Cm(5.8), Cm(3.0), Cm(4.5)]
    for i, (l1, v1, l2, v2) in enumerate(info_data):
        row = tbl.rows[i]
        for j, (w, txt, is_label) in enumerate([(col_w[0],l1,True),(col_w[1],v1,False),
                                                  (col_w[2],l2,True),(col_w[3],v2,False)]):
            cell = row.cells[j]
            cell.width = w
            set_cell_margins(cell)
            shade_cell(cell, "F0EBE1" if is_label else "FAF8F4")
            p = cell.paragraphs[0]
            run = p.add_run(txt)
            run.bold = is_label
            run.font.size = Pt(9)
            if is_label:
                run.font.color.rgb = RGBColor(0x8B, 0x73, 0x55)

    add_spacer()

    # -- Section 1 — Purpose ----------------------------------------------------
    add_section_header(1, "Programme Purpose & Scope")
    add_body(f"This Individual Behavior Support Plan has been developed to provide structured, "
             f"evidence-informed support for {child}'s developmental needs. It is important to note that "
             f"this plan is not a diagnostic document, nor does it imply the presence of any clinical "
             f"condition or disorder.")
    add_body("The purpose of this programme is to build specific developmental skills — including "
             "emotional regulation, impulse control, frustration tolerance, and functional communication — "
             "within the safe, consistent, and nurturing environment of the nursery setting.")
    add_body("All interventions are grounded in a positive, strengths-based framework that emphasises "
             "the child's capacity for growth. Progress is expected to occur gradually and non-linearly.")
    add_spacer()

    # -- Section 2 — Behaviors -------------------------------------------------
    add_section_header(2, "Identified Behavioral Concerns")
    add_body("The following behaviors have been identified as current areas of focus:")
    if all_b:
        p = doc.add_paragraph()
        for b in all_b:
            r = p.add_run(f"  {b}  ")
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x6B, 0x64, 0x56)
        set_para_spacing(p, after=40)

    p_lv = doc.add_paragraph()
    r1 = p_lv.add_run("Frequency: ")
    r1.bold = True; r1.font.size = Pt(10)
    r2 = p_lv.add_run(d.get("frequency","—").capitalize() + "   ")
    r2.font.size = Pt(10)
    r3 = p_lv.add_run("Intensity: ")
    r3.bold = True; r3.font.size = Pt(10)
    r4 = p_lv.add_run(d.get("intensity","—").capitalize())
    r4.font.size = Pt(10)
    set_para_spacing(p_lv, after=40)

    if d.get("pattern"):
        p_pat = doc.add_paragraph()
        rp1 = p_pat.add_run("Recent Pattern / Context: ")
        rp1.bold = True; rp1.font.size = Pt(10)
        rp2 = p_pat.add_run(d["pattern"])
        rp2.font.size = Pt(10)
        set_para_spacing(p_pat, after=60)
    add_spacer()

    # -- Section 3 — Skills ----------------------------------------------------
    add_section_header(3, "Core Skills Targeted")
    add_body("The following skill areas have been selected as primary targets for this programme:")
    for s in d.get("skills", []):
        if s in SKILL_DETAILS:
            title, body_text = SKILL_DETAILS[s]
            p_sk = doc.add_paragraph()
            r_t = p_sk.add_run(f"{title}:  ")
            r_t.bold = True
            r_t.font.size = Pt(10)
            r_t.font.color.rgb = RGBColor(0x2A, 0x25, 0x20)
            r_b = p_sk.add_run(body_text)
            r_b.font.size = Pt(9.5)
            r_b.font.color.rgb = RGBColor(0x4A, 0x45, 0x40)
            # Light background shading via paragraph border
            pPr = p_sk._p.get_or_add_pPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"),  "clear")
            shd.set(qn("w:fill"), "F0EBE1")
            pPr.append(shd)
            ind = OxmlElement("w:ind")
            ind.set(qn("w:left"), "200")
            pPr.append(ind)
            set_para_spacing(p_sk, after=60, line=276)
    add_spacer()

    # -- Section 4 — Activities ------------------------------------------------
    add_section_header(4, "Session Activities")
    add_body("Sessions will incorporate structured, play-based, and reflective activities:")
    for t_, b_ in ACTIVITY_ITEMS:
        add_bullet(t_, b_)
    add_spacer()

    # -- Section 5 — Monitoring ------------------------------------------------
    add_section_header(5, "Session Monitoring Framework")
    mon_tbl = doc.add_table(rows=len(MONITORING_ROWS)+1, cols=2)
    mon_tbl.style = "Table Grid"
    hdr_cells = mon_tbl.rows[0].cells
    for i, txt in enumerate(["Monitoring Dimension", "What Is Recorded"]):
        shade_cell(hdr_cells[i], "2A2520")
        set_cell_margins(hdr_cells[i])
        p = hdr_cells[i].paragraphs[0]
        r = p.add_run(txt)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for ri, (d_, r_) in enumerate(MONITORING_ROWS):
        row = mon_tbl.rows[ri+1]
        fill = "FAF8F4" if ri % 2 == 0 else "F0EBE1"
        for ci, txt in enumerate([d_, r_]):
            cell = row.cells[ci]
            shade_cell(cell, fill)
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            run = p.add_run(txt)
            run.bold = (ci == 0)
            run.font.size = Pt(9.5)
    add_spacer()

    # -- Section 6 — Progress -------------------------------------------------
    add_section_header(6, "Indicators of Progress")
    add_body("The following indicators will be used as primary markers of meaningful progress:")
    for _, t_, b_ in PROGRESS_CARDS:
        add_bullet(t_, b_)
    add_spacer()

    # -- Section 7 — Collaboration ---------------------------------------------
    add_section_header(7, "Family & Team Collaboration")
    add_body("This programme operates on the understanding that meaningful and lasting developmental "
             "change occurs when the child's key environments are aligned in their approach and consistent "
             "in their response.")
    collab_items = [
        ("Nursery Team", "Teaching staff are briefed on programme goals and monitoring frameworks. "
                         "Fortnightly check-ins ensure responsiveness and fidelity to the plan."),
        ("Key Worker",   "The assigned key worker maintains session records and serves as primary liaison "
                         "between the programme and the classroom environment."),
        ("Family Partnership", "Parents receive regular written updates and recommended home reinforcement "
                               "strategies. Family input is actively valued and integral to all reviews."),
    ]
    for t_, b_ in collab_items:
        add_bullet(t_, b_)

    if d.get("notes") and d["notes"].strip():
        add_spacer()
        p_nt = doc.add_paragraph()
        r_nt = p_nt.add_run("Additional Notes:  ")
        r_nt.bold = True
        r_nt.font.size = Pt(10)
        r_nt.font.color.rgb = RGBColor(0x8B, 0x73, 0x55)
        r_nt2 = p_nt.add_run(d["notes"])
        r_nt2.font.size = Pt(10)
        set_para_spacing(p_nt, after=60)

    # -- Footer ----------------------------------------------------------------
    add_spacer()
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Horizontal rule via top border
    pPr = p_foot._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    top_el = OxmlElement("w:top")
    top_el.set(qn("w:val"),   "single")
    top_el.set(qn("w:sz"),    "4")
    top_el.set(qn("w:space"), "1")
    top_el.set(qn("w:color"), "DDD8CE")
    pBdr.append(top_el)
    pPr.append(pBdr)

    rf = p_foot.add_run(f"{footer_t}  |  Generated: {today}  |  {nursery}")
    rf.font.size = Pt(8)
    rf.italic = True
    rf.font.color.rgb = RGBColor(0x6B, 0x64, 0x56)
    set_para_spacing(p_foot, before=60)

    out = io.BytesIO()
    doc.save(out)
    return out.getvalue()


# -----------------------------------------------------------------------------
# SIDEBAR — FORM
# -----------------------------------------------------------------------------
def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.6rem;padding:0.5rem 0 1.2rem;">
            <div style="width:34px;height:34px;background:#2A2520;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1rem;color:#fff;">✦</div>
            <div>
                <div style="font-family:'Jost',sans-serif;font-size:1rem;font-weight:500;color:#2A2520;line-height:1.2;">
                    Plan Builder</div>
                <div style="font-size:0.68rem;color:#6B6456;">Individual Support Programme</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Templates
        with st.expander("📋 Load a Template", expanded=False):
            if st.button("Transition Difficulties", use_container_width=True, key="tpl1"):
                st.session_state.tpl = "transition"
            if st.button("Aggression Toward Peers", use_container_width=True, key="tpl2"):
                st.session_state.tpl = "aggression"

        st.markdown("### Child Information")
        child_name  = st.text_input("Child Name *", placeholder="e.g. Liam Hassan",
                                     key="child_name")
        dob         = st.date_input("Date of Birth", value=date(date.today().year - 3, date.today().month, 1),
                                     key="date_of_birth", min_value=date(date.today().year-12,1,1),
                                     max_value=date.today())
        # Auto-calculate age
        today_d = date.today()
        years = today_d.year - dob.year - ((today_d.month, today_d.day) < (dob.month, dob.day))
        months_total = (today_d.year * 12 + today_d.month) - (dob.year * 12 + dob.month)
        months = months_total % 12
        age = f"{years} year{'s' if years != 1 else ''} {months} month{'s' if months != 1 else ''}"
        st.caption(f"🎂 Age: **{age}**")

        class_group = st.text_input("Class / Group", placeholder="e.g. Sunflower Group",
                                     key="class_group")
        therapist_name = st.text_input("Behavioral Therapist Name", placeholder="e.g. Sara Ahmed",
                                        key="therapist_name")
        start_date  = st.date_input("Programme Start Date", value=date.today(), key="start_date")

        st.markdown("### Behavioral Concerns")
        behaviors = st.multiselect(
            "Main behaviors",
            BEHAVIOR_OPTIONS,
            key="behaviors",
            placeholder="Select all that apply…",
        )
        custom_behavior = st.text_input("Custom behavior (optional)",
                                         placeholder="Describe a specific behavior…",
                                         key="custom_behavior")

        col1, col2 = st.columns(2)
        with col1:
            frequency = st.selectbox("Frequency", ["low","moderate","high"],
                                      index=1, key="frequency")
        with col2:
            intensity = st.selectbox("Intensity", ["low","moderate","high"],
                                      index=1, key="intensity")

        pattern = st.text_area("Recent pattern / context",
                                placeholder="e.g. Behaviors occur primarily during transitions…",
                                key="pattern", height=80)

        st.markdown("### Skills to Target")
        skills = []
        for s in SKILL_DETAILS.keys():
            if st.checkbox(s, key=f"skill_{s}"):
                skills.append(s)

        st.markdown("### Programme Details")
        col3, col4 = st.columns(2)
        with col3:
            sessions_per_month = st.number_input("Sessions / month", min_value=1,
                                                   max_value=31, value=4,
                                                   key="sessions_per_month")
        with col4:
            session_frequency = st.selectbox(
                "Frequency",
                ["Once per week","Twice per week","Three times per week",
                 "Daily","Biweekly","As needed"],
                key="session_frequency",
            )
        notes = st.text_area("Additional notes (optional)",
                              placeholder="Context, preferences, observations…",
                              key="notes", height=80)

        st.markdown("### Nursery Information")
        nursery_name = st.text_input("Nursery Name", placeholder="e.g. Little Stars Nursery",
                                      key="nursery_name")
        logo_file    = st.file_uploader("Logo (PNG / JPG)", type=["png","jpg","jpeg"],
                                         key="logo_file")
        footer_text  = st.text_input("Footer text (optional)",
                                      placeholder="Confidential — For internal use only.",
                                      key="footer_text")

        logo_bytes = None
        if logo_file:
            logo_bytes = logo_file.read()

        # Apply template if requested
        if st.session_state.get("tpl"):
            tpl = st.session_state.pop("tpl")
            if tpl == "transition":
                st.session_state.behaviors      = ["Refusing transitions","Tantrums / meltdowns","Dropping to the floor"]
                st.session_state.frequency      = "high"
                st.session_state.intensity      = "moderate"
                st.session_state.pattern        = "Behaviors occur primarily during transitions between activities and at pickup time."
                st.session_state["skill_Emotional Regulation"] = True
                st.session_state["skill_Frustration Tolerance"] = True
                st.session_state["skill_Communication Skills"] = True
                st.rerun()
            elif tpl == "aggression":
                st.session_state.behaviors      = ["Hitting / kicking others","Throwing objects","Verbal aggression"]
                st.session_state.frequency      = "moderate"
                st.session_state.intensity      = "high"
                st.session_state.pattern        = "Most incidents occur during unstructured play, particularly when sharing is required."
                st.session_state["skill_Impulse Control"] = True
                st.session_state["skill_Social Skills"] = True
                st.session_state["skill_Frustration Tolerance"] = True
                st.rerun()

        return {
            "child_name":        child_name,
            "date_of_birth":     dob,
            "age":               age,
            "class_group":       class_group,
            "therapist_name":    therapist_name,
            "start_date":        start_date,
            "behaviors":         behaviors,
            "custom_behavior":   custom_behavior,
            "frequency":         frequency,
            "intensity":         intensity,
            "pattern":           pattern,
            "skills":            skills,
            "sessions_per_month": sessions_per_month,
            "session_frequency": session_frequency,
            "notes":             notes,
            "nursery_name":      nursery_name,
            "logo_bytes":        logo_bytes,
            "footer_text":       footer_text,
        }


# -----------------------------------------------------------------------------
# ACCESS CODE GATE
# -----------------------------------------------------------------------------

def get_valid_codes() -> list:
    """
    Load access codes from st.secrets.
    Expected secrets.toml entry:
        ACCESS_CODES = "CODE1,CODE2,CODE3"
    Returns a list of stripped uppercase codes.
    """
    try:
        raw = st.secrets["ACCESS_CODES"]
        return [c.strip().upper() for c in raw.split(",") if c.strip()]
    except Exception:
        return []


def render_login_screen():
    """
    Full-page login screen shown to unauthenticated users.
    Returns True if the user just entered a valid code (triggers rerun).
    """
    st.markdown("""
    <style>
    /* Hide sidebar entirely on login screen */
    section[data-testid="stSidebar"] { display: none !important; }
    .main .block-container {
        max-width: 480px !important;
        margin: 0 auto !important;
        padding-top: 8vh !important;
    }

    .login-wrap {
        background: #fff;
        border: 1px solid #DDD8CE;
        border-radius: 16px;
        padding: 3rem 2.5rem 2.5rem;
        box-shadow: 0 8px 40px rgba(42,37,32,0.10);
        text-align: center;
    }
    .login-mark {
        width: 52px; height: 52px;
        background: #2A2520; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; color: #fff;
        margin: 0 auto 1.2rem;
    }
    .login-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.75rem; font-weight: 400;
        color: #2A2520; margin-bottom: 0.4rem;
        line-height: 1.2;
    }
    .login-sub {
        font-size: 0.85rem; color: #6B6456;
        margin-bottom: 2rem; line-height: 1.6;
    }
    .login-error {
        background: #FAECE8; border-radius: 8px;
        padding: 0.6rem 1rem; font-size: 0.83rem;
        color: #8A3A2A; margin-top: 0.75rem;
    }
    .login-footer {
        font-size: 0.72rem; color: #B09A7A;
        margin-top: 1.5rem; line-height: 1.5;
    }
    </style>

    <div class="login-wrap">
        <div class="login-mark">✦</div>
        <div class="login-title">Behavior Plan Builder</div>
        <div class="login-sub">
            This tool is for authorised nursery staff only.<br>
            Please enter your access code to continue.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # The input sits outside the HTML block so Streamlit renders it properly
    code_input = st.text_input(
        "Access Code",
        placeholder="Enter your code…",
        type="password",
        label_visibility="collapsed",
        key="access_code_input",
    )

    btn = st.button("Enter →", use_container_width=True, key="access_code_btn")

    if btn or (code_input and code_input.endswith("\n")):
        valid_codes = get_valid_codes()
        if not valid_codes:
            # No codes configured — fail open with a warning (dev mode)
            st.warning("No ACCESS_CODES found in secrets. Add them to enable access control.")
            st.session_state.authenticated = True
            st.rerun()
        elif code_input.strip().upper() in valid_codes:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown(
                '<div class="login-error">⚠  Incorrect access code. Please try again.</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="login-footer">Contact your administrator if you need an access code.</div>',
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main():
    inject_styles()

    # -- Access gate -----------------------------------------------------------
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        render_login_screen()
        st.stop()   # Nothing below renders until authenticated

    # Session state
    if "tpl" not in st.session_state:
        st.session_state.tpl = None

    # App header
    st.markdown("""
    <div class="app-header">
        <div class="app-header-mark">✦</div>
        <div>
            <div class="app-header-title">Individual Behavior Support Plan Generator</div>
            <div class="app-header-sub">Fill in the sidebar → preview updates live → export Staff PDF or Parent PDF</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Collect form data from sidebar
    d = render_sidebar()

    # -- Live preview ----------------------------------------------------------
    if d["child_name"].strip():
        st.markdown(render_html_preview(d), unsafe_allow_html=True)

        # Export section
        st.markdown("""
        <div class="export-box">
            <div class="export-title">Export Documents</div>
        </div>
        """, unsafe_allow_html=True)

        col_pdf, col_parent = st.columns(2)

        with col_pdf:
            try:
                pdf_bytes = build_pdf_staff(d)
                filename_pdf = f"BehaviorPlan_Staff_{d['child_name'].replace(' ','_')}.pdf"
                st.download_button(
                    label="⬇  Staff PDF (+ Activities)",
                    data=pdf_bytes,
                    file_name=filename_pdf,
                    mime="application/pdf",
                    use_container_width=True,
                    help="Full professional report with suggested behavioral activities for sessions",
                )
            except Exception as e:
                st.error(f"Staff PDF error: {e}")

        with col_parent:
            try:
                parent_bytes = build_pdf_parent(d)
                filename_parent = f"BehaviorPlan_Parent_{d['child_name'].replace(' ','_')}.pdf"
                st.download_button(
                    label="⬇  Parent-Friendly PDF",
                    data=parent_bytes,
                    file_name=filename_parent,
                    mime="application/pdf",
                    use_container_width=True,
                    help="Warm, clear summary written for parents — no jargon",
                )
            except Exception as e:
                st.error(f"Parent PDF error: {e}")

    else:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    height:55vh;gap:1rem;opacity:0.5;">
            <div style="font-size:3rem;">✦</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:400;
                        color:#2A2520;">Your plan will appear here</div>
            <div style="font-size:0.85rem;color:#6B6456;">Enter a child name in the sidebar to begin</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
