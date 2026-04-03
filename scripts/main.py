from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
global_feature_columns = None

#======================================================================================================================

important_features = [
#--------------DIFFERENTIALS---------------
'precomp_age_differential',
'precomp_height_differential',
'precomp_days_since_last_comp_differential',
'precomp_reach_differential',
'precomp_avg_head_strikes_absorbed_differential',
'precomp_total_comp_time_differential',
'precomp_avg_takedowns_def_differential',
'precomp_avg_distance_strikes_def_differential',
'precomp_avg_sig_strikes_absorbed_differential',
'precomp_avg_control_differential',
'precomp_avg_total_strikes_absorbed_differential',
'precomp_avg_takedowns_attempts_per_min_differential',
'precomp_win_loss_ratio_differential',
'precomp_avg_distance_strikes_absorbed_differential',
'precomp_avg_body_strikes_def_differential',
'precomp_avg_stamina_differential',
'precomp_avg_ground_strikes_def_differential',
'precomp_total_strikes_def_differential',
'precomp_avg_ground_strikes_attempts_per_min_differential',
'precomp_avg_clinch_strikes_def_differential',
'precomp_avg_clinch_strikes_attempts_per_min_differential',
'precomp_avg_head_strikes_attempts_differential',
'precomp_avg_head_strikes_landed_per_min_differential',
'precomp_avg_total_strikes_def_differential',
'precomp_avg_leg_strikes_def_differential',
'precomp_distance_strikes_def_differential',
'precomp_avg_ground_strikes_landed_per_min_differential',
'precomp_avg_clinch_strikes_landed_per_min_differential',
'precomp_head_strikes_def_differential',
'precomp_avg_sig_strikes_def_differential',
'precomp_sig_strikes_def_differential',
'precomp_avg_leg_strikes_attempts_per_min_differential',
'precomp_avg_head_strikes_def_differential',
'precomp_control_differential',
'precomp_avg_total_comp_time_differential',
'precomp_avg_total_distance_strikes_absorbed_differential',
'precomp_avg_ground_strikes_absorbed_differential',
'precomp_avg_body_strikes_attempts_per_min_differential',
'precomp_head_strikes_landed_per_min_differential',
'precomp_clinch_strikes_attempts_per_min_differential',
'precomp_avg_distance_strikes_attempts_per_min_differential',
'precomp_avg_clinch_strikes_absorbed_differential',
'precomp_num_fights_differential',
'precomp_avg_head_strikes_attempts_per_min_differential',
'precomp_avg_body_strikes_landed_per_min_differential',
'precomp_avg_total_body_strikes_absorbed_differential',
'precomp_avg_leg_strikes_landed_per_min_differential',
'precomp_body_strikes_def_differential',
'precomp_avg_takedowns_landed_per_min_differential',
'precomp_total_distance_strikes_absorbed_differential',
'precomp_avg_body_strikes_absorbed_differential',
'precomp_avg_total_clinch_strikes_absorbed_differential',
'precomp_avg_total_strikes_attempts_per_min_differential',
'precomp_avg_leg_strikes_absorbed_differential',
'precomp_avg_num_fights_differential',
'precomp_body_strikes_landed_per_min_differential',
'precomp_avg_distance_strikes_landed_per_min_differential',
'precomp_body_strikes_attempts_per_min_differential',
'precomp_distance_strikes_attempts_per_min_differential',
'precomp_avg_total_head_strikes_absorbed_differential',
'precomp_head_strikes_attempts_per_min_differential',
'precomp_total_head_strikes_absorbed_differential',
'precomp_avg_total_strikes_landed_per_min_differential',
'precomp_head_strikes_absorbed_differential',
'precomp_total_clinch_strikes_absorbed_differential',
'precomp_avg_sub_attempts_per_min_differential',
'precomp_total_sig_strikes_absorbed_differential',
'precomp_total_leg_strikes_absorbed_differential',
'precomp_avg_win_loss_ratio_differential',
'precomp_sig_strikes_absorbed_differential',
'precomp_avg_total_leg_strikes_absorbed_differential',
'precomp_avg_sig_strikes_landed_per_min_differential',
'precomp_avg_sub_def_differential',
'precomp_leg_strikes_attempts_per_min_differential',
'precomp_avg_total_sig_strikes_absorbed_differential',
'precomp_total_total_strikes_absorbed_differential',
'precomp_total_strikes_landed_per_min_differential',
'precomp_distance_strikes_absorbed_differential',
'precomp_stamina_differential',
'precomp_avg_total_total_strikes_absorbed_differential',
'precomp_avg_total_takedowns_absorbed_differential',
'precomp_total_strikes_absorbed_differential',
'precomp_avg_takedowns_absorbed_differential',
'precomp_avg_sig_strikes_attempts_per_min_differential',
'precomp_total_strikes_attempts_per_min_differential',
'precomp_total_body_strikes_absorbed_differential',
'precomp_avg_win_streak_differential',
'precomp_clinch_strikes_landed_per_min_differential',
'precomp_ground_strikes_def_differential',
'precomp_avg_total_ground_strikes_absorbed_differential',
'precomp_leg_strikes_landed_per_min_differential',
'precomp_total_ground_strikes_absorbed_differential',
'precomp_takedowns_def_differential',
'precomp_clinch_strikes_def_differential',
'precomp_sig_strikes_landed_per_min_differential',
'precomp_sig_strikes_attempts_per_min_differential',
'precomp_distance_strikes_landed_per_min_differential',
'precomp_takedowns_attempts_per_min_differential',
'precomp_ground_strikes_attempts_per_min_differential',
'precomp_body_strikes_absorbed_differential',
'precomp_avg_KO_losses_differential',
'precomp_leg_strikes_absorbed_differential',
'precomp_leg_strikes_def_differential',
'precomp_ground_strikes_landed_per_min_differential',
'precomp_total_takedowns_absorbed_differential',
'precomp_avg_lose_streak_differential',
'precomp_clinch_strikes_absorbed_differential',
'precomp_takedowns_landed_per_min_differential',
'precomp_ground_strikes_absorbed_differential',
'precomp_avg_sub_landed_per_min_differential',
'precomp_avg_total_sub_absorbed_differential',
'precomp_avg_knockdowns_differential',
'precomp_avg_reversals_differential',
'precomp_win_streak_differential',
'precomp_avg_sub_absorbed_differential',
'precomp_sub_attempts_per_min_differential',
'precomp_lose_streak_differential',
'precomp_takedowns_absorbed_differential',
'precomp_KO_losses_differential',
'precomp_sub_def_differential',
'precomp_total_sub_absorbed_differential',
'precomp_sub_landed_per_min_differential',
'precomp_knockdowns_differential',
'precomp_reversals_differential',
'precomp_sub_absorbed_differential',
'precomp_comp_time_differential',
'precomp_avg_comp_time_differential',
#--------------ACCURACY---------------
'precomp_avg_ground_strikes_acc_differential',
'precomp_avg_leg_strikes_acc_differential',
'precomp_avg_takedowns_acc_differential',
'precomp_head_strikes_acc_differential',
'precomp_avg_head_strikes_acc_differential',
'precomp_avg_sig_strikes_acc_differential',
'precomp_avg_body_strikes_acc_differential',
'precomp_body_strikes_acc_differential',
'precomp_avg_clinch_strikes_acc_differential',
'precomp_total_strikes_acc_differential',
'precomp_avg_distance_strikes_acc_differential',
'precomp_avg_total_strikes_acc_differential',
'precomp_distance_strikes_acc_differential',
'precomp_ground_strikes_acc_differential',
'precomp_sig_strikes_acc_differential',
'precomp_leg_strikes_acc_differential',
'precomp_clinch_strikes_acc_differential',
'precomp_avg_sub_acc_differential',
'precomp_takedowns_acc_differential',
'precomp_sub_acc_differential',
#---------------LANDED----------------
'precomp_avg_head_strikes_landed_differential',
'precomp_avg_sig_strikes_landed_differential',
'precomp_avg_total_strikes_landed_differential',
'precomp_avg_distance_strikes_landed_differential',
'precomp_avg_takedowns_landed_differential',
'precomp_avg_body_strikes_landed_differential',
'precomp_avg_leg_strikes_landed_differential',
'precomp_head_strikes_landed_differential',
'precomp_avg_clinch_strikes_landed_differential',
'precomp_avg_ground_strikes_landed_differential',
'precomp_sig_strikes_landed_differential',
'precomp_distance_strikes_landed_differential',
'precomp_total_strikes_landed_differential',
'precomp_body_strikes_landed_differential',
'precomp_leg_strikes_landed_differential',
'precomp_clinch_strikes_landed_differential',
'precomp_ground_strikes_landed_differential',
'precomp_takedowns_landed_differential',
'precomp_avg_sub_landed_differential',
'precomp_sub_landed_differential',
]

