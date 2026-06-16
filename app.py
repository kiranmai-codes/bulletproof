import streamlit as st
import requests
import json
import os
from datetime import date
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bulletproof — AI PRD Generator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DEFAULT API KEY
# Loaded from Streamlit secrets (deploy) or a
# local .env / environment variable (local dev).
# Users can still override via the sidebar.
# ─────────────────────────────────────────────
def _load_default_key() -> str:
    """Return the server-side API key without exposing it in source code."""
    # 1. Streamlit Cloud secrets (preferred for deployment)
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    # 2. Environment variable (local dev / Docker)
    return os.environ.get("OPENROUTER_API_KEY", "")

DEFAULT_API_KEY = _load_default_key()

# ─────────────────────────────────────────────
# MASTER SYSTEM PROMPT  (synthesized from Apple
# AirPods PRD · Jimmy Rodriguez Notion Template
# · Tasklight Detailed PRD · Gaurav Oberoi Guide)
# ─────────────────────────────────────────────
MASTER_SYSTEM_PROMPT = f"""You are a Principal Product Manager at a top-tier tech company with 15+ years shipping products used by millions. You write PRDs the way the best PMs in the world do — grounded in real evidence, obsessively customer-centric, specific enough for engineers to build from, and short enough that stakeholders actually read them.

You have internalized three schools of PRD writing:
1. The Apple school — requirements are numbered, prioritized (P1–P10), and testable. Every requirement is a falsifiable statement: "The product SHALL [do X]." Sections include Aspects (Design, Functionality, Interactivity, Customization), regulatory constraints, and a competitive analysis mindset.
2. The Modern PM school (Jimmy Rodriguez / Notion-style) — outcome-driven, AI-ready, structured around Problem Alignment → Solution → Scope → Delivery. UX principles are explicit. Success metrics are outcome-based, not output-based.
3. The Startup PM school (Gaurav Oberoi) — specs are code for human brains. Every word earns its place. Brevity forces clarity. Think like an engineer: address edge cases before the developer finds them.

When given feature bullets, a product type, and a target user, you produce a PRD that synthesizes all three schools. You never write vague requirements. You never list vanity metrics. You never leave open questions empty.

Today's date: {date.today().strftime("%B %d, %Y")}

---

## OUTPUT FORMAT

Generate the PRD in this exact Markdown structure. Do not deviate from section names or order.

---

# [PRD] {{Feature Name}} — {{Product Type}}

**PM:** [inferred from context or "TBD"]
**Status:** Draft v1.0
**Last Updated:** {date.today().strftime("%B %d, %Y")}
**Confidence:** [High / Medium / Low — your honest assessment of how complete this PRD is given the input]

---

## 1. Problem Alignment

### The Problem
Write 2–4 sentences. State the customer problem in plain language. Explain why it matters to the customer AND the business. Avoid symptoms — name the root cause. Ground it in evidence or behavioral patterns when possible.

### Why Now
1–3 bullets. What changed? Market shift, strategic priority, cost of delay, competitive pressure? Be time-bound and specific. Never repeat the problem statement here.

### Background & Evidence
List real evidence types (even if placeholder):
- **Customer signal:** [interviews, support tickets, survey data]
- **Quantitative data:** [usage metric, conversion rate, churn signal]
- **Competitive context:** [what competitors do, what gap exists]
- **Strategic fit:** [how this maps to company priority]

---

## 2. Solution Summary

One clear paragraph. Describe the WHAT and the WHY of the approach — not the HOW. Must be explainable in under 60 seconds. Must map directly back to the problem above. Do not turn this into a feature list.

### Target Users

| Role | Description | Included? |
|------|-------------|-----------|
| Primary | [Job title / persona, core need] | ✅ Yes |
| Secondary | [Job title / persona, adjacent need] | ✅ Yes |
| Explicitly not for | [Who this doesn't serve] | ❌ No |

### UX & Design Principles
List exactly 3–5 principles. Each must be directive enough to resolve a real design tradeoff. Not "user-friendly" — that's meaningless. Format: **[Principle Name]:** one sentence on what it means in practice.

### Definition of Success

| Metric | Baseline | Target | Timeframe | Type |
|--------|----------|--------|-----------|------|
| [Primary outcome metric] | [current #] | [goal #] | [by when] | Customer outcome |
| [Secondary metric] | [current #] | [goal #] | [by when] | Business metric |
| [Guardrail metric] | [current #] | [must not drop below] | [ongoing] | Guardrail |

**Primary metric** (the one number that defines success): [name it explicitly]

---

## 3. Scope & Capabilities

**TL;DR scope statement:** One paragraph. What is in this initiative. What is explicitly not. Write it like you're drawing a fence.

### Key Capabilities

List 4–8 outcome-based capability statements. No UI details. No technical specs. Each one maps to user value and is testable.
Format: "The system must allow [user type] to [action] so that [outcome]."

### In-Scope: User Stories

Prioritized. Use real personas, not generic "user." Format: **As a [persona], I want to [action], so that [outcome].** Include acceptance criteria for P0 stories.

**P0 — Must Ship**
1. As a [persona], I want to [...], so that [...].
   - ✅ Acceptance: [specific, testable condition]

**P1 — Should Ship**
2. As a [persona], I want to [...], so that [...].

**P2 — Nice to Have**
3. As a [persona], I want to [...], so that [...].

### Out of Scope

| Excluded Feature | Why Deferred |
|-----------------|--------------|
| [Feature] | [Reason: saves scope, different user, v2, etc.] |

---

## 4. Detailed Requirements

> This section follows the Apple PRD school. Requirements are numbered, prioritized P1–P10 (P10 = highest priority / must-have), and written as falsifiable SHALL statements.

### 4.1 Core Functionality
- **4.1.1** The product SHALL [specific, testable requirement]. *(P10)*

### 4.2 UX & Interaction
- **4.2.1** The product SHALL [specific, testable requirement]. *(P9)*

### 4.3 Performance & Reliability
- **4.3.1** The product SHALL [specific, testable requirement]. *(P8)*

### 4.4 Security & Compliance *(if applicable)*
- **4.4.1** The product SHALL [specific, testable requirement]. *(P7)*

> Priority scale: P10 = non-negotiable / P7–9 = core / P4–6 = important / P1–3 = nice-to-have

---

## 5. Delivery, Risks & Open Questions

### Release Plan

| Phase | Name | What Ships | Gate Criteria |
|-------|------|------------|---------------|
| Alpha | Internal | [core capability, internal only] | [specific condition to advance] |
| Beta | Closed | [+ what's added] | [specific condition to advance] |
| GA | General Availability | [full scope] | [primary metric hit] |

**Experiment plan:** [Will this be A/B tested? What's the holdback %? How long?]

### Constraints & Assumptions

**Constraints** (hard limits that shape the solution):
- Technical: [e.g. must work within existing auth system, no new infra]
- Legal/Compliance: [e.g. GDPR, specific regulation]
- Resource: [e.g. 1 engineer, 6-week timeline]
- Platform: [e.g. web only v1, mobile deferred]

**Assumptions** (things we're betting on that could be wrong):
- [Assumption 1 — what happens to this PRD if this assumption is wrong?]
- [Assumption 2]

### Open Questions & Risks

| # | Question / Risk | Owner | Resolution Path | Due |
|---|----------------|-------|-----------------|-----|
| 1 | [Unresolved question that blocks design or build] | [Name/team] | [How will this get answered] | [Date] |
| 2 | [Risk: what could go wrong + mitigation] | [Name/team] | [Mitigation] | [Date] |
| 3 | [Dependency on another team or system] | [Name/team] | [How tracked] | [Date] |

---

## 6. Appendix

### Competitive Landscape *(include when relevant)*
Brief table or bullets comparing how top 3–5 competitors handle this problem.

### Milestones
| Milestone | Date |
|-----------|------|
| Spec review complete | [date] |
| Design handoff | [date] |
| Engineering kickoff | [date] |
| Alpha ready | [date] |
| Beta launch | [date] |
| GA / planned release | [date] |

### Glossary *(include when using technical or domain-specific terms)*
| Term | Definition |
|------|------------|
| [Term] | [Plain-English definition] |

---

## RULES YOU MUST FOLLOW

1. **Never write a vague requirement.** "The product should be fast" is not a requirement. "The product SHALL load in under 1.5 seconds on a 4G connection" is.
2. **Never use vanity metrics.** "10,000 users" is not a success metric. "% of users who complete the core workflow within their first session" is.
3. **Never leave Open Questions empty.** If you don't know what the open questions are, that IS the open question.
4. **Calibrate depth to input quality.** If the feature bullets are sparse, say so in the Confidence field and flag which sections need more input. Do not hallucinate specifics.
5. **Acceptance criteria for every P0 story.** No exceptions. Engineers cannot build to a story without knowing what "done" looks like.
6. **The Out of Scope list must anticipate stakeholder asks.** Think about what a VP, designer, or engineer will ask for that's not included — and explicitly call it out.
7. **Write for two audiences simultaneously:** (a) a non-technical stakeholder who needs the 60-second version, and (b) an engineer who needs enough detail to estimate.
8. **Tailor every PRD to its product type.** A B2B SaaS PRD has different success metrics than a Consumer App or AI Feature.
9. **The title format is non-negotiable:** [PRD] Description of Initiative — never a code name, never vague.

---

## PRODUCT TYPE CALIBRATION

**B2B SaaS:** Lead metrics = activation rate, seat expansion, NRR, support ticket deflection. Key constraints = SSO, role-based access, audit logs, SLAs, security compliance. Out of scope anchors = mobile app, CSV bulk import, enterprise-only features.

**Consumer App:** Lead metrics = D1/D7/D30 retention, sharing/virality rate, task completion, session depth. Key constraints = app store guidelines, offline support, push notification limits. Out of scope anchors = web version, enterprise features, API access.

**Marketplace:** Lead metrics = GMV, take rate, liquidity (supply/demand match rate), repeat purchase. Two-sided constraints = trust & safety, payment processing, dispute resolution. Out of scope anchors = white-label, international expansion, physical fulfillment.

**AI Feature:** Lead metrics = task completion rate, AI acceptance rate (vs. override rate), time-to-value vs. manual baseline, trust score. Key constraints = latency budget, model cost per call, fallback behavior, user explainability. Out of scope anchors = fine-tuning, on-device inference, multi-modal input.

**Internal Tool:** Lead metrics = adoption rate among target team, task time reduction, error rate reduction. Key constraints = existing auth/infra, no new vendor procurement, works in current stack. Out of scope anchors = external user access, mobile, analytics dashboard.

**API / Developer Tool:** Lead metrics = time-to-first-API-call, weekly active developers, SDK adoption rate, error rate in integration. Key constraints = backward compatibility, versioning strategy, rate limits. Out of scope anchors = GUI/dashboard, non-developer users, managed hosting.
"""

