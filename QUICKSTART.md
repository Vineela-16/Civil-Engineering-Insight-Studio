# QUICK START GUIDE

## What's New in v2.0

Your Civil Engineering Insight Studio has been completely refactored with:
✓ Modern Gemini API (uses `model.generate_content()` with native PIL images)
✓ Two output modes: Text Report & Structured JSON
✓ Robust JSON parsing and human-readable summaries
✓ Complete documentation and test suite

## 30-Second Setup

1. **Verify .env has your API key:**
   ```
   cat .env
   ```
   You should see:
   ```
   GOOGLE_API_KEY=AIzaSy...
   GEMINI_MODEL=gemini-2.5-flash
   ```

2. **Install dependencies (if needed):**
   ```
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```
   streamlit run app.py
   ```

4. **Open browser:**
   ```
   http://localhost:8501
   ```

## What You Can Do Now

### Upload an Image
- Click "Upload an image" 
- Select a JPG, JPEG, or PNG of any civil engineering structure
- Add optional context in the text area

### Choose Output Mode
- **Text Report**: Human-readable analysis with engineering insights
- **Structured JSON**: Machine-readable data matching the schema in `JSON_SCHEMA.json`

### Get Analysis
- Click "Describe Structure"
- Gemini AI analyzes the image and generates:
  * Structure type identification
  * Material detection with evidence
  * Dimension estimates with confidence levels
  * Construction methodology
  * Project progress assessment
  * Engineering challenges
  * Recommendations
  * Uncertainty notes

## Testing Without Streamlit

Want to test the core functions first?

```bash
python test_functions.py
```

This creates a test image, calls both text and JSON modes, and verifies everything works.

## Core Functions

### Text Analysis
```python
result = get_gemini_response(
    user_notes="Any additional context here",
    pil_image=your_image_object,
    prompt=TEXT_REPORT_PROMPT
)
print(result)  # Free-text engineering description
```

### JSON Analysis
```python
json_str = get_gemini_json_response(
    user_notes="Any additional context here",
    pil_image=your_image_object,
    base_prompt=JSON_REPORT_PROMPT
)
parsed = parse_json_from_response(json_str)
print(parsed)  # Python dict with structured data
```

## Files You Need to Know About

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application - THIS IS YOUR APP |
| `.env` | Configuration (API key, model name) |
| `requirements.txt` | Python dependencies |
| `README.md` | Comprehensive documentation |
| `test_functions.py` | Test script to verify functionality |
| `JSON_SCHEMA.json` | Reference for JSON output format |
| `REFACTORING_SUMMARY.md` | Technical details of the refactoring |

## Troubleshooting

**"streamlit: command not found"**
```bash
pip install streamlit
```

**"ModuleNotFoundError: No module named 'google.generativeai'"**
```bash
pip install google-generativeai
```

**"Model 'gemini-2.5-flash' not found"**
- Edit `.env` and try a different model:
  ```
  GEMINI_MODEL=gemini-1.5-pro
  ```
- Or list available models:
  ```bash
  python list_available_models.py
  ```

**"API key invalid"**
- Check `.env` file has correct GOOGLE_API_KEY
- Get a new key: https://ai.google.dev/

## What Changed from Previous Versions

| Before | After |
|--------|-------|
| Sent images as base64 strings | Sends PIL Image objects directly |
| Tried `genai.chat.create()` | Uses `genai.GenerativeModel().generate_content()` |
| Text-only output | Text Report + Structured JSON modes |
| No JSON parsing | Robust JSON extraction and formatting |
| Duplicate widgets | Unique widget keys (no Streamlit errors) |

## Next Steps

1. **Run the app**: `streamlit run app.py`
2. **Upload a real image** of a civil engineering structure
3. **Try both modes** (Text Report and Structured JSON)
4. **Export results** as needed (copy/paste from the UI)

## Tips for Best Results

- **Clear images**: Better image quality = better analysis
- **Multiple angles**: Upload several images to analyze different aspects
- **Provide context**: Use the notes field to ask specific questions
- **Verify results**: AI analysis should be verified by qualified engineers
- **Use JSON mode**: For programmatic integration or data processing

## Documentation

- **Setup & Usage**: See `README.md`
- **API Reference**: See `README.md` (API Reference section)
- **JSON Schema**: See `JSON_SCHEMA.json`
- **Technical Details**: See `REFACTORING_SUMMARY.md`

## Support

- **Gemini API Issues**: https://ai.google.dev/
- **Streamlit Help**: https://docs.streamlit.io/
- **Python Docs**: https://www.python.org/

---

**You're all set! Run `streamlit run app.py` and start analyzing structures.**