#======================================================================================================================

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully from", filepath)
        return df
    except FileNotFoundError:
        print(f"Error: The file {filepath} does not exist.")
        return None

#======================================================================================================================

def display_feature_importance(model, feature_names):
    importances = model.feature_importances_
    feature_importance_dict = {name: importance for name, importance in zip(feature_names, importances)}
    sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)
    print("Attributes' Computed Weights: ")
    for index, (feature, importance) in enumerate(sorted_features[:350], start=1):
        formatted_feature = ' '.join(word.capitalize() for word in feature.split('_'))
        print(f"{index}) {formatted_feature}: {importance:.3f}")

#======================================================================================================================

def preprocess_data(df):
    df['fighter'] = df['fighter'].str.lower()
    df['opponent'] = df['opponent'].str.lower()
    if 'date' in df.columns:
        df.drop('date', axis=1, inplace=True)

    for col in important_features:
        if df[col].dtype == object:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    return df

#======================================================================================================================

def get_fighter_data(fighter_name, df):
    fighter_data = df[df['fighter'] == fighter_name][important_features]
    if not fighter_data.empty:
        return fighter_data.mean()
    else:
        print(f"No data found for fighter {fighter_name}. Using zero-filled data.")
        return pd.Series(0, index=important_features)
    
#======================================================================================================================