# ─────────────────────────────────────────────
# FREE MODELS ON OPENROUTER
# ─────────────────────────────────────────────
# Single default model — no selector shown to users
DEFAULT_MODEL = "openrouter/free"

PRODUCT_TYPES = [
    "B2B SaaS",
    "Consumer App",
    "Marketplace",
    "AI Feature",
    "Internal Tool",
    "API / Developer Tool",
]

SAMPLE_BULLETS = {
    "B2B SaaS": """- Team members need to invite colleagues to the workspace
- Role-based permissions: Admin, Editor, Viewer
- Audit log of all user actions with timestamps
- SSO integration with Google and Okta
- Admin dashboard showing usage analytics per seat
- Bulk invite via CSV upload
- Pending invite management with resend/revoke""",

    "Consumer App": """- Users can save recipes from any website with one click
- Automatic ingredient scaling based on servings
- Auto-generate shopping list from selected recipes
- Meal planning calendar (weekly view)
- Share recipes with friends via link
- Offline access to saved recipes
- Nutritional info per recipe""",

    "Marketplace": """- Sellers can list products with photos, price, and description
- Buyers can filter by category, price range, and location
- In-app messaging between buyer and seller
- Escrow payment held until buyer confirms receipt
- Seller ratings and review system
- Dispute resolution flow for failed transactions
- Push notifications for new messages and order updates""",

    "AI Feature": """- AI writing assistant embedded in the document editor
- Real-time completions as the user types
- Rewrite selected text in different tones (formal, casual, concise)
- Summarize long documents into key bullets
- Detect and flag inconsistent terminology across the doc
- Works with offline fallback to a smaller model
- User can accept, reject, or edit any AI suggestion""",

    "Internal Tool": """- Ops team can submit IT requests via a form
- Auto-routing to the correct team based on request type
- SLA tracking with escalation alerts
- Requestor gets real-time status updates via Slack
- Admins can manage team capacity and reassign tickets
- Monthly reports on resolution time and ticket volume
- Integration with existing Jira instance""",

    "API / Developer Tool": """- REST API for sending transactional emails
- SDKs for Python, Node.js, and Ruby
- Webhook support for delivery, open, and click events
- Dashboard showing send volume, delivery rate, bounce rate
- API key management with scoped permissions
- Sandbox mode for testing without sending real emails
- Rate limiting with clear error messages and retry guidance""",
}

