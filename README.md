# 🛡️ Bulletproof — AI PRD Generator

> Generate engineer-ready Product Requirement Documents in seconds, powered by LLMs via OpenRouter.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?logo=streamlit)
![OpenRouter](https://img.shields.io/badge/API-OpenRouter-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

Bulletproof takes a few feature bullets and a product type, then outputs a **complete, structured PRD** — the kind senior PMs write — in under 60 seconds.

The master system prompt synthesizes three battle-tested PRD schools:

| School | What it contributes |
|--------|---------------------|
| **Apple PRD** | Numbered, prioritized (`P1–P10`) SHALL requirements; testable acceptance criteria |
| **Modern PM / Notion-style** | Outcome-driven structure: Problem → Solution → Scope → Delivery |
| **Startup PM (Gaurav Oberoi)** | Radical brevity; specs as "code for human brains"; edge cases front-loaded |

---

## Features

- ⚡ **Streaming generation** — output appears word by word, no waiting for a full response
- 🔁 **Refine mode** — iterate on an existing PRD with a single instruction
- 📜 **PRD history** — session-level history of all generated documents
- 📥 **Export options** — Markdown download, Notion-ready `.md`, and plain text
- 🤖 **Model picker** — swap between any OpenRouter-hosted model (GPT-4o, Claude, Gemini, etc.)
- 🔑 **Bring your own key** — users can override the default key with their own OpenRouter API key

---

## Screenshots

<img width="1710" height="991" alt="Screenshot 2026-06-16 at 11 24 20 AM" src="https://github.com/user-attachments/assets/544cd6d2-bfda-4a0f-9b6e-81bf7996a29b" />


---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/bulletproof-prd.git
cd bulletproof-prd
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenRouter API key

**Option A — environment variable (recommended for local dev):**

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

**Option B — Streamlit secrets (recommended for deployment):**

Create `.streamlit/secrets.toml`:

```toml
OPENROUTER_API_KEY = "sk-or-v1-..."
```

**Option C — paste directly in the app sidebar** at runtime.

> ⚠️ Never commit your API key to version control. The `.gitignore` already excludes `.streamlit/secrets.toml`.

### 4. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select this repo.
3. Add your `OPENROUTER_API_KEY` under **Advanced settings → Secrets**.
4. Click **Deploy** — you get a public URL instantly.

---

## Project structure

```
bulletproof-prd/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## Configuration

| Setting | Where | Default |
|---------|-------|---------|
| Default API key | `DEFAULT_API_KEY` constant in `app.py` | Hardcoded (replace before deploy) |
| Default model | Sidebar model picker | `google/gemini-flash-1.5` |
| Streaming | `call_openrouter_stream()` | Enabled |

---

## PRD output structure

Every generated PRD follows this locked template:

```
1. Problem Alignment     — root cause, why now, evidence
2. Solution Summary      — what & why, target users, success metrics
3. Scope & Capabilities  — user stories (P0/P1/P2), out-of-scope table
4. Detailed Requirements — SHALL statements with P1–P10 priority
5. Delivery & Risks      — release phases, constraints, open questions
6. Appendix              — competitive landscape, milestones, glossary
```

---

## Sample output

See [`PRD_B2B_SaaS_2026-06-16.txt`](PRD_B2B_SaaS_2026-06-16.txt) for a full example — a Workspace Access & Governance Suite PRD covering RBAC, SSO, bulk CSV onboarding, and immutable audit logs.

---

## Contributing

PRs welcome. Areas that need work:

- [ ] PDF export (via `fpdf2` or `weasyprint`)
- [ ] Persistent history across sessions (SQLite or Supabase)
- [ ] SCIM / Azure AD template variants
- [ ] Multi-language PRD output

---

## License

MIT — use freely, attribution appreciated.

---

## Acknowledgements

Prompt methodology inspired by:
- Apple Hardware PRD format
- [Jimmy Rodriguez's Notion PRD template](https://www.notion.so)
- Tasklight detailed spec guidelines
- [Gaurav Oberoi's "Painless Functional Specs" guide](https://go.gauravobero.com/specs)
