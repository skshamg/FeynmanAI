```markdown
# 🎓 FeynmanAI: Socratic Inversion Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Model-Gemini%20Flash-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **"If you can't explain it simply, you don't understand it well enough."** — *Richard Feynman*

**FeynmanAI** is a reverse-Socratic AI learning platform that shifts students from passive consumers into active instructors. Instead of querying an omniscient assistant for answers, the user must teach **Alex**—an inquisitive, slightly confused AI classmate programmed with authentic conceptual misconceptions. 

Behind the scenes, an isolated evaluator tracks pedagogical clarity, detects textbook jargon, and scores genuine conceptual mastery in real time.

---

## ⚡ The Problem: The "Illusion of Competence"
Traditional AI study tools act as automated answer keys. Students passively prompt an LLM, read a wall of text, and mistake familiarity for mastery. Research on the **Feynman Technique** proves that durable learning requires **active retrieval** and articulating complex concepts in simple terms. Current educational AI tools reinforce passivity; FeynmanAI enforces active synthesis.

---

## 🏛️ System Architecture

FeynmanAI decouples conversational pedagogy from evaluation logic using a dual-agent architecture:


```


              +-----------------------------------+
              |        Student (Teacher UI)       |
              +-----------------+-----------------+
                                |
                        [User Explanation]
                                |
        +-----------------------+-----------------------+
        |                                               |
        v                                               v
+-----------------------+                       +-----------------------+
|     Agent 1: Alex     |                       |   Agent 2: Evaluator  |
|  (Inquisitive Peer)   |                       |  (Pedagogy Analyzer)  |
+-----------+-----------+                       +-----------+-----------+
|                                               |
Generates authentic                             Performs background
STEM misconceptions &                           assessment (0-100%) &
counter-questions                               identifies jargon
|                                               |
+-----------------------+-----------------------+
|
v
+-----------------------------------+
|   Streamlit Reactive Dashboard    |
|  - Live Dialogue Stream           |
|  - Dynamic Comprehension Meter    |
|  - LaTeX Formula Typography       |
+-----------------------------------+

```

### Core Execution Flow
1. **The Classroom Stage (Alex):** Driven by an inquisitive persona model (`gemini-3.8-flash`), Alex responds concisely (2–3 sentences) and raises intuitive fallacies (e.g., questioning bound state negative orbital energies or macroscopic vs. microscopic wave-particle duality).
2. **The Scorekeeper (Evaluator Engine):** Concurrently, an isolated evaluator analyzes the transcript against the target concept, scoring cognitive depth and returning structured JSON feedback.
3. **Resilient Gateway:** Built with automated backoff retry logic to handle cloud traffic surges transparently.

---

## ✨ Key Features

- **Reverse-Socratic Paradigm:** The user directs the session while the AI acts as the student testing the teacher's understanding.
- **Dynamic Comprehension HUD:** Real-time visual progress tracking (0% to 100%) that scales as misconceptions are dismantled.
- **Jargon Detection Alert:** Detects when students fall back on memorized definitions without explaining the underlying mechanics.
- **Native LaTeX Rendering:** Seamlessly renders mathematical equations and physical notation (e.g., Bohr radii, de Broglie wavelengths, Rydberg formulas).
- **Zero Frontend Overhead:** 100% Python-engineered reactive web interface using Streamlit.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Frontend / UI Engine:** Streamlit
- **LLM Engine:** Google Gemini Flash (`google-genai` SDK)
- **Environment Management:** `python-dotenv`
- **Math Formatting:** Built-in KaTeX / LaTeX typography

---


### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here

```

### 3. Install Dependencies

```bash
pip install streamlit google-genai python-dotenv

```

### 4. Run the Application

```bash
streamlit run app.py

```

The application will open automatically in your browser at local host.

---

## 🧪 Verification Walkthrough (Example Test Case)

1. **Target Topic:** *Structure of Atom: Bohr's Model & de Broglie Hypothesis*
2. **Turn 1 (Quantization):** User introduces stationary orbits where angular momentum $mvr = \frac{nh}{2\pi}$. Alex questions why accelerating charges don't radiate continuously according to Maxwell's laws.
3. **Turn 2 (Standing Waves):** User introduces de Broglie matter waves ($\lambda = \frac{h}{mv}$) and constructive interference ($2\pi r = n\lambda$). Alex questions why throwing a macroscopic cricket ball doesn't exhibit diffraction around obstacles.
4. **Turn 3 (Scale Resolution):** User explains the magnitude of Planck's constant ($10^{-34}\text{ J s}$). Alex resolves the misconception, and the Comprehension Gauge climbs to full mastery (>90%).

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