def make_fight_prediction(fighter1_data, fighter2_data, feature_columns, model):
    differential_data = fighter1_data - fighter2_data

    fight_input = pd.DataFrame([differential_data], columns=feature_columns)
    probability = model.predict_proba(fight_input)[0]
    print("Probability of outcomes (Fighter 1 wins, Fighter 2 wins):", probability)
    predicted_winner = "Fighter 1 wins" if probability[0] > 0.5 else "Fighter 2 wins"
    confidence = max(probability)
    print(f"Predicted fight result: {predicted_winner} with {confidence*100:.2f}% confidence")
    print("========================================================================")
    
#======================================================================================================================
def train_model():
    filepath_ml_data = 'data/masterMLpublic.csv'
    
    # Try looking in 'data/masterMLpublic.csv' or fallback to 'data/data.csv' or others if we need
    # Since we reorganized, earlier I saw the file named `Machine Learning Models Weights - Sheet1.csv`.
    # Wait, in the README it said: `dataset taken from (https://... {masterMLpublic.csv})`. I'll try to load UFC/ufc-master.csv or data/data.csv.
    # Actually wait. Let me just use the actual file path of the data that's in the repo right now.
    import os
    if os.path.exists('data/data.csv'):
        filepath_ml_data = 'data/data.csv'
    elif os.path.exists('../data/data.csv'):
        filepath_ml_data = '../data/data.csv'
    
    print(f"Loading data from {filepath_ml_data}")
    full_data = load_data(filepath_ml_data)
    if full_data is None:
        print("Data loading failed. Cannot train model.")
        return None, None
    
    # PREPROCESS
    print("Preprocessing data...")
    full_data_preprocessed = preprocess_data(full_data)
    if 'fighter' not in full_data_preprocessed.columns:
        print("Error: 'fighter' column not found after preprocessing. Aborting.")
        return None, None
    
    print("Data is clean. Proceeding with model training...")
    full_data_reduced = full_data_preprocessed[important_features + ['result']]

    # SPLIT
    train_data, test_data = train_test_split(full_data_reduced, test_size=0.10, random_state=42)
    X_train = train_data.drop(['result'], axis=1)
    Y_train = train_data['result']

    global global_feature_columns
    global_feature_columns = X_train.columns

    # TRAIN
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, Y_train)
    # display_feature_importance(model, X_train.columns)
    
    return model, full_data_preprocessed

#======================================================================================================================
def predict_matchup(fighter1_name, fighter2_name, model, preprocessed_data):
    fighter1_name = fighter1_name.strip().lower()
    fighter2_name = fighter2_name.strip().lower()
    
    fighter1_data = get_fighter_data(fighter1_name, preprocessed_data)
    fighter2_data = get_fighter_data(fighter2_name, preprocessed_data)
    
    differential_data = fighter1_data - fighter2_data
    fight_input = pd.DataFrame([differential_data], columns=global_feature_columns)
    probability = model.predict_proba(fight_input)[0]
    
    predicted_winner = fighter1_name if probability[0] > 0.5 else fighter2_name
    predicted_winner = predicted_winner.capitalize()
    confidence = max(probability)
    
    return predicted_winner, confidence

#======================================================================================================================
def main():
    model, preprocessed_data = train_model()
    if model is None:
        return
    
    #INPUT PREDICTION
    while True:
        fighter1_name = input("Enter first fighter name: ").strip().lower()
        if fighter1_name == 'end':
            break
        fighter2_name = input("Enter second fighter name: ").strip().lower()
        if fighter2_name == 'end':
            break
        
        winner, conf = predict_matchup(fighter1_name, fighter2_name, model, preprocessed_data)
        print(f"Predicted fight result: {winner} wins with {conf*100:.2f}% confidence")
        print("========================================================================")

if __name__ == '__main__':
    main()