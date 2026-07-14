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

## n8n Integration (Optional)

This repository includes a pre-configured n8n workflow file: [n8n-workflow.json](file:///c:/Users/maclaun/Desktop/auton8n/ai-claim-parser/n8n-workflow.json).

To set up the n8n automation locally:
1. **Start the n8n server**: 
   - Double-click `start-n8n.bat` (Windows) or run `n8n start` manually.
2. **Access n8n dashboard**:
   - Open http://localhost:5678 in your browser and complete the initial setup.
3. **Import the workflow**:
   - Click "Build workflow".
   - Open the menu in the top-right corner (three dots) and select **Import from File**.
   - Choose the `n8n-workflow.json` file from the root of this project.
4. **Test the integration**:
   - Make sure your Flask server is running on port 5000.
   - Click the orange **"Execute workflow"** button in n8n.
   - Send a test payload to your n8n webhook URL to see the data parsed by Llama 3.1 8B in real time!

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
