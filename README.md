# AI Insurance Claim Parser & Lead Automation Dashboard

An AI-powered microservice that simulates how an insurance/compensation company processes incoming legal claims from emails. Uses Groq (Llama 3.1 8B) as the primary engine and Google Gemini as a secondary fallback to automatically extract structured data from messy, unstructured claim emails.

## Features

- **AI-Powered Parsing**: Uses Llama 3.1 8B (via Groq) or Google Gemini with structured JSON output to extract client name, accident date, claim type, damage estimation, and generate summaries
- **Smart Status Assignment**: AI evaluates claim completeness and suggests appropriate status (Pending, Approved, or Requires Human Review)
- **Multi-Provider Fallback**: Automatically tries Groq first, cascades through multiple Gemini models if Groq fails, and drops back to a regex-based mock parser if no API keys are configured — perfect for offline development
- **Responsive Dashboard**: Modern dark/light theme with glassmorphism design, built with Tailwind CSS
- **Real-time Updates**: Claims appear instantly without page reload via Fetch API
- **Claim Management**: Approve or reject claims directly from the dashboard

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 / Flask |
| Database | SQLite (WAL mode) |
| AI | Groq SDK (Llama 3.1 8B) / Google GenAI SDK (Gemini) |
| Validation | Pydantic v2 |
| Frontend | Tailwind CSS v3 (CDN) + Vanilla JS |

## Quick Start

### 1. Clone and set up

```bash
cd ai-claim-parser
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure API key (optional)

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and/or GEMINI_API_KEY
```

> Without any API keys, the app runs in **mock mode** with simulated AI responses (marked with `[MOCK]` prefix).

### 3. Run

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## n8n & Telegram Integration (Optional)

This project contains a pre-configured n8n workflow file: [n8n-workflow.json](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/n8n-workflow.json). 

The workflow listens for new claims, parses them with Flask AI, and notifies a human reviewer in Telegram if the claim needs review. It also notifies Telegram whenever you approve or reject a claim on the dashboard.

### 1. Setup Your Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Start the chat and send the command `/newbot`. Follow the steps to name your bot and get the **API Token** (looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
3. Search for [@userinfobot](https://t.me/userinfobot) (or any similar ID bot), start it, and copy your **ID** (a number like `987654321`). This is your `Chat ID`.
4. Open a chat with your newly created bot and click **Start** (important, or the bot won't be allowed to message you!).

### 2. Configure n8n
1. **Start the n8n server**: 
   - Double-click `start-n8n.bat` (Windows) or run `n8n start` manually.
2. **Access n8n dashboard**:
   - Open http://localhost:5678 in your browser and complete the initial setup.
3. **Import the workflow**:
   - Click "Build workflow".
   - Open the menu in the top-right corner (three dots) and select **Import from File**.
   - Choose the `n8n-workflow.json` file from the root of this project.
4. **Link your Telegram Credentials**:
   - Double-click the **Telegram: Send Alert** node.
   - Under *Credential to connect with*, click *Select Credential* -> *Create New Credential*.
   - Paste your **API Token** from BotFather and save.
   - In the **Chat ID** field, replace `YOUR_TELEGRAM_CHAT_ID` with your actual ID from `@userinfobot`.
   - Do the exact same for the **Telegram: Status Update** node.

### 3. Connect Flask back-notifications (Optional)
If you want the dashboard "Approve/Reject" buttons to trigger Telegram messages:
1. In n8n, double-click the **Webhook (Status Update)** node.
2. Copy the **Test URL** (e.g. `http://localhost:5678/webhook-test/status-update-trigger`).
3. Open your local `.env` file and paste it there:
   ```env
   N8N_STATUS_WEBHOOK_URL=http://localhost:5678/webhook-test/status-update-trigger
   ```
4. Restart your Flask server (`run.bat`). Now, clicking Approve or Reject on the UI will notify you on Telegram!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard page |
| `GET` | `/api/claims` | List all claims (JSON) |
| `POST` | `/api/incoming-claim` | Submit a new claim for AI processing |
| `POST` | `/api/claim/<id>/status` | Update claim status |

### Submit a claim via API

```bash
curl -X POST http://localhost:5000/api/incoming-claim \
  -H "Content-Type: application/json" \
  -d '{
    "sender_email": "client@example.com",
    "raw_text": "My name is John Doe, on June 12th my car was hit by a truck near Warsaw. The repair cost is around 12000 PLN."
  }'
```

## Project Structure

```
ai-claim-parser/
├── app.py              # Flask server and API routes
├── ai_parser.py        # AI parser module (Groq / Gemini / Mock fallback)
├── database.py         # SQLite schema and CRUD operations
├── models.py           # Pydantic schemas for structured output
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── templates/
    └── index.html      # Dashboard (Tailwind CSS + JS)
```

## License

MIT
