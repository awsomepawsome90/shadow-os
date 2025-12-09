# ICD-10 Setup - Quick Start Guide

## 30-Second Setup

```bash
python setup_icd10.py
```

That's it. The script handles everything else.

## What Happens

1. ✅ Downloads 74,719 official ICD-10 codes from CDC
2. ✅ Formats them for your vector database
3. ✅ Loads them into ChromaDB
4. ✅ Verifies everything works

Takes ~5-10 minutes.

## After Setup

### Start your backend:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Test it works:
```bash
python test_brain.py
```

### Try medical queries:
Edit `test_brain.py` and change the `TEST_QUESTION`:
```python
TEST_QUESTION = "What is Type 2 Diabetes?"
TEST_QUESTION = "What ICD code is used for pneumonia?"
TEST_QUESTION = "Explain code E11.9"
```

## Files Created

| File | Purpose |
|------|---------|
| `data/icd10cm_official_raw.txt` | Raw CDC download (backup) |
| `data/icd10_complete_database.txt` | Formatted medical codes |
| `data/chroma_db/` | Updated with ICD-10 data |

## Nothing Broke

Your existing code is **completely unchanged**:
- `backend/main.py` ✅ Works as before
- `backend/ingest_docs.py` ✅ Works as before
- `test_brain.py` ✅ Works as before
- All API endpoints ✅ Work as before

## One Problem?

### Download failed?
- Check internet connection
- Try again—CDC server might be busy
- No internet? See [ICD10_INTEGRATION_SUMMARY.md](ICD10_INTEGRATION_SUMMARY.md)

### Module not found?
```bash
pip install requests
```

### Still stuck?
See [ICD10_INTEGRATION_SUMMARY.md](ICD10_INTEGRATION_SUMMARY.md) for troubleshooting

## Need to Undo?

```python
# In Python or via the API
POST /db/reset
```

Then:
1. Put your own .txt/.pdf files in `data/`
2. Run `python backend/ingest_docs.py`
3. Done—system works exactly as before

## Next Steps

1. Run setup: `python setup_icd10.py`
2. Start backend: `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000`
3. Test it: `python test_brain.py`
4. Query it: Try medical questions!

That's all!
