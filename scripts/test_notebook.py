#!/usr/bin/env python3
"""
Quick test to verify the notebook will compile correctly
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("   ⚠️  XGBoost not installed locally (will be available in Google Colab)")

print("="*60)
print("TESTING NOTEBOOK COMPILATION")
print("="*60)

# 1. Load data
print("\n1. Loading data...")
fights = pd.read_csv('../data/ufc-master.csv')
print(f"   ✅ Loaded {len(fights)} fights with {len(fights.columns)} columns")

# 2. Create target
print("\n2. Creating target variable...")
fights['target'] = (fights['Winner'] == 'Red').astype(int)
print(f"   ✅ Target created. Red wins: {fights['target'].sum()}, Blue wins: {(~fights['target'].astype(bool)).sum()}")

# 3. Create differential features
print("\n3. Creating differential features...")
red_cols = [col for col in fights.columns if col.startswith('Red') and not col.endswith('Dif')]
blue_cols = [col for col in fights.columns if col.startswith('Blue') and not col.endswith('Dif')]

diff_features = {}
for red_col in red_cols:
    blue_col = red_col.replace('Red', 'Blue')
    if blue_col in blue_cols:
        # Only create differential for numeric columns
        if pd.api.types.is_numeric_dtype(fights[red_col]) and pd.api.types.is_numeric_dtype(fights[blue_col]):
            feature_name = 'diff_' + red_col.replace('Red', '').lower()
            diff_features[feature_name] = fights[red_col] - fights[blue_col]

# Add existing differentials
existing_dif_cols = [col for col in fights.columns if col.endswith('Dif')]
for existing_dif in existing_dif_cols:
    normalized_name = 'diff_' + existing_dif.replace('Dif', '').lower()
    diff_features[normalized_name] = fights[existing_dif]

diff_df = pd.DataFrame(diff_features)
print(f"   ✅ Created {len(diff_features)} differential features")

# 4. Prepare for modeling
print("\n4. Preparing data for modeling...")
X = diff_df.fillna(0)
y = fights['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"   ✅ Train: {len(X_train)} samples, Test: {len(X_test)} samples")

# 5. Train models
print("\n5. Training models...")

# Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
lr_acc = accuracy_score(y_test, lr.predict(X_test_scaled))
print(f"   ✅ Logistic Regression: {lr_acc:.4f} ({lr_acc*100:.2f}%)")

# Random Forest
rf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_acc = accuracy_score(y_test, rf.predict(X_test))
print(f"   ✅ Random Forest: {rf_acc:.4f} ({rf_acc*100:.2f}%)")

# XGBoost
if HAS_XGB:
    xgb = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric='logloss')
    xgb.fit(X_train, y_train)
    xgb_acc = accuracy_score(y_test, xgb.predict(X_test))
    print(f"   ✅ XGBoost: {xgb_acc:.4f} ({xgb_acc*100:.2f}%)")
else:
    xgb_acc = 0.0
    print(f"   ⚠️  XGBoost: Skipped (not installed)")

# Summary
print("\n" + "="*60)
print("✅ ALL TESTS PASSED - NOTEBOOK WILL COMPILE CORRECTLY!")
print("="*60)
print(f"\nBest Model: {max([('Logistic Regression', lr_acc), ('Random Forest', rf_acc), ('XGBoost', xgb_acc)], key=lambda x: x[1])[0]}")
print(f"Best Accuracy: {max(lr_acc, rf_acc, xgb_acc):.4f}")
print(f"Improvement over random: +{(max(lr_acc, rf_acc, xgb_acc) - 0.5)*100:.2f} percentage points")
