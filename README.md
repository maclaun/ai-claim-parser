# AI Insurance Claim Parser & Lead Automation Dashboard

An AI-powered microservice that simulates how an insurance/compensation company processes incoming legal claims from emails. Uses Google Gemini AI to automatically extract structured data from messy, unstructured claim emails.

## Features

- **AI-Powered Parsing**: Uses Google Gemini (gemini-2.5-flash) with structured JSON output to extract client name, accident date, claim type, damage estimation, and generate summaries
- **Smart Status Assignment**: AI evaluates claim completeness and suggests appropriate status (Pending, Approved, or Requires Human Review)
- **Mock Fallback**: Works without an API key using regex-based mock parser — perfect for development and demos
- **Responsive Dashboard**: Modern dark/light theme with glassmorphism design, built with Tailwind CSS
- **Real-time Updates**: Claims appear instantly without page reload via Fetch API
- **Claim Management**: Approve or reject claims directly from the dashboard

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 / Flask |
| Database | SQLite (WAL mode) |
| AI | Google GenAI SDK (Gemini 2.5 Flash) |
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
# Edit .env and add your GEMINI_API_KEY
```

> Without an API key, the app runs in **mock mode** with simulated AI responses (marked with `[MOCK]` prefix).

### 3. Run

```bash
python app.py
```

Open http://localhost:5000 in your browser.

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
├── ai_parser.py        # Gemini AI integration + mock fallback
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
