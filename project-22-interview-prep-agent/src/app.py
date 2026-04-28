
from dotenv import load_dotenv
import os
load_dotenv(r'C:\Users\Gurveer\ds-portfolio\.env')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

import streamlit as st
import json
import sqlite3
import datetime
import pandas as pd
from openai import OpenAI

client = OpenAI()

# ── Question bank (abbreviated for app) ──────────────────────
questions = [
    {"domain": "machine_learning", "q": "Explain the bias-variance tradeoff.", 
     "rubric": ["defines bias/variance", "tradeoff relationship", "regularization", "practical example"]},
    {"domain": "sql_data_engineering", "q": "How do you optimize a slow SQL query on 100M rows?",
     "rubric": ["indexing", "query plan", "partitioning", "avoid SELECT *"]},
    {"domain": "ai_safety_alignment", "q": "Explain RLHF end to end.",
     "rubric": ["preference data", "reward model", "KL penalty", "PPO", "limitations"]},
    {"domain": "llm_agentic_systems", "q": "What is RAG and when is it better than fine-tuning?",
     "rubric": ["retrieval augmented generation", "knowledge cutoff", "cost", "dynamic knowledge"]},
    {"domain": "statistics_probability", "q": "How do you design an A/B test end to end?",
     "rubric": ["null hypothesis", "power analysis", "randomization", "practical vs statistical significance"]},
    {"domain": "mlops_production", "q": "Walk me through deploying an ML model to production.",
     "rubric": ["serialization", "API serving", "containerization", "CI/CD", "monitoring"]},
    {"domain": "finance_quantitative", "q": "Explain Black-Scholes-Merton from first principles.",
     "rubric": ["GBM assumption", "Ito Lemma", "inputs", "Greeks", "limitations"]},
    {"domain": "deep_learning", "q": "Explain the transformer architecture end to end.",
     "rubric": ["tokenization", "positional encoding", "multi-head attention", "feed-forward", "layer norm"]},
]

DB_PATH = r'C:\Users\Gurveer\ds-portfolio\project-22-interview-prep-agent\data\sessions.db'
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS sessions
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         date TEXT, domain TEXT, question TEXT,
         score INTEGER, max_score INTEGER,
         percentage REAL, feedback TEXT, missing TEXT)''')
    conn.commit()
    conn.close()

def score_answer(question, rubric, answer, domain):
    prompt = f"""You are a strict technical interviewer scoring a data science candidate.
Question: {question}
Domain: {domain}
Rubric: {json.dumps(rubric)}
Answer: {answer}
Return ONLY valid JSON:
{{
  "total": 3,
  "max": {len(rubric)},
  "percentage": 75,
  "feedback": "feedback here",
  "what_was_missing": "missing points",
  "model_answer_hint": "key points of strong answer"
}}"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = resp.choices[0].message.content.strip().replace("```json","").replace("```","")
    return json.loads(raw)

def save_result(domain, question, score, max_score, pct, feedback, missing):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO sessions 
        (date, domain, question, score, max_score, percentage, feedback, missing)
        VALUES (?,?,?,?,?,?,?,?)''',
        (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
         domain, question, score, max_score, pct, feedback, missing))
    conn.commit()
    conn.close()

# ── Streamlit UI ──────────────────────────────────────────────
init_db()
st.set_page_config(page_title="Interview Prep Agent", page_icon="🎯", layout="wide")
st.title("🎯 DS & AI Interview Prep Agent")
st.caption("Answer each question and get instant AI-powered feedback with rubric scoring.")

if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "results" not in st.session_state:
    st.session_state.results = []
if "scored" not in st.session_state:
    st.session_state.scored = False

q_idx = st.session_state.q_idx

# Progress bar
st.progress(q_idx / len(questions))
st.caption(f"Question {min(q_idx+1, len(questions))} of {len(questions)}")

if q_idx < len(questions):
    q = questions[q_idx]
    st.markdown(f"### [{q['domain'].replace('_',' ').upper()}]")
    st.markdown(f"**{q['q']}**")

    answer = st.text_area("Your answer:", height=180, key=f"ans_{q_idx}")

    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.button("Submit Answer", type="primary")
    with col2:
        skip = st.button("Skip →")

    if submit and answer.strip():
        with st.spinner("Scoring your answer..."):
            result = score_answer(q['q'], q['rubric'], answer, q['domain'])

        pct = result['percentage']
        color = "green" if pct >= 75 else "orange" if pct >= 50 else "red"

        st.markdown(f"### Score: :{color}[{result['total']}/{result['max']} ({pct}%)]")
        st.markdown(f"**📝 Feedback:** {result['feedback']}")
        st.markdown(f"**❌ Missing:** {result['what_was_missing']}")
        st.markdown(f"**💡 Strong answer includes:** {result['model_answer_hint']}")

        save_result(q['domain'], q['q'], result['total'], result['max'],
                    pct, result['feedback'], result['what_was_missing'])

        st.session_state.results.append({
            'domain': q['domain'], 'score': result['total'],
            'max': result['max'], 'percentage': pct
        })

        if st.button("Next Question →"):
            st.session_state.q_idx += 1
            st.rerun()

    if skip:
        st.session_state.q_idx += 1
        st.rerun()

else:
    # Session complete
    st.success("🎉 Session Complete!")
    results = st.session_state.results
    if results:
        df = pd.DataFrame(results)
        total = df['score'].sum()
        possible = df['max'].sum()
        overall = (total / possible * 100) if possible > 0 else 0
        grade = "Excellent 🏆" if overall >= 85 else "Good 👍" if overall >= 70 else "Keep Practicing 💪"

        st.metric("Overall Score", f"{overall:.1f}%", grade)

        st.markdown("### Performance by Domain")
        domain_df = df.groupby('domain')['percentage'].mean().reset_index()
        st.bar_chart(domain_df.set_index('domain'))

        st.markdown("### Historical Progress")
        conn = sqlite3.connect(DB_PATH)
        hist = pd.read_sql(
            "SELECT date, AVG(percentage) as avg_score FROM sessions GROUP BY date",
            conn
        )
        conn.close()
        if len(hist) > 1:
            st.line_chart(hist.set_index('date'))

        if st.button("Start New Session"):
            st.session_state.q_idx = 0
            st.session_state.results = []
            st.rerun()
