# 🛸 MAITRI — Astronaut Wellness System

**Mental Assistance & Integrated Therapeutic Response Intelligence**

A unified Streamlit app combining:
- **MAITRI Chatbot** — Personality-aware AI therapeutic assistant for astronauts (Meera, Kabir, Zara)
- **Arm Curl Analyzer** — MediaPipe-powered exercise tracker with rep counting, angle tracking, and form feedback
- **Mission Logs** — Filterable diary of all wellness entries

---

## 🚀 Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app runs at **http://localhost:8501**

---

## 📁 File Structure
```
maitri_app/
├── app.py              ← Main Streamlit app
├── process_frame.py    ← Arm curl analyzer (MediaPipe)
├── utils.py            ← Drawing utilities
├── sample_video.mp4    ← Demo exercise video
├── requirements.txt
└── astronauts.db       ← Created automatically on first run
```

---

## 🔑 API Key
MAITRI uses the Anthropic API. Set your key as an environment variable:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```
Or add it via Streamlit secrets (`~/.streamlit/secrets.toml`):
```toml
ANTHROPIC_API_KEY = "your-key-here"
```

The app reads it from `st.secrets` or `os.environ` automatically.

---

## 👩‍🚀 Astronaut Profiles
| Astronaut | MBTI | Trait | Therapeutic Style |
|-----------|------|-------|-------------------|
| Meera | ENFJ | Emotional & Expressive | Warm validation, grounding, breathing |
| Kabir | INTJ | Analytical & Stoic | Structured protocols, cognitive reframing |
| Zara | ENFP | Adventurous & Optimistic | Playful visualizations, cosmic imagery |
