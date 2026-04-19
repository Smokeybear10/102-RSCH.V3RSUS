# CIS5450 UFC Fight Prediction Project

## Dataset Files

The notebook uses the following CSV file:

- **`ufc-master.csv`** - Main dataset containing:
  - Fight outcomes (Winner column)
  - Red and Blue fighter statistics (prefixed with Red/Blue)
  - Fight context (Date, Location, Weight Class, Title Bout status)
  - Betting odds
  - Pre-calculated differential features (columns ending in 'Dif')

### Dataset Structure
- **6,528 fights** (rows)
- **118 features** (columns)
- Data includes UFC fights with comprehensive fighter statistics

## Key Columns

### Fighter Stats (Red/Blue prefix)
- `RedFighter` / `BlueFighter` - Fighter names
- `RedWins` / `BlueWins` - Career wins
- `RedLosses` / `BlueLosses` - Career losses
- `RedHeightCms` / `BlueHeightCms` - Height in centimeters
- `RedReachCms` / `BlueReachCms` - Reach in centimeters
- `RedAvgSigStrLanded` / `BlueAvgSigStrLanded` - Average significant strikes
- `RedAvgTDLanded` / `BlueAvgTDLanded` - Average takedowns
- `RedAvgSubAtt` / `BlueAvgSubAtt` - Average submission attempts
- `RedStance` / `BlueStance` - Fighting stance

### Fight Context
- `Date` - Fight date
- `Location` - Fight location
- `WeightClass` - Division
- `TitleBout` - Boolean for title fight
- `Winner` - "Red" or "Blue"

### Existing Differentials
- `WinDif`, `LossDif` - Win/loss differentials
- `HeightDif`, `ReachDif` - Physical differentials
- `SigStrDif`, `AvgTDDif`, `AvgSubAttDif` - Performance differentials

## Running the Notebook

### In Google Colab:
1. Go to https://colab.research.google.com/
2. Upload `cis5450UFCProjectGroup118.ipynb`
3. Upload `ufc-master.csv` to your Google Drive (anywhere - just remember the folder name)
4. Update the path in Cell 5 to match where you uploaded the CSV
5. Run all cells

### Locally:
1. Ensure you're in the `/Users/thomasou/Github/UFC` directory
2. Make sure `ufc-master.csv` exists (or update the path in Cell 8)
3. Run the notebook cells in order
4. The notebook will automatically:
   - Load the data
   - Create additional differential features
   - Train 3 models (Logistic Regression, Random Forest, XGBoost)
   - Evaluate and compare performance

## Expected Performance

- **Baseline (Logistic Regression)**: ~60-65% accuracy
- **Random Forest**: ~63-68% accuracy
- **XGBoost**: ~64-70% accuracy

All models significantly outperform random guessing (50%).
