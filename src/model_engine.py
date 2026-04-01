import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import os


EXCLUDED_BASES = frozenset([
    'odds', 'expectedvalue', 'decodds', 'subodds', 'koodds', 'fighter',
])

FEATURE_DISPLAY = {
    'avgsigstrlanded': 'Sig. Strikes Landed',
    'avgsigstrpct': 'Strike Accuracy',
    'avgsubatt': 'Submission Attempts',
    'avgtdlanded': 'Takedowns Landed',
    'avgtdpct': 'Takedown Accuracy',
    'winsbyko': 'KO Wins',
    'winsbytkoductorstoppage': 'TKO Wins',
    'winsbysubmission': 'Submission Wins',
    'winsbydecisionmajority': 'Majority Dec. Wins',
    'winsbydecisionsplit': 'Split Dec. Wins',
    'winsbydecisionunanimous': 'Unanimous Dec. Wins',
    'heightcms': 'Height',
    'reachcms': 'Reach',
    'weightlbs': 'Weight',
    'age': 'Age',
    'wins': 'Career Wins',
    'losses': 'Career Losses',
    'draws': 'Draws',
    'currentwinstreak': 'Win Streak',
    'currentlosestreak': 'Lose Streak',
    'longestwinstreak': 'Longest Win Streak',
    'totalroundsfought': 'Rounds Fought',
    'totaltitlebouts': 'Title Bouts',
    'losestreak': 'Lose Streak',
    'winstreak': 'Win Streak',
    'win': 'Career Wins',
    'loss': 'Career Losses',
    'totalround': 'Rounds Fought',
    'totaltitlebout': 'Title Bouts',
    'ko': 'KO Wins',
    'sub': 'Submission Wins',
    'height': 'Height',
    'reach': 'Reach',
    'sigstr': 'Sig. Strikes',
    'avgtd': 'Takedowns',
}

FEATURE_CATEGORY = {
    'avgsigstrlanded': 'striking', 'avgsigstrpct': 'striking',
    'winsbyko': 'striking', 'winsbytkoductorstoppage': 'striking',
    'ko': 'striking', 'sigstr': 'striking',

    'avgsubatt': 'grappling', 'avgtdlanded': 'grappling',
    'avgtdpct': 'grappling', 'winsbysubmission': 'grappling',
    'sub': 'grappling', 'avgtd': 'grappling',

    'heightcms': 'physical', 'reachcms': 'physical',
    'weightlbs': 'physical', 'age': 'physical',
    'height': 'physical', 'reach': 'physical',

    'wins': 'experience', 'losses': 'experience', 'draws': 'experience',
    'currentwinstreak': 'experience', 'currentlosestreak': 'experience',
    'longestwinstreak': 'experience', 'totalroundsfought': 'experience',
    'totaltitlebouts': 'experience',
    'winsbydecisionmajority': 'experience', 'winsbydecisionsplit': 'experience',
    'winsbydecisionunanimous': 'experience',
    'losestreak': 'experience', 'winstreak': 'experience',
    'win': 'experience', 'loss': 'experience',
    'totalround': 'experience', 'totaltitlebout': 'experience',
}

CATEGORY_LABELS = {
    'striking': 'Striking',
    'grappling': 'Grappling',
    'physical': 'Physical',
    'experience': 'Experience',
}


