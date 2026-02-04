# Civil Engineering Insight Studio

A professional Streamlit web application that analyzes images of civil engineering structures using Google Generative AI (Gemini) to generate detailed engineering reports.

## Features

✓ **Two Output Modes:**
- **Text Report**: Professional free-text engineering analysis with structure type, materials, dimensions, construction methodology, project progress, challenges, and recommendations
- **Structured JSON**: Machine-readable JSON output matching a defined schema for programmatic integration

✓ **Modern Gemini API**: Uses `genai.GenerativeModel()` with `model.generate_content()` for optimal performance

✓ **Native Image Support**: Passes PIL images directly to Gemini (not base64 strings or markdown links)

✓ **User Notes**: Optional context/questions from the user for customized analysis

✓ **Image Preview**: Real-time display of uploaded images before analysis

✓ **Professional Prompts**: Engineered system prompts for civil engineering expertise

## Requirements

- Python 3.8+
- Google Gemini API key
- Dependencies: `streamlit`, `google-generativeai`, `python-dotenv`, `pillow`

## Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir CivilEngineeringInsightStudio
   cd CivilEngineeringInsightStudio
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Google API key:**
   - Create a `.env` file in the project directory
   - Add your Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     GEMINI_MODEL=gemini-2.5-flash
     ```
   - Get a free API key at: https://ai.google.dev/

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Upload an Image**: Click "Upload an image" and select a JPG, JPEG, or PNG file of a civil engineering structure
2. **Add Optional Notes**: Provide any context or specific questions (optional)
3. **Select Output Mode**:
   - "Text Report" for human-readable engineering analysis
   - "Structured JSON" for machine-readable JSON data
4. **Click "Describe Structure"**: The app will analyze the image using Gemini AI
5. **View Results**:
   - Text Report: Shows markdown-formatted engineering description
   - Structured JSON: Shows both raw JSON and a human-readable summary

## Project Structure

```
CivilEngineeringInsightStudio/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # API key configuration (create this)
└── README.md                 # This file
```

## Configuration

### Environment Variables

- **GOOGLE_API_KEY** (required): Your Google Gemini API key
- **GEMINI_MODEL** (optional): Model name (default: `gemini-1.5-flash`)

### Available Models

- `gemini-2.5-flash` (latest, recommended)
- `gemini-2.5-pro`
- `gemini-2.0-flash`
- `gemini-2.0-flash-001`
- `gemini-2.0-flash-lite`
- `gemini-2.0-pro`
- And others...

Check available models: `python list_available_models.py`

## API Reference

### Core Functions

#### `get_gemini_response(user_notes: str, pil_image: Image.Image, prompt: str) -> str`
Sends a PIL image and prompt to Gemini, returns text response.

**Parameters:**
- `user_notes`: Optional user context/questions
- `pil_image`: PIL Image object (converted to RGB)
- `prompt`: System prompt with analysis instructions

**Returns:**
- Text response from the model

#### `get_gemini_json_response(user_notes: str, pil_image: Image.Image, base_prompt: str) -> str`
Sends a PIL image and prompt to Gemini, returns JSON-formatted response.

**Parameters:**
- `user_notes`: Optional user context/questions
- `pil_image`: PIL Image object (converted to RGB)
- `base_prompt`: JSON schema prompt (JSON_REPORT_PROMPT)

**Returns:**
- Raw JSON string from the model

#### `parse_json_from_response(response_text: str) -> dict`
Parses JSON from model response, handling markdown code blocks and wrapped JSON.

**Parameters:**
- `response_text`: Raw text response from model

**Returns:**
- Parsed JSON dictionary

### JSON Schema

The Structured JSON output follows this schema:

```json
{
  "StructureType": "string",
  "Materials": [
    {
      "material": "string",
      "evidence": "string"
    }
  ],
  "Dimensions": {
    "estimates": [
      {
        "element": "string",
        "estimate_m": "number or null",
        "range_m": "string",
        "confidence": "string (high|medium|low)",
        "assumptions": "string"
      }
    ],
    "notes": "string"
  },
  "ConstructionMethodology": ["string"],
  "ProjectProgress": {
    "completed": ["string"],
    "pending": ["string"],
    "confidence": "string"
  },
  "EngineeringChallenges": ["string"],
  "Recommendations": ["string"],
  "Uncertainties": ["string"]
}
```

## Troubleshooting

### "Model not found" Error
- Check your API key is valid in `.env`
- Try a different model: `GEMINI_MODEL=gemini-1.5-pro`
- Run `python list_available_models.py` to see available models

### "No module named 'streamlit'"
- Install dependencies: `pip install -r requirements.txt`

### Image not displaying
- Ensure the uploaded file is a valid JPG, JPEG, or PNG
- File size should be reasonable (< 20MB)

### JSON parsing errors
- The model may have included explanatory text before the JSON
- The `parse_json_from_response()` function handles most cases automatically
- Check the raw output in error messages

## Notes

- The app uses the deprecated `google.generativeai` package (with a FutureWarning). This still works but you can migrate to `google.genai` in the future.
- Visual-only analysis has inherent limitations; results should be verified by qualified engineers
- The app respects the Gemini API usage limits and quotas

## Academic Use

This project is suitable for:
- Computer Science / Engineering final-year projects
- AI/ML course demonstrations
- Web application development portfolios
- API integration examples

## License

Freely available for educational and commercial use.

## Support

For issues with:
- **Google Gemini API**: https://ai.google.dev/
- **Streamlit**: https://docs.streamlit.io/
- **Python**: https://www.python.org/doc/

---

**Created**: February 2026
**Version**: 2.0 (Refactored with native image support and dual output modes)
