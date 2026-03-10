# Artisan Dashboard — MVP

> Helping artisans discover modern market-relevant design trends and generate new product design concepts while preserving traditional craft identity.

A social venture platform that acts as a **creative assistant and market-intelligence layer** for artisans. The artisan remains the creator; technology helps them understand what's trending and visualize adapted product ideas before investing time and material.

---

## Features

- **Landing Page** — Mission statement, problem overview, and CTA
- **Artisan Dashboard** — Unified workspace with craft profile, trend explorer, design generator, and saved ideas
- **Trend Recommendations** — Discover trending colors, motifs, product formats, and styling insights for your craft type
- **Design Concept Generator** — Enter design parameters and generate a concept prompt + preview image
- **Saved Ideas Gallery** — Browse, review, and download design briefs from your concept history
- **Profile Editing** — Update artisan name, craft type, region, and materials

## Tech Stack

| Layer     | Technology                            |
|-----------|---------------------------------------|
| Frontend  | HTML, CSS, JavaScript, Bootstrap 5    |
| Backend   | Flask (Python)                        |
| Database  | SQLite                                |
| Templates | Jinja2                                |
| Fonts     | Google Fonts (Outfit, Playfair Display) |

## Project Structure

```
webapp/
├── app.py                  # Flask app entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md
├── templates/
│   ├── base.html           # Base layout with nav & footer
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Main dashboard
│   └── saved_concepts.html # Saved concepts gallery
├── static/
│   ├── css/styles.css      # Custom artisan-themed styles
│   ├── js/dashboard.js     # Frontend logic
│   └── images/generated/   # Generated concept images
├── routes/
│   ├── main_routes.py      # Page routes (/, /dashboard, /saved-concepts)
│   └── api_routes.py       # API endpoints
├── services/
│   ├── trend_service.py    # Trend recommendation engine
│   ├── prompt_service.py   # Design prompt builder
│   └── image_service.py    # Image generation (mock/pluggable)
├── models/
│   └── concept_model.py    # SQLite CRUD for saved concepts
├── data/
│   └── mock_trends.json    # Mock trend data (3 craft types)
├── database/
│   └── app.db              # SQLite database (auto-created)
└── utils/
    └── __init__.py         # Helper utilities
```

## Quick Start

### 1. Clone and navigate

```bash
cd webapp
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 5. Run the application

```bash
python app.py
```

The app will be available at **http://localhost:5000**

## API Endpoints

| Method | Endpoint                          | Description                           |
|--------|-----------------------------------|---------------------------------------|
| GET    | `/`                               | Landing page                          |
| GET    | `/dashboard`                      | Artisan dashboard                     |
| GET    | `/saved-concepts`                 | Saved concepts gallery                |
| POST   | `/api/recommend-trends`           | Get trend recommendations             |
| POST   | `/api/generate-design`            | Generate a design concept             |
| GET    | `/api/concepts`                   | List all saved concepts               |
| DELETE | `/api/concepts/<id>`              | Delete a saved concept                |
| GET    | `/api/crafts`                     | List available craft types            |
| GET    | `/api/products/<craft>`           | Get products for a craft type         |
| GET    | `/api/audiences/<craft>/<product>`| Get audiences for a craft-product     |
| PUT    | `/api/profile`                    | Update artisan profile                |

## Mock Data

The MVP includes realistic trend data for three craft types:

- **Banarasi Weaving** — Saris and stoles for multiple audience segments
- **Madhubani Art** — Tote bags and wall art for urban/home decor buyers
- **Block Printing** — Cushion covers and table runners for lifestyle buyers

## Future Integration Points

The codebase is structured for easy API integration:

- **Trend Sources** — Pinterest API, social media scraping, e-commerce feeds (see `services/trend_service.py`)
- **Image Generation** — OpenAI DALL-E, Stability AI, Hugging Face (see `services/image_service.py`)
- **LangChain** — Structured prompt templates and chains (see comments in `services/prompt_service.py`)
- **User Auth** — Add Flask-Login for multi-artisan support
- **Marketplace** — Extend to include product listings and buyer interface

## License

This project is part of a social venture initiative.
