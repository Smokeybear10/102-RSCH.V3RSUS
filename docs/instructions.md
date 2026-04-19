# Quick Start Instructions

## What I Just Changed

✅ The notebook now looks for `ufc-master.csv` **directly** (no archive folder needed!)

## How to Run in Google Colab (Easiest)

### Step 1: Upload the CSV to Google Drive

1. Go to https://drive.google.com/
2. Click **"+ New"** → **"File upload"**
3. Select `ufc-master.csv` from your computer
   - It's located at: `/Users/thomasou/Github/UFC/archive/ufc-master.csv`
4. Upload it to **any folder** in your Google Drive (or just the root)

### Step 2: Upload the Notebook to Colab

1. Go to https://colab.research.google.com/
2. Click **"Upload"** (or File → Upload notebook)
3. Select `cis5450UFCProjectGroup118.ipynb`

### Step 3: Set the Path

In the notebook, find **Cell 5** and change this line to match where you put the CSV:

```python
os.chdir('/content/drive/MyDrive')  # If you uploaded to Drive root
```

**OR if you put it in a folder:**

```python
os.chdir('/content/drive/MyDrive/UFC')  # If you created a UFC folder
```

### Step 4: Run Everything

1. Click **"Runtime"** → **"Run all"**
2. When prompted, click **"Connect to Google Drive"** and allow access
3. Wait 2-3 minutes for everything to run
4. Scroll through to see your results!

---

## Common Paths

Choose the one that matches where you uploaded the CSV:

| Where You Uploaded | Path to Use in Cell 5 |
|---|---|
| Directly in "My Drive" | `os.chdir('/content/drive/MyDrive')` |
| In a "UFC" folder | `os.chdir('/content/drive/MyDrive/UFC')` |
| In a "CIS5450" folder | `os.chdir('/content/drive/MyDrive/CIS5450')` |
| In "Colab Notebooks" folder | `os.chdir('/content/drive/MyDrive/Colab Notebooks')` |

---

## Not Sure Where You Put It?

After Cell 5 runs, add a new cell and run:

```python
import os
print("Your folders:", os.listdir('/content/drive/MyDrive'))
```

This will show you all your folders. Then use the matching path!

---

## Expected Results

When it runs successfully, you'll see:

- ✅ Data loaded: ~6,500 fights
- ✅ Models trained with ~63-67% accuracy
- ✅ Multiple visualizations
- ✅ Feature importance rankings
- ✅ ROC curves comparing models

---

## Need Help?

If you see an error about file not found:
1. Check that `ufc-master.csv` is uploaded to your Drive
2. Update the path in Cell 5 to match where you put it
3. Re-run the notebook

---

**Your notebook is ready to submit after you run it!** 🚀
