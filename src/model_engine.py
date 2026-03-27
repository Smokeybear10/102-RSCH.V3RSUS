import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import os

class FightPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.fights_df = None
        self.features = []

    def train(self, data_path='data/ufc-master.csv'):
        print(f"Loading data from {data_path}...")
        if not os.path.exists(data_path):
            if os.path.exists('../' + data_path):
                data_path = '../' + data_path
            else:
                print("ufc-master.csv not found!")
                return False

        self.fights_df = pd.read_csv(data_path)
        fights = self.fights_df.copy()

        print("Preparing features...")
        fights['target'] = (fights['Winner'] == 'Red').astype(int)

        red_cols = [col for col in fights.columns if col.startswith('Red') and not col.endswith('Dif')]
        blue_cols = [col for col in fights.columns if col.startswith('Blue') and not col.endswith('Dif')]

        diff_features = {}
        for red_col in red_cols:
            blue_col = red_col.replace('Red', 'Blue')
            if blue_col in blue_cols:
                if pd.api.types.is_numeric_dtype(fights[red_col]) and pd.api.types.is_numeric_dtype(fights[blue_col]):
                    feature_name = 'diff_' + red_col.replace('Red', '').lower()
                    diff_features[feature_name] = fights[red_col] - fights[blue_col]

        existing_dif_cols = [col for col in fights.columns if col.endswith('Dif')]
        for existing_dif in existing_dif_cols:
            normalized_name = 'diff_' + existing_dif.replace('Dif', '').lower()
            diff_features[normalized_name] = fights[existing_dif]

        diff_df = pd.DataFrame(diff_features)
        X = diff_df.fillna(0)
        y = fights['target']
        
        self.features = X.columns.tolist()

        print("Training model...")
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.model.fit(X_scaled, y)
        print("Model trained successfully via Logistic Regression!")
        return True

    def get_fighter_stats(self, fighter_name):
        fights = self.fights_df
        
        red_matches = fights[fights['RedFighter'].str.lower() == fighter_name.lower()]
        blue_matches = fights[fights['BlueFighter'].str.lower() == fighter_name.lower()]
        
        if red_matches.empty and blue_matches.empty:
            return None
            
        latest_date = None
        is_red = True
        best_row = None
        
        if not red_matches.empty:
            red_matches = red_matches.sort_values('Date', ascending=False)
            latest_date = red_matches.iloc[0]['Date']
            best_row = red_matches.iloc[0]
            
        if not blue_matches.empty:
            blue_matches = blue_matches.sort_values('Date', ascending=False)
            b_date = blue_matches.iloc[0]['Date']
            if latest_date is None or b_date > latest_date:
                is_red = False
                best_row = blue_matches.iloc[0]
                
        stats = {}
        prefix = 'Red' if is_red else 'Blue'
        for col in fights.columns:
            if col.startswith(prefix):
                base_name = col.replace(prefix, '')
                stats[base_name] = best_row[col]
                
        # Assign real name matching casing
        stats['ActualName'] = best_row[prefix + 'Fighter']
        return stats

    def predict_matchup(self, f1_name, f2_name):
        f1_stats = self.get_fighter_stats(f1_name)
        f2_stats = self.get_fighter_stats(f2_name)
        
        if not f1_stats:
            raise ValueError(f"Fighter not found: {f1_name}")
        if not f2_stats:
            raise ValueError(f"Fighter not found: {f2_name}")
            
        # Compute diff logic
        f1_actual = f1_stats['ActualName']
        f2_actual = f2_stats['ActualName']
        
        diff_dict = {}
        for feature_name in self.features:
            base_col = feature_name.replace('diff_', '', 1)
            
            # The original diff logic was: diff_feature = RedStat - BlueStat
            # For pre-existing diffs, it's harder, but let's approximate
            # We will use f1 as Red and f2 as Blue.
            
            # Find the matching stat name
            # Because we lowercased base_name in train: feature_name = 'diff_' + red_col.replace('Red', '').lower()
            # Let's search for case-insensitive match in f1_stats keys
            val1 = 0
            val2 = 0
            for k, v in f1_stats.items():
                if k.lower() == base_col and pd.api.types.is_numeric_dtype(type(v)):
                    val1 = v
            for k, v in f2_stats.items():
                if k.lower() == base_col and pd.api.types.is_numeric_dtype(type(v)):
                    val2 = v
                    
            diff_dict[feature_name] = [val1 - val2]
            
        X_input = pd.DataFrame(diff_dict)
        X_input = X_input.fillna(0)
        X_scaled = self.scaler.transform(X_input)
        
        prob = self.model.predict_proba(X_scaled)[0]

        winner = f1_actual if prob[1] > 0.5 else f2_actual
        confidence = max(prob)

        return winner, confidence, f1_actual, f2_actual, prob, f1_stats, f2_stats
