<div align="center">
  <img src="https://img.shields.io/badge/Status-Beta-indigo?style=for-the-badge" alt="Status Badge"/>
  <h1>⚖️ VERDIX</h1>
  <p><strong>The Autonomous Financial Decision Engine that passes a verdict before it pays.</strong></p>
</div>

<br />

VERDIX is an autonomous multi-agent financial decision engine built for the **Locus Hackathon**. It acts as an intelligent intermediary for your wallet, analyzing, negotiating, and executing transactions based on a user's defined risk thresholds, budget constraints, and spending memory. 

Instead of simple automated payments, VERDIX simulates a complete human purchasing funnel using distinct AI agents that cross-evaluate each other before generating a final transaction signature.

## 🚀 Key Features

*   **Multi-Agent Pipeline:** Five distinct agents (Scout, Analyst, Trust, Negotiator, Executor) work in orchestration to process a transaction.
*   **0–100 Trust/Risk Scoring Engine:** Automatically flags suspicious pricing, unverified sellers, or market anomalies before money moves.
*   **Simulated Negotiation Loop:** A dynamic `AI ↔ Seller` interaction model that negotiates prices based on personality tokens (Budget, Balanced, Premium).
*   **Cross-Agent Memory:** Past purchases, brand preferences, and budget patterns influence new evaluations in real-time.
*   **Cost & Conflict Tracking:** Fully transparent tracking of API/USDC costs per reasoning step, and automatic detection of agent disagreements.
*   **Live Locus API Integration:** Built on Locus’s wrapped APIs (Exa for Search, Firecrawl for scraping, OpenAI for reasoning, Base network for USDC).

---

## 🧠 The Agent Architecture

VERDIX breaks every transaction down into 5 collaborative steps:

1.  **Scout Agent:** Searches the web (via Exa) to compile a competitive catalog of products matching the user's intent.
2.  **Analyst Agent:** Scores each product (0-100) based on base value, budget fit, and user memory (preferred brands vs. avoid lists).
3.  **Trust Agent:** Calculates a 0-100 risk score, detecting price anomalies (e.g., "50% below market average") and generating security flags.
4.  **Negotiator Agent:** Engages in simulated multi-turn chats with the seller to negotiate a better deal based on the user's personality configuration.
5.  **Executor Agent:** The final judge. Checks negotiated price against the wallet balance and configured spending limits, resulting in either a `PURCHASED` or `REFUSED` verdict.

---

## 🛠️ Tech Stack

*   **Frontend:** Next.js (App Router), React, TypeScript.
*   **Styling:** Custom CSS with Glassmorphism and animated micro-interactions.
*   **Backend:** Python, FastAPI, Uvicorn, Pydantic.
*   **Intelligence:** Locus Wrapped APIs (OpenAI `gpt-4o-mini`, Exa Search).
*   **Payments:** Locus Wallet integrations (USDC on Base).

---

## 🚀 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (3.9+)
*   A Locus Developer API Key (`claw_dev_...`)

### Installation 

1. **Clone the repository**
   ```bash
   git clone https://github.com/Infinite-Leo/VERDIX.git
   cd VERDIX
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   LOCUS_API_KEY=your_locus_api_key_here
   LOCUS_BASE_URL=https://beta-api.paywithlocus.com/api
   MAX_TRANSACTION_USDC=50.0
   SPENDING_LIMIT_USDC=100.0
   DEMO_MODE=true # Set to false to use actual Locus wallet balance
   ```

3. **Start the Backend (FastAPI)**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Start the Frontend (Next.js)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Run the App**
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Demo Mode Overview

VERDIX includes a robust `DEMO_MODE` to ensure presentations run perfectly even if the connected Locus wallet currently holds 0 USDC. When the wallet is empty, the system automatically falls back to a deterministic, realistic simulation layer (`demo_data.py`), which perfectly emulates the Locus JSON envelope responses.

As soon as the wallet is funded with USDC, the platform seamlessly switches back to triggering live Exa searches, actual LLM generation, and real on-chain checks.

---

<div align="center">
  <i>Built for the Locus Autonomous Agent Hackathon</i>
</div>