# ─────────────────────────────────────────────
# CUSTOM CSS  — Bulletproof Design System
# Palette:
#   Background  #F7F4EF  warm off-white
#   Surface     #FFFFFF  pure white cards
#   Sidebar     #1C1F2E  deep navy
#   Ink         #1A1D2E  near-black text
#   Muted       #6B7280  grey body text
#   Accent      #E85D26  burnt orange (the bullet)
#   Accent2     #2563EB  electric blue (links/tags)
#   Border      #E5E2DB  warm hairline
#   Success     #16A34A  green for status
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Lora:ital,wght@0,600;1,400&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F7F4EF !important; color: #1A1D2E; }
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 1380px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #1C1F2E !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.12);
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] label { color: #94A3B8 !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #94A3B8 !important; font-size: 0.8rem !important; }
[data-testid="stSidebar"] hr { border-color: #2D3148 !important; margin: 0.8rem 0 !important; }
[data-testid="stSidebar"] small { color: #64748B !important; }

/* Sidebar inputs */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextArea textarea {
    background-color: #252840 !important;
    border: 1px solid #2D3148 !important;
    color: #F1F5F9 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #E85D26 !important;
    box-shadow: 0 0 0 2px rgba(232,93,38,0.2) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #252840 !important;
    border: 1px solid #2D3148 !important;
    color: #F1F5F9 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #252840 !important;
    border: 1px solid #2D3148 !important;
    color: #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2D3148 !important;
    border-color: #E85D26 !important;
    color: #F1F5F9 !important;
}

/* ── Top nav bar ── */
.bp-topbar {
    background: #1C1F2E;
    padding: 0 2rem;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 0 rgba(255,255,255,0.06);
}
.bp-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.bp-logo-icon {
    width: 30px; height: 30px;
    background: #E85D26;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 15px; color: white;
}
.bp-logo-text {
    font-weight: 800;
    font-size: 1rem;
    color: #F1F5F9;
    letter-spacing: -0.02em;
}
.bp-logo-sub {
    font-size: 0.72rem;
    color: #64748B;
    margin-top: 1px;
}
.bp-nav-pills {
    display: flex;
    gap: 8px;
    align-items: center;
}
.bp-pill {
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: 1px solid;
}
.bp-pill-orange { background: rgba(232,93,38,0.12); color: #E85D26; border-color: rgba(232,93,38,0.25); }
.bp-pill-blue   { background: rgba(37,99,235,0.12); color: #60A5FA; border-color: rgba(37,99,235,0.25); }
.bp-pill-grey   { background: rgba(255,255,255,0.06); color: #94A3B8; border-color: rgba(255,255,255,0.1); }

/* ── Section headers ── */
h1, h2, h3 { color: #1A1D2E !important; font-family: 'Inter', sans-serif !important; }
.bp-section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.bp-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E5E2DB;
}

/* ── Cards ── */
.bp-card {
    background: #FFFFFF;
    border: 1px solid #E5E2DB;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
}
.bp-card-inset {
    background: #F7F4EF;
    border: 1px solid #E5E2DB;
    border-radius: 10px;
    padding: 16px 18px;
}

/* ── Main inputs ── */
.stTextInput input, .stTextArea textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E5E2DB !important;
    color: #1A1D2E !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #E85D26 !important;
    box-shadow: 0 0 0 3px rgba(232,93,38,0.1) !important;
    outline: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #C4B9A8 !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: #6B7280 !important;
    margin-bottom: 4px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E5E2DB !important;
    color: #1A1D2E !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}

/* ── Primary button — the CTA ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #E85D26 0%, #C44A18 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 4px 12px rgba(232,93,38,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #F06A30 0%, #D45520 100%) !important;
    box-shadow: 0 6px 16px rgba(232,93,38,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(232,93,38,0.25) !important;
}

/* Secondary buttons */
.stButton > button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E5E2DB !important;
    color: #374151 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #E85D26 !important;
    color: #E85D26 !important;
    background: #FFF5F0 !important;
}

/* Download buttons */
.stDownloadButton > button {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E5E2DB !important;
    color: #374151 !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: #E85D26 !important;
    color: #E85D26 !important;
    background: #FFF5F0 !important;
    transform: translateY(-1px) !important;
}

/* ── Output card — the PRD viewer ── */
.output-card {
    background: #FFFFFF;
    border: 1px solid #E5E2DB;
    border-radius: 12px;
    padding: 28px 32px;
    min-height: 520px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    font-family: 'Inter', sans-serif;
}

/* PRD rendered markdown */
.output-card h1 {
    font-family: 'Lora', Georgia, serif !important;
    color: #1A1D2E !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #E85D26;
    padding-bottom: 10px;
    margin-bottom: 16px !important;
}
.output-card h2 {
    color: #E85D26 !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-top: 2rem !important;
    margin-bottom: 10px !important;
    display: flex;
    align-items: center;
    gap: 8px;
}
.output-card h2::before {
    content: '';
    display: inline-block;
    width: 4px; height: 14px;
    background: #E85D26;
    border-radius: 2px;
    flex-shrink: 0;
}
.output-card h3 {
    color: #1A1D2E !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    margin-top: 1.2rem !important;
    margin-bottom: 6px !important;
}
.output-card p {
    color: #374151 !important;
    font-size: 0.88rem !important;
    line-height: 1.75 !important;
    margin-bottom: 0.6rem !important;
}
.output-card li {
    color: #374151 !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    margin-bottom: 3px !important;
}
.output-card strong { color: #1A1D2E !important; font-weight: 600 !important; }
.output-card table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 0 0 1px #E5E2DB;
}
.output-card th {
    background: #F7F4EF !important;
    color: #6B7280 !important;
    padding: 8px 14px !important;
    border-bottom: 1px solid #E5E2DB !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    text-align: left !important;
}
.output-card td {
    color: #374151 !important;
    padding: 7px 14px !important;
    border-bottom: 1px solid #F3F0EA !important;
    font-size: 0.84rem !important;
}
.output-card tr:last-child td { border-bottom: none !important; }
.output-card blockquote {
    border-left: 3px solid #E85D26 !important;
    padding: 8px 16px !important;
    background: #FFF5F0 !important;
    border-radius: 0 6px 6px 0 !important;
    margin: 12px 0 !important;
    color: #9A3412 !important;
    font-size: 0.84rem !important;
}
.output-card code {
    background: #F3F0EA !important;
    color: #C44A18 !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    font-size: 0.83rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.output-card hr {
    border: none !important;
    border-top: 1px solid #E5E2DB !important;
    margin: 1.5rem 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1.5px solid #E5E2DB !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #9CA3AF !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border-radius: 0 !important;
    background: transparent !important;
    letter-spacing: 0.02em;
}
.stTabs [aria-selected="true"] {
    color: #E85D26 !important;
    border-bottom: 2px solid #E85D26 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    color: #6B7280 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    background: #F7F4EF !important;
    border-radius: 8px !important;
    border: 1px solid #E5E2DB !important;
}
.streamlit-expanderContent {
    background: #FAFAF8 !important;
    border: 1px solid #E5E2DB !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 8px !important;
    font-size: 0.83rem !important;
}
[data-testid="stAlert"] { border-radius: 8px !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #E85D26 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #F7F4EF; }
::-webkit-scrollbar-thumb { background: #D4CFC7; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #B5AFA7; }

/* ── Separator ── */
hr { border-color: #E5E2DB !important; margin: 1rem 0 !important; }

/* ── Caption / small text ── */
.stCaption, small { color: #9CA3AF !important; font-size: 0.75rem !important; }

/* ── Status pill ── */
.bp-status-ready {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F0FDF4; border: 1px solid #BBF7D0;
    color: #15803D; border-radius: 20px;
    padding: 3px 10px; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.bp-status-generating {
    display: inline-flex; align-items: center; gap: 5px;
    background: #FFF5F0; border: 1px solid #FED7AA;
    color: #C2410C; border-radius: 20px;
    padding: 3px 10px; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.bp-status-waiting {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F9FAFB; border: 1px solid #E5E7EB;
    color: #9CA3AF; border-radius: 20px;
    padding: 3px 10px; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.3} }
.bp-dot-live { animation: pulse-dot 1.2s ease-in-out infinite; }

/* ── Empty state ── */
.bp-empty {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 420px; text-align: center;
}
.bp-empty-icon {
    width: 56px; height: 56px;
    background: #F3F0EA; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; margin-bottom: 16px;
}
.bp-empty-title { color: #374151; font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; }
.bp-empty-sub { color: #9CA3AF; font-size: 0.82rem; line-height: 1.6; }

/* ── Word count / meta chips ── */
.bp-meta {
    display: inline-flex; align-items: center; gap: 4px;
    background: #F7F4EF; border: 1px solid #E5E2DB;
    color: #6B7280; border-radius: 6px;
    padding: 2px 8px; font-size: 0.72rem; font-weight: 500;
}

/* Remove Streamlit default top padding / decorations */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# OPENROUTER STREAMING CALL
# ─────────────────────────────────────────────
def call_openrouter_stream(api_key: str, model: str, user_message: str):
    """Generator: yields text chunks from OpenRouter streaming API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
        "HTTP-Referer": "https://bulletproof-prd.streamlit.app",
        "X-Title": "Bulletproof - AI PRD Generator",  # ASCII only - no em dash
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": MASTER_SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        "stream": True,
        "max_tokens": 4000,
        "temperature": 0.65,
    }
    # Explicitly encode as UTF-8 to avoid latin-1 codec errors from
    # special characters (em dashes, curly quotes, etc.) in the prompt.
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    with requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=body,
        stream=True,
        timeout=120,
    ) as resp:
        if resp.status_code != 200:
            err = resp.json()
            raise RuntimeError(
                err.get("error", {}).get("message", f"HTTP {resp.status_code}")
            )
        for raw in resp.iter_lines():
            if not raw:
                continue
            line = raw.decode("utf-8") if isinstance(raw, bytes) else raw
            if line.startswith("data: "):
                data = line[6:].strip()
                if data == "[DONE]":
                    return
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError):
                    continue


def call_openrouter_simple(api_key: str, model: str, user_message: str) -> str:
    """Non-streaming fallback for refinement calls."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
        "HTTP-Referer": "https://bulletproof-prd.streamlit.app",
        "X-Title": "Bulletproof - AI PRD Generator",  # ASCII only - no em dash
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": MASTER_SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        "max_tokens": 4000,
        "temperature": 0.5,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=body,
        timeout=120,
    )
    if resp.status_code != 200:
        err = resp.json()
        raise RuntimeError(
            err.get("error", {}).get("message", f"HTTP {resp.status_code}")
        )
    return resp.json()["choices"][0]["message"]["content"]


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "prd_output": "",
        "generating": False,
        "generation_time": 0.0,
        "token_estimate": 0,
        "history": [],          # list of {"title", "content", "type", "ts"}
        "error": "",
        "refine_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Brand ──
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:4px'>"
        "<div style='background:#00ff9d;color:#0d1117;width:32px;height:32px;"
        "border-radius:8px;display:flex;align-items:center;justify-content:center;"
        "font-weight:900;font-size:16px'>B</div>"
        "<span style='color:#e6edf3;font-weight:700;font-size:1.1rem'>Bulletproof</span>"
        "</div>"
        "<p style='color:#4a6741;font-size:0.75rem;margin-top:0;margin-bottom:12px'>"
        "Bullets → Production-ready PRDs</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("## ⚙️ Configuration")

    # ── API Key: user's key overrides default ──
    user_key_input = st.text_input(
        "Your OpenRouter API Key (optional)",
        type="password",
        placeholder="sk-or-v1-... (leave blank to use default)",
        help="Enter your own key to use your quota. Leave blank to use the shared default key.",
    )

    # Resolve which key to actually use
    api_key = user_key_input.strip() if user_key_input.strip() else DEFAULT_API_KEY

    # Show status indicator
    if user_key_input.strip():
        st.markdown(
            "<small style='color:#00ff9d'>✓ Using your API key</small>",
            unsafe_allow_html=True,
        )
    elif DEFAULT_API_KEY:
        st.markdown(
            "<small style='color:#7ee8a2'>✓ Using shared key — or add yours above for your own quota</small>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<small style='color:#ff7b7b'>⚠ No default key set. "
            "<a href='https://openrouter.ai/keys' style='color:#7ee8a2'>Get a free key →</a></small>",
            unsafe_allow_html=True,
        )

    selected_model = DEFAULT_MODEL

    st.markdown("---")
    st.markdown("### 📋 Product Details")

    product_type = st.selectbox("Product Type", PRODUCT_TYPES)

    target_user = st.text_input(
        "Target User",
        placeholder="e.g. startup founders, enterprise HR managers",
    )

    pm_name = st.text_input(
        "PM Name (optional)",
        placeholder="Your name",
    )

    st.markdown("---")
    st.markdown("### 📜 History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            tag = "🟢" if item["type"] == "generate" else "🔵"
            if st.button(
                f"{tag} {item['title'][:28]}…" if len(item['title']) > 28 else f"{tag} {item['title']}",
                key=f"hist_{i}",
                use_container_width=True,
            ):
                st.session_state.prd_output = item["content"]
                st.rerun()
    else:
        st.caption("Generated PRDs will appear here.")

    st.markdown("---")
    st.markdown(
        "<small style='color:#4a6741'>Powered by OpenRouter Free Tier · "
        "System prompt synthesized from Apple PRD, Notion Template & Gaurav Oberoi's spec guide</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────
col_header, col_badge = st.columns([4, 1])
with col_header:
    st.markdown(
        "<h1 style='color:#e6edf3;margin-bottom:0'>🛡️ Bulletproof</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#4a6741;margin-top:4px;font-size:0.85rem'>"
        "Feature bullets → Production-ready PRDs · Powered by free OpenRouter models</p>",
        unsafe_allow_html=True,
    )
with col_badge:
    st.markdown(
        "<div style='text-align:right;margin-top:12px'>"
        "<span style='background:#0d2818;border:1px solid #1e3a2f;color:#00ff9d;"
        "padding:4px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;"
        "letter-spacing:0.08em'>FREE TIER</span></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Two-column layout ──
left_col, right_col = st.columns([1, 1], gap="large")

# ─────────────────────────────────────────────
# LEFT: INPUT PANEL
# ─────────────────────────────────────────────
with left_col:
    st.markdown("### ✏️ Feature Input")

    tab_write, tab_sample = st.tabs(["Write your own", "Load sample"])

    with tab_write:
        feature_bullets = st.text_area(
            "Feature Bullets",
            height=280,
            placeholder=(
                "- Users can invite teammates via email\n"
                "- Role-based permissions (Admin, Editor, Viewer)\n"
                "- Audit log of all changes\n"
                "- SSO with Google / Okta\n"
                "- Usage dashboard for admins"
            ),
            label_visibility="collapsed",
        )

    with tab_sample:
        if st.button("Load sample for: " + product_type, use_container_width=True):
            # Write directly into the widget's own session-state key so the
            # text area actually shows the new value after rerun.
            st.session_state["sample_area"] = SAMPLE_BULLETS.get(product_type, "")
            st.rerun()
        sample_display = st.text_area(
            "Sample (editable)",
            height=240,
            label_visibility="collapsed",
            key="sample_area",
        )
        if sample_display:
            feature_bullets = sample_display

    # Additional context (collapsible)
    with st.expander("➕ Add more context (optional)"):
        problem_context = st.text_area(
            "Background / Evidence",
            height=80,
            placeholder="Any data, research, customer quotes, or competitive context you want the PRD to reference...",
        )
        constraints = st.text_area(
            "Known Constraints",
            height=70,
            placeholder="e.g. Web only v1, 2 engineers, must use existing auth system, GDPR applies...",
        )
        timeline = st.text_input(
            "Target Timeline",
            placeholder="e.g. Ship beta in 6 weeks, GA in Q3 2026",
        )

    st.markdown("---")

    # ── Generate button ──
    key_ready = bool(api_key and api_key != "YOUR_OPENROUTER_KEY_HERE")
    can_generate = bool(key_ready and feature_bullets and feature_bullets.strip())

    if st.button(
        "⚡ Generate PRD" if not st.session_state.generating else "⏳ Generating…",
        type="primary",
        disabled=st.session_state.generating or not can_generate,
    ):
        if not key_ready:
            st.error("No API key available. Add your OpenRouter key in the sidebar.")
        elif not feature_bullets.strip():
            st.error("Please enter some feature bullets first.")
        else:
            st.session_state.generating = True
            st.session_state.prd_output = ""
            st.session_state.error = ""
            st.rerun()

    if not key_ready:
        st.warning("⚠️ Add your OpenRouter API key in the sidebar to generate.")
    elif not feature_bullets:
        st.info("💡 Enter feature bullets above, then hit Generate PRD.")

    # ── Refine section (only when PRD exists) ──
    if st.session_state.prd_output:
        st.markdown("---")
        st.markdown("### 🔧 Refine PRD")
        refine_instruction = st.text_area(
            "What to improve?",
            height=80,
            placeholder=(
                "e.g. Make the success metrics more specific with baselines\n"
                "Add a competitive landscape section\n"
                "Rewrite Section 4 with stricter SHALL requirements"
            ),
        )
        if st.button("Apply Refinement", use_container_width=True):
            if refine_instruction.strip():
                st.session_state.refine_mode = True
                st.session_state.generating = True
                st.session_state["refine_instruction"] = refine_instruction
                st.rerun()


# ─────────────────────────────────────────────
# RIGHT: OUTPUT PANEL
# ─────────────────────────────────────────────
with right_col:
    st.markdown("### 📑 Generated PRD")

    # ── Status bar ──
    status_cols = st.columns([2, 1, 1])
    with status_cols[0]:
        if st.session_state.generating:
            st.markdown(
                "<span style='color:#00ff9d;font-size:0.8rem'>● GENERATING…</span>",
                unsafe_allow_html=True,
            )
        elif st.session_state.prd_output:
            st.markdown(
                "<span style='color:#00ff9d;font-size:0.8rem'>✓ PRD READY</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<span style='color:#4a6741;font-size:0.8rem'>○ WAITING</span>",
                unsafe_allow_html=True,
            )
    with status_cols[1]:
        if st.session_state.generation_time:
            st.caption(f"⏱ {st.session_state.generation_time:.1f}s")
    with status_cols[2]:
        if st.session_state.token_estimate:
            st.caption(f"~{st.session_state.token_estimate} words")

    # ── Generation logic ──
    if st.session_state.generating:
        try:
            if st.session_state.get("refine_mode"):
                # Refinement mode
                user_msg = f"""Here is the current PRD:

{st.session_state.prd_output}

---
Refinement instruction: {st.session_state.get('refine_instruction', '')}

Please apply the refinement and return the full updated PRD, keeping the same structure."""
            else:
                # Fresh generation
                pm_line = f"PM Name: {pm_name}" if pm_name else ""
                context_line = f"\nBackground / Evidence:\n{problem_context}" if problem_context else ""
                constraints_line = f"\nKnown Constraints: {constraints}" if constraints else ""
                timeline_line = f"\nTarget Timeline: {timeline}" if timeline else ""

                user_msg = f"""Generate a complete PRD for the following:

Product Type: {product_type}
Target User: {target_user or 'Not specified'}
{pm_line}
Feature Bullets:
{feature_bullets}
{context_line}
{constraints_line}
{timeline_line}

Follow the master PRD format exactly. Be specific, evidence-grounded, and engineer-ready."""

            # Stream output
            t_start = time.time()
            output_placeholder = st.empty()
            full_text = ""

            for chunk in call_openrouter_stream(api_key, selected_model, user_msg):
                full_text += chunk
                output_placeholder.markdown(
                    f"<div class='output-card'>{full_text}▌</div>",
                    unsafe_allow_html=True,
                )

            t_end = time.time()

            # Save to state
            st.session_state.prd_output = full_text
            st.session_state.generation_time = round(t_end - t_start, 1)
            st.session_state.token_estimate = len(full_text.split())

            # Save to history
            title_line = [l for l in full_text.split("\n") if l.strip().startswith("# [PRD]")]
            title = title_line[0].replace("# ", "") if title_line else f"{product_type} PRD"
            st.session_state.history.append({
                "title": title,
                "content": full_text,
                "type": "refine" if st.session_state.refine_mode else "generate",
                "ts": date.today().isoformat(),
            })

        except Exception as e:
            st.session_state.error = str(e)
        finally:
            st.session_state.generating = False
            st.session_state.refine_mode = False
            st.rerun()

    # ── Show error ──
    if st.session_state.error:
        st.error(f"❌ {st.session_state.error}")
        st.markdown(
            "**Common fixes:** Check your API key · Try a different model · "
            "Verify you have free credits at [openrouter.ai](https://openrouter.ai)"
        )

    # ── Show PRD output ──
    if st.session_state.prd_output and not st.session_state.generating:
        # Rendered tab + Raw tab
        out_tab1, out_tab2 = st.tabs(["📄 Rendered", "📝 Raw Markdown"])

        with out_tab1:
            st.markdown(
                f"<div class='output-card'>{st.session_state.prd_output}</div>",
                unsafe_allow_html=True,
            )

        with out_tab2:
            st.code(st.session_state.prd_output, language="markdown")

        # ── Export buttons ──
        st.markdown("---")
        exp_col1, exp_col2, exp_col3 = st.columns(3)

        with exp_col1:
            filename = f"PRD_{product_type.replace(' ', '_')}_{date.today().isoformat()}.md"
            st.download_button(
                label="⬇️ Download Markdown",
                data=st.session_state.prd_output,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )

        with exp_col2:
            # Notion-ready copy (same content, Notion imports .md perfectly)
            st.download_button(
                label="📋 Notion-ready .md",
                data=st.session_state.prd_output,
                file_name=filename.replace(".md", "_notion.md"),
                mime="text/markdown",
                use_container_width=True,
                help="Download and drag into Notion — it renders the full PRD automatically",
            )

        with exp_col3:
            # Plain text version
            import re
            plain = re.sub(r"[#*`|_>~]", "", st.session_state.prd_output)
            st.download_button(
                label="📃 Plain Text",
                data=plain,
                file_name=filename.replace(".md", ".txt"),
                mime="text/plain",
                use_container_width=True,
            )

        # ── Portfolio tip ──
        with st.expander("🎯 Portfolio Tip — Turn this into 3 PRD portfolio pieces"):
            st.markdown("""
**Step 1:** Generate PRDs for 3 different product types:
- **B2B SaaS** → e.g. Team invitation wizard
- **Consumer App** → e.g. Recipe saving and meal planning
- **AI Feature** → e.g. In-editor writing assistant

**Step 2:** Download each as Notion-ready `.md`

**Step 3:** Import into Notion → Share as public pages

**Step 4:** Add links to your resume:
> *"Built AI PRD generator · Generated 3 portfolio PRDs for B2B, Consumer & AI feature contexts"*

**Step 5 (optional):** Host the app on [Streamlit Community Cloud](https://streamlit.io/cloud) for free → add the live URL to your resume.
""")

    elif not st.session_state.prd_output and not st.session_state.generating:
        st.markdown(
            """<div class='output-card' style='display:flex;flex-direction:column;
            align-items:center;justify-content:center;min-height:420px;opacity:0.5'>
            <div style='font-size:3rem;margin-bottom:16px'>📄</div>
            <p style='color:#4a6741;text-align:center;line-height:1.8'>
            Enter feature bullets on the left<br>
            and hit <strong style='color:#7ee8a2'>⚡ Generate PRD</strong> to get started.
            </p>
            <p style='color:#374a33;font-size:0.78rem;text-align:center;margin-top:8px'>
            Uses master system prompt synthesized from<br>
            Apple PRD · Notion Template · Tasklight · Gaurav Oberoi
            </p>
            </div>""",
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
footer_cols = st.columns([1, 1, 1, 1])
with footer_cols[0]:
    st.markdown("<small style='color:#4a6741'>🛡️ Bulletproof · Free via OpenRouter</small>", unsafe_allow_html=True)
with footer_cols[1]:
    st.markdown("<small style='color:#4a6741'>📐 Apple · Notion · Tasklight PRD schemas</small>", unsafe_allow_html=True)
with footer_cols[2]:
    st.markdown("<small style='color:#4a6741'>📖 Gaurav Oberoi spec methodology</small>", unsafe_allow_html=True)
with footer_cols[3]:
    st.markdown(f"<small style='color:#374a33'>{date.today().strftime('%B %d, %Y')}</small>", unsafe_allow_html=True)