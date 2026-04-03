# V3RSUS | MMA Predictive Analytics

Ensemble machine learning engine that predicts UFC fight outcomes using career stat differentials across 6,500+ historical bouts.

## Quick Start

```bash
pip install -r requirements.txt
python backend/app.py
# open http://localhost:5000
```

## What It Does

Pick two fighters. V3RSUS pulls their career-wide stats, computes the gap between them on 35 dimensions, and runs three ML models (Logistic Regression, Random Forest, Gradient Boosting) to predict the winner. Each prediction includes:

- Win probability with model consensus breakdown
- Top factors driving the prediction, ranked by impact
- Edge analysis across striking, grappling, physical, and experience categories
- Full fighter stat profiles and head-to-head comparison
- Historical matchup results if the fighters have fought before

## How It Works

1. Look up each fighter's most recent career-wide stats from the dataset
2. Compute differential features (Fighter 1 stat - Fighter 2 stat) across 35 dimensions
3. Standardize against training data distribution
4. Three models independently produce win probabilities; their average is the final prediction
5. Explanation engine decomposes the logistic regression output to surface the top contributing factors

Models are trained on 6,528 UFC fights with 5-fold cross-validation. Ensemble accuracy is ~60%, competitive with academic ML studies on MMA (58-68% range). Vegas sits at ~65-70% with access to camp intel, injuries, and insider info we don't have.

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | Vanilla HTML/CSS/JS, Oswald + Barlow fonts |
| Backend | Python, Flask, Flask-CORS |
| ML | scikit-learn (Logistic Regression, Random Forest, Gradient Boosting) |
| Data | pandas, numpy, 6,500+ UFC fights from ufcstats.com |
| Deploy | Vercel (serverless Python) |

## Project Structure

```
V3RSUS/
├── api/                  # Vercel serverless entrypoint
│   └── index.py
├── backend/              # Flask app + ML engine
│   ├── app.py            # API routes, fighter profile builder
│   └── model_engine.py   # Training, prediction, explanation logic
├── public/               # Static frontend
│   ├── index.html        # Main app (hero + prediction UI)
│   ├── about.html        # About page
│   ├── methodology.html  # Technical methodology deep dive
│   ├── style.css         # Global styles
│   ├── methodology.css   # Methodology page styles
│   ├── script.js         # Client-side logic (autocomplete, rendering)
│   └── icon.svg          # Favicon
├── data/                 # Training datasets
│   └── ufc-master.csv    # Primary dataset
├── scripts/              # Original ML training/exploration scripts
├── notebooks/            # Jupyter notebooks from research phase
├── docs/                 # Project documentation and presentations
├── requirements.txt
└── vercel.json
```

## API

All endpoints are served by the Flask backend:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/fighters` | List of all fighters in the dataset |
| GET | `/api/model-info` | Fighter count, fight count, feature count |
| POST | `/api/predict` | Predict a matchup (body: `{ fighter1, fighter2 }`) |

## Contributors

Built for CIS 5450: Big Data Analytics at UPenn.

- Thomas Ou
- Aakash Jha
- Kevin Jiang

---

Built by Thomas Ou