class FightPredictor:

    def __init__(self):
        self.models = {}
        self.scaler = None
        self.fights_df = None
        self.features = []
        self.model_metrics = {}
        self.lr_coefficients = None
        self.fighter_count = 0
        self.fight_count = 0
        self.feature_count = 0

    def train(self, data_path='data/ufc-master.csv'):
        print(f"Loading data from {data_path}...")
        if not os.path.exists(data_path):
            alt = '../' + data_path
            if os.path.exists(alt):
                data_path = alt
            else:
                print("ufc-master.csv not found!")
                return False

        self.fights_df = pd.read_csv(data_path)
        fights = self.fights_df.copy()
        self.fight_count = len(fights)

        red_names = fights['RedFighter'].dropna().unique()
        blue_names = fights['BlueFighter'].dropna().unique()
        self.fighter_count = len(set(red_names) | set(blue_names))

        fights['target'] = (fights['Winner'] == 'Red').astype(int)

        red_cols = [c for c in fights.columns if c.startswith('Red') and not c.endswith('Dif')]
        blue_set = set(c for c in fights.columns if c.startswith('Blue') and not c.endswith('Dif'))

        diff_features = {}
        for red_col in red_cols:
            blue_col = red_col.replace('Red', 'Blue', 1)
            if blue_col in blue_set:
                if pd.api.types.is_numeric_dtype(fights[red_col]) and pd.api.types.is_numeric_dtype(fights[blue_col]):
                    base = red_col.replace('Red', '', 1).lower()
                    if base not in EXCLUDED_BASES:
                        diff_features['diff_' + base] = fights[red_col] - fights[blue_col]

        for col in fights.columns:
            if col.endswith('Dif') and pd.api.types.is_numeric_dtype(fights[col]):
                base = col.replace('Dif', '').lower()
                diff_features['diff_' + base] = fights[col]

        X = pd.DataFrame(diff_features).fillna(0)
        y = fights['target']
        self.features = X.columns.tolist()
        self.feature_count = len(self.features)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        configs = [
            ('logistic_regression', LogisticRegression(max_iter=1000, random_state=42)),
            ('random_forest', RandomForestClassifier(
                n_estimators=100, max_depth=8, min_samples_leaf=5,
                random_state=42, n_jobs=-1,
            )),
            ('gradient_boosting', GradientBoostingClassifier(
                n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42,
            )),
        ]

        for name, model in configs:
            print(f"  Training {name}...")
            model.fit(X_scaled, y)
            self.models[name] = model

            scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
            self.model_metrics[name] = {
                'accuracy': round(float(scores.mean()), 4),
                'std': round(float(scores.std()), 4),
            }
            print(f"    {scores.mean():.3f} (+/- {scores.std():.3f})")

        self.lr_coefficients = self.models['logistic_regression'].coef_[0]

        print(f"Trained {len(self.models)} models on {self.feature_count} features "
              f"from {self.fight_count} fights ({self.fighter_count} fighters).")
        return True

    def _base(self, feature_name):
        return feature_name.replace('diff_', '', 1)

    def _display(self, feature_name):
        base = self._base(feature_name)
        return FEATURE_DISPLAY.get(base, base.replace('_', ' ').title())

    def _category(self, feature_name):
        base = self._base(feature_name)
        return FEATURE_CATEGORY.get(base, 'other')

    def _safe_num(self, val):
        if val is None:
            return 0
        if isinstance(val, (int, np.integer)):
            return int(val)
        if isinstance(val, (float, np.floating)):
            return 0 if (np.isnan(val) or np.isinf(val)) else float(val)
        return 0

    def _fmt_val(self, v):
        if isinstance(v, float):
            return round(v, 1) if v != int(v) else int(v)
        return v

    def get_fighter_stats(self, fighter_name):
        fights = self.fights_df
        name_lower = fighter_name.lower()

        red = fights[fights['RedFighter'].str.lower() == name_lower]
        blue = fights[fights['BlueFighter'].str.lower() == name_lower]

        if red.empty and blue.empty:
            return None

        latest_date = None
        is_red = True
        best_row = None

        if not red.empty:
            red = red.sort_values('Date', ascending=False)
            latest_date = red.iloc[0]['Date']
            best_row = red.iloc[0]

        if not blue.empty:
            blue = blue.sort_values('Date', ascending=False)
            b_date = blue.iloc[0]['Date']
            if latest_date is None or b_date > latest_date:
                is_red = False
                best_row = blue.iloc[0]

        prefix = 'Red' if is_red else 'Blue'
        stats = {}
        for col in fights.columns:
            if col.startswith(prefix):
                stats[col.replace(prefix, '', 1)] = best_row[col]

        stats['ActualName'] = best_row[prefix + 'Fighter']
        stats['TotalFights'] = len(red) + len(blue)
        return stats

    def _find_historical(self, f1_name, f2_name):
        fights = self.fights_df
        f1, f2 = f1_name.lower(), f2_name.lower()

        mask = (
            ((fights['RedFighter'].str.lower() == f1) & (fights['BlueFighter'].str.lower() == f2)) |
            ((fights['RedFighter'].str.lower() == f2) & (fights['BlueFighter'].str.lower() == f1))
        )
        matches = fights[mask].sort_values('Date', ascending=False)
        if matches.empty:
            return None

        results = []
        for _, row in matches.iterrows():
            if row['Winner'] == 'Red':
                winner = row['RedFighter']
            elif row['Winner'] == 'Blue':
                winner = row['BlueFighter']
            else:
                winner = 'Draw'

            results.append({
                'date': str(row.get('Date', '')),
                'winner': winner,
                'method': str(row['Finish']) if pd.notna(row.get('Finish')) else None,
                'round': int(row['FinishRound']) if pd.notna(row.get('FinishRound')) else None,
                'time': str(row['FinishRoundTime']) if pd.notna(row.get('FinishRoundTime')) else None,
            })
        return results

    def _compute_diff(self, f1_stats, f2_stats):
        diff_dict = {}
        for fname in self.features:
            base = self._base(fname)
            v1, v2 = 0, 0
            for k, v in f1_stats.items():
                if k.lower() == base:
                    v1 = self._safe_num(v)
                    break
            for k, v in f2_stats.items():
                if k.lower() == base:
                    v2 = self._safe_num(v)
                    break
            diff_dict[fname] = [v1 - v2]
        return pd.DataFrame(diff_dict).fillna(0)

    def _key_factors(self, scaled_vals, f1_name, f2_name, f1_stats, f2_stats):
        contribs = self.lr_coefficients * scaled_vals

        raw = []
        for i, fname in enumerate(self.features):
            c = contribs[i]
            if abs(c) < 0.005:
                continue

            base = self._base(fname)
            v1, v2 = 0, 0
            for k, v in f1_stats.items():
                if k.lower() == base:
                    v1 = self._safe_num(v)
                    break
            for k, v in f2_stats.items():
                if k.lower() == base:
                    v2 = self._safe_num(v)
                    break

            raw.append({
                'factor': self._display(fname),
                'category': self._category(fname),
                'advantage': f1_name if c > 0 else f2_name,
                'impact': round(abs(float(c)), 4),
                'f1Value': self._fmt_val(v1),
                'f2Value': self._fmt_val(v2),
            })

        seen = {}
        for f in raw:
            name = f['factor']
            if name not in seen or f['impact'] > seen[name]['impact']:
                seen[name] = f

        return sorted(seen.values(), key=lambda x: x['impact'], reverse=True)[:8]

    def _category_scores(self, scaled_vals):
        contribs = self.lr_coefficients * scaled_vals

        buckets = {}
        for i, fname in enumerate(self.features):
            cat = self._category(fname)
            if cat in CATEGORY_LABELS:
                buckets.setdefault(cat, []).append(contribs[i])

        result = {}
        for cat in CATEGORY_LABELS:
            if cat in buckets and buckets[cat]:
                avg = np.mean(buckets[cat])
                score = 50 + 50 * float(np.tanh(avg * 3))
                score = max(0, min(100, score))
                if avg > 0.01:
                    adv = 'fighter1'
                elif avg < -0.01:
                    adv = 'fighter2'
                else:
                    adv = 'even'
                result[cat] = {
                    'score': round(score),
                    'advantage': adv,
                    'label': CATEGORY_LABELS[cat],
                }
            else:
                result[cat] = {'score': 50, 'advantage': 'even', 'label': CATEGORY_LABELS[cat]}

        return result

    def predict_matchup(self, f1_name, f2_name):
        f1_stats = self.get_fighter_stats(f1_name)
        f2_stats = self.get_fighter_stats(f2_name)

        if not f1_stats:
            raise ValueError(f"Fighter not found: {f1_name}")
        if not f2_stats:
            raise ValueError(f"Fighter not found: {f2_name}")

        f1_actual = f1_stats['ActualName']
        f2_actual = f2_stats['ActualName']

        X_input = self._compute_diff(f1_stats, f2_stats)
        X_scaled = self.scaler.transform(X_input)
        scaled = X_scaled[0]

        model_breakdown = {}
        ensemble_prob = np.zeros(2)

        for name, model in self.models.items():
            prob = model.predict_proba(X_scaled)[0]
            model_breakdown[name] = {
                'f1Prob': round(float(prob[1]), 4),
                'f2Prob': round(float(prob[0]), 4),
                'accuracy': self.model_metrics[name]['accuracy'],
            }
            ensemble_prob += prob

        ensemble_prob /= len(self.models)
        f1_prob = float(ensemble_prob[1])
        f2_prob = float(ensemble_prob[0])

        winner = f1_actual if f1_prob > 0.5 else f2_actual
        confidence = max(f1_prob, f2_prob)

        model_breakdown['ensemble'] = {
            'f1Prob': round(f1_prob, 4),
            'f2Prob': round(f2_prob, 4),
        }

        return {
            'winner': winner,
            'confidence': round(confidence, 4),
            'f1Prob': round(f1_prob, 4),
            'f2Prob': round(f2_prob, 4),
            'f1Name': f1_actual,
            'f2Name': f2_actual,
            'f1Stats': f1_stats,
            'f2Stats': f2_stats,
            'keyFactors': self._key_factors(scaled, f1_actual, f2_actual, f1_stats, f2_stats),
            'categoryAnalysis': self._category_scores(scaled),
            'modelBreakdown': model_breakdown,
            'historicalMatchups': self._find_historical(f1_name, f2_name),
        }

    def get_model_info(self):
        return {
            'fightCount': self.fight_count,
            'fighterCount': self.fighter_count,
            'featureCount': self.feature_count,
            'models': self.model_metrics,
            'categories': list(CATEGORY_LABELS.keys()),
        }
