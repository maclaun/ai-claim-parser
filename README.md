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

### 1. Clone and Setup
For Windows users, we have automated the environment setup:
1. Double-click [setup.bat](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/setup.bat). This will create a Python virtual environment, install dependencies, and create your `.env` file.

*For macOS/Linux users, run manually:*
```bash
cd ai-claim-parser
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Credentials
1. Open `.env` and paste your `GROQ_API_KEY`.
2. Open [start-n8n.bat](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/start-n8n.bat) and paste your Telegram bot credentials (token and chat ID).

> Without API keys, the app runs in **mock mode** with local regex parsing.

### 3. Run Everything in One Click
For Windows users, run both the Flask server and n8n server concurrently:
1. Double-click [start-all.bat](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/start-all.bat).

*For macOS/Linux, run manually:*
```bash
python app.py
```
Flask app will open at http://localhost:5000.

## n8n & Telegram Integration (Optional)

This project contains a pre-configured n8n workflow file: [n8n-workflow.json](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/n8n-workflow.json). 

The workflow listens for new claims, parses them with Flask AI, and notifies a human reviewer in Telegram if the claim needs review. It also notifies Telegram whenever you approve or reject a claim on the dashboard.

### 1. Setup Your Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Start the chat and send the command `/newbot`. Follow the steps to name your bot and get the **API Token** (looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
3. Search for [@userinfobot](https://t.me/userinfobot) (or any similar ID bot), start it, and copy your **ID** (a number like `987654321`). This is your `Chat ID`.
4. Open a chat with your newly created bot and click **Start** (important, or the bot won't be allowed to message you!).

### 2. Configure and Run n8n
1. **Configure Environment Variables**:
   - Open [start-n8n.bat](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/start-n8n.bat) in any text editor.
   - Insert your Telegram bot token and chat ID into the configuration section:
     ```bat
     set "TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN"
     set "TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID"
     ```
2. **Start the n8n server**: 
   - Double-click [start-n8n.bat](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/start-n8n.bat) to run the server.
3. **Access n8n dashboard**:
   - Open http://localhost:5678 in your browser and complete the initial setup.
4. **Import the workflow**:
   - Click **Build workflow**.
   - Open the menu in the top-right corner (three dots) and select **Import from File**.
   - Choose the `n8n-workflow.json` file from the root of this project.
5. **No Credentials Needed**:
   - The workflow uses the environment variables you defined in `start-n8n.bat`. The Telegram HTTP nodes automatically read them via `{{ $env.TELEGRAM_BOT_TOKEN }}` and `{{ $env.TELEGRAM_CHAT_ID }}`. No manual setup in n8n is required!

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
