# V3RSUS Improvement Plan

## Current State

- Single Logistic Regression model (~60-65% accuracy)
- No prediction explanation - just winner + confidence
- No feature importance surfaced to users
- Only uses most recent fight data per fighter
- No categorized breakdown (striking vs grappling vs physical)
- No historical head-to-head check
- Frontend is functional but doesn't show any reasoning

## Goal

Make V3RSUS a professional-grade MMA analytics platform where predictions are **transparent** - users see exactly *why* the model predicts a winner, broken down by category, with key driving factors highlighted.

---

## Phase 1: Algorithm Engine (Priority)

### 1.1 Ensemble Model
- Combine **Logistic Regression + Random Forest + Gradient Boosting**
- Average predicted probabilities across all three for more robust predictions
- Track cross-validation accuracy for each model and the ensemble
- Expected improvement: ~65-70% accuracy (up from ~60-65%)

### 1.2 Prediction Explanation Engine
For every prediction, compute and return:

**Key Factors** (top 5-8 features driving this prediction):
- Which differential features contributed most to the outcome
- Use LR coefficients * feature values, RF/GB feature importances
- Human-readable descriptions: "Fighter 1 lands 5.2 sig. strikes/min vs 3.1"

**Categorized Edge Analysis** - group all features into 5 categories:
| Category | Features |
|----------|----------|
| **Striking** | Sig strikes landed/min, accuracy %, head/body/leg/distance/clinch strikes |
| **Grappling** | Takedown landed/accuracy, submission attempts, ground strikes, control |
| **Physical** | Height, reach, weight, age |
| **Experience** | Total fights, rounds, title bouts, win/loss ratio, streak |
| **Defense** | Strike defense %, TD defense %, sub defense %, absorption rates |

For each category, compute which fighter has the edge and a 0-100 score.

**Historical Matchup** - check if these two fighters have fought before in the dataset, return date/winner/method.

### 1.3 Fighter Stats Improvements
- Use **weighted average** of last 3 fights (most recent weighted heaviest) instead of just the single most recent fight
- Compute a fighter "power rating" from their overall stats

### 1.4 Model Metrics
- Run k-fold cross-validation at train time
- Store and expose accuracy, precision, recall for each model + ensemble

---

## Phase 2: API Enhancement

Enrich `/api/predict` response with:
```
{
  // existing fields stay the same
  "analysis": {
    "keyFactors": [...],        // top factors with descriptions
    "categories": {             // 5-category edge breakdown
      "striking": { advantage, score, factors },
      "grappling": { ... },
      "physical": { ... },
      "experience": { ... },
      "defense": { ... }
    },
    "historicalMatchup": null | { date, winner, method },
    "modelBreakdown": {         // per-model predictions
      "logistic_regression": { prob, accuracy },
      "random_forest": { prob, accuracy },
      "gradient_boosting": { prob, accuracy },
      "ensemble": { prob, accuracy }
    }
  }
}
```

New endpoint: `GET /api/model-info` - returns model metrics, feature count, training data stats.

---

## Phase 3: Frontend (after algorithm)

- Display prediction analysis cards (key factors, category breakdown)
- Radar/spider chart for 5-category comparison
- Model confidence breakdown visualization
- Historical matchup display
- Overall polish and professional feel

---

## Implementation Order

1. Rewrite `src/model_engine.py` with ensemble + explanation engine
2. Update `app.py` API to return enriched data
3. Update frontend to display analysis
