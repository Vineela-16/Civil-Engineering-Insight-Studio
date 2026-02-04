"""
CIVIL ENGINEERING INSIGHT STUDIO - APPLICATION ARCHITECTURE

╔══════════════════════════════════════════════════════════════════════════╗
║                    STREAMLIT WEB APPLICATION FLOW                         ║
╚══════════════════════════════════════════════════════════════════════════╝

USER INTERFACE (Streamlit)
════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                  Civil Engineering Insight Studio                        │
│  🏗️ Upload an image of a civil engineering structure to generate a     │
│     professional analysis.                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Optional: Add any context or specific questions for the analysis       │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ [User notes text area - 80 pixels high]                            │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  Upload an image (jpg, jpeg, png)                                       │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ [Choose File] [Browse]                                           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  [Image Preview if uploaded]                                             │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │        Uploaded image                                            │   │
│  │     (600x400 or responsive)                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  Select output mode:                                                     │
│  ◉ Text Report    ○ Structured JSON                                      │
│                                                                           │
│  ┌─────────────────────┐                                                │
│  │  Describe Structure │                                                │
│  └─────────────────────┘                                                │
│                                                                           │
│  ═══════════════════════════════════════════════════════════════════    │
│  [Results display below - Spinner during processing]                    │
│  ═══════════════════════════════════════════════════════════════════    │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


API ARCHITECTURE (Backend)
════════════════════════════════════════════════════════════════════════════

                         ┌─────────────────────────┐
                         │   .env Configuration    │
                         │  GOOGLE_API_KEY = ***   │
                         │  GEMINI_MODEL = 2.5-fl  │
                         └────────┬────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  genai.configure(api_key)  │
                    └─────────────┬──────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ user_notes: str  │    │ pil_image:       │    │ prompt: str     │
│                  │    │ Image.Image      │    │                 │
│ (context from    │    │                  │    │ (system prompt) │
│  text area)      │    │ (uploaded file   │    │                 │
│                  │    │  converted to    │    │ TEXT_REPORT or  │
│                  │    │  RGB PIL Image)  │    │ JSON_REPORT     │
└────────┬─────────┘    └────────┬─────────┘    └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ get_gemini_response()   │   OR    │ get_gemini_json_response()
                    │ get_gemini_json_response│   OR    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────────────────┐
                    │ model = genai.GenerativeModel()     │
                    │ content = [prompt, notes, image]    │
                    │ response = model.generate_content() │
                    └────────────┬────────────────────────┘
                                 │
                    ┌────────────▼──────────────────┐
                    │  Google Gemini API            │
                    │  Process image + prompt       │
                    │  Return: response.text        │
                    └────────────┬──────────────────┘
                                 │
                    ┌────────────▼──────────────────────┐
                    │  Extract response.text            │
                    │  For JSON: parse_json_from_response
                    └────────────┬──────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
    ┌─────────────┐        ┌──────────────┐       ┌──────────────┐
    │ Text Result │        │ JSON Result  │       │ Error        │
    │             │        │              │       │              │
    │ str (raw)   │        │ str (raw)    │       │ Exception    │
    └────────┬────┘        └───────┬──────┘       └───────┬──────┘
             │                     │                      │
             │            ┌────────▼─────────┐            │
             │            │ parse_json_from_ │            │
             │            │ response()       │            │
             │            └────────┬─────────┘            │
             │                     │                      │
             │            ┌────────▼──────────────┐       │
             │            │ parsed: dict         │       │
             │            └────────┬──────────────┘       │
             │                     │                      │
             ▼                     ▼                      ▼
    ┌─────────────────┐   ┌──────────────────┐  ┌──────────────────┐
    │ st.markdown()   │   │ st.json(parsed)  │  │ st.error()       │
    │ Display as text │   │ Show raw JSON    │  │ Display error    │
    │                 │   │ render_json_     │  │ + helpful hints  │
    │                 │   │ summary()        │  │                  │
    │                 │   │ Human-readable   │  │                  │
    └─────────────────┘   │ summary          │  └──────────────────┘
                          └──────────────────┘


CODE STRUCTURE (app.py)
════════════════════════════════════════════════════════════════════════════

SECTION 1: IMPORTS (lines 1-32)
├── Standard Library: os, json, io
├── Third-party: PIL.Image, streamlit, dotenv
└── Optional: google.generativeai

SECTION 2: CONFIGURATION (lines 34-48)
├── load_dotenv() - Load environment variables
├── GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
├── GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
└── genai.configure(api_key=GOOGLE_API_KEY)

SECTION 3: PROMPTS (lines 50-130)
├── TEXT_REPORT_PROMPT
│   └── Instructions for civil engineering text analysis
└── JSON_REPORT_PROMPT
    └── Instructions for JSON output with schema

SECTION 4: CORE FUNCTIONS (lines 132-340)
├── get_gemini_response(user_notes, pil_image, prompt) -> str
│   ├── Builds content list [prompt, optional notes, PIL image]
│   ├── Calls model.generate_content(content)
│   └── Returns response.text
│
├── get_gemini_json_response(user_notes, pil_image, base_prompt) -> str
│   ├── Similar to above but with low temperature (0.1)
│   ├── Higher max_output_tokens for JSON
│   └── Returns raw JSON string
│
├── parse_json_from_response(response_text) -> dict
│   ├── Try 1: Direct JSON parse
│   ├── Try 2: Extract from markdown code blocks
│   ├── Try 3: Find balanced JSON object
│   └── Return parsed dict or raise ValueError
│
└── render_json_summary(parsed: dict)
    ├── Shows StructureType
    ├── Shows Materials with evidence
    ├── Shows Dimensions with confidence
    ├── Shows Construction Methodology
    ├── Shows Project Progress
    ├── Shows Engineering Challenges
    ├── Shows Recommendations
    └── Shows Uncertainties

SECTION 5: STREAMLIT UI (lines 342-430)
└── main()
    ├── st.set_page_config()
    ├── st.header() - "🏗️ Civil Engineering Insight Studio"
    ├── st.markdown() - Description
    ├── st.text_area() - User notes (key=None, auto-generated)
    ├── st.file_uploader() - Image upload (key="image_uploader")
    ├── Image preview (st.image())
    ├── st.radio() - Output mode selector (key="output_mode")
    ├── st.button() - "Describe Structure" (key="describe_btn")
    └── Results display logic
        ├── If Text Report → st.markdown()
        └── If JSON → st.json() + render_json_summary()


DATA FLOW DIAGRAM
════════════════════════════════════════════════════════════════════════════

User                    Streamlit                    Gemini AI
────                    ─────────                    ─────────

Upload Image    ──────>  File received
                         Convert to PIL Image (RGB)
Add Notes       ──────>  Store text
Select Mode     ──────>  Save choice
Click Button    ──────>  Validate inputs
                         Build content list
                         [prompt, notes, image]
                                            ──────>  Process request
                                                    Analyze image
                                                    Generate response
                         Receive response  <──────
                         Extract text
                         (For JSON: Parse)
                         Render results
Display output  <──────  st.markdown() or st.json()


FUNCTION CALL SEQUENCE
════════════════════════════════════════════════════════════════════════════

USER CLICKS "Describe Structure"
│
├─> if pil_image is None → st.error() → EXIT
│
└─> with st.spinner("Analyzing image..."):
    │
    ├─> if output_mode == "Text Report":
    │   │
    │   └─> result = get_gemini_response(
    │           user_notes or "",
    │           pil_image,
    │           TEXT_REPORT_PROMPT
    │       )
    │       │
    │       ├─> model = genai.GenerativeModel(GEMINI_MODEL)
    │       ├─> content = [prompt, notes?, image]
    │       ├─> response = model.generate_content(content)
    │       └─> return response.text
    │   │
    │   └─> st.success()
    │       st.markdown(result)
    │
    └─> else (JSON mode):
        │
        └─> result = get_gemini_json_response(
                user_notes or "",
                pil_image,
                JSON_REPORT_PROMPT
            )
            │
            ├─> model = genai.GenerativeModel(GEMINI_MODEL)
            ├─> content = [prompt, notes?, image]
            ├─> response = model.generate_content(
            │       content,
            │       generation_config=GenerationConfig(
            │           temperature=0.1,
            │           max_output_tokens=2000
            │       )
            │   )
            └─> return response.text
            │
            ├─> try:
            │   │
            │   └─> parsed = parse_json_from_response(result)
            │       │
            │       ├─> json.loads(result)  # Try 1
            │       ├─> Extract from code block  # Try 2
            │       └─> Find balanced object  # Try 3
            │
            │   st.success()
            │   st.json(parsed)
            │   render_json_summary(parsed)
            │
            └─> except ValueError:
                st.error()
                st.text(result)


CONFIGURATION FLOW
════════════════════════════════════════════════════════════════════════════

Startup (app.py loads):
│
├─> from dotenv import load_dotenv
├─> load_dotenv()  ─────────────>  Reads .env file
│
├─> GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  ───>  AIzaSy...
│
├─> GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
│                                                  ───>  gemini-2.5-flash
│
├─> if GOOGLE_API_KEY and genai:
│   │
│   └─> try:
│       │
│       └─> genai.configure(api_key=GOOGLE_API_KEY)  ──> API Ready
│
└─> Application Ready for Requests


ERROR HANDLING
════════════════════════════════════════════════════════════════════════════

get_gemini_response() exceptions:
├─> RuntimeError("Gemini not configured...")
└─> RuntimeError("Gemini API error: {error_msg}")
    └─> With hints for "not found" / "not supported"

get_gemini_json_response() exceptions:
├─> RuntimeError("Gemini not configured...")
└─> RuntimeError("Gemini API error: {error_msg}")
    └─> With hint to try different model

parse_json_from_response() exceptions:
└─> ValueError("Could not extract valid JSON from response")

Main UI error handling:
├─> if pil_image is None → st.error("Please upload an image first")
├─> try/except around analysis → st.error("Error: {str(e)}")
└─> JSON parse failures → st.error() + st.text(raw)

═══════════════════════════════════════════════════════════════════════════

VERSION: 2.0 (Complete Refactor)
STATUS: PRODUCTION READY
DATE: February 2026
"""
