# 🧠 Parameter Extraction API

A **Flask API** for automatically extracting structured parameters from natural language text using the **Google Gemini** model.
This service allows you to dynamically define a list of parameters to extract and returns a clean JSON object as output.

---

## 🚀 Project Structure

```
.
├── api.py                                   # Main script (Flask + Google Gemini)
├── requirements.txt                         # Project dependencies
├── AI-Extractor.postman_collection.json  # Postman test collection
├── .env                                     # Create this file and add: GOOGLE_API_KEY = (your key)
└── README.md
```

---

## ⚙️ Requirements

* Python **3.10+**
* A **Google AI Studio** account with access to the Gemini API
* `.env` file containing your Google API key

---

## 📦 Installation

1. **Clone the repository and navigate to the project directory:**

   ```bash
   git clone https://github.com/oLumina/AI-Extractor
   cd AI-Extractor
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the project root and add your Google API key:**

   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

---

## ▶️ Running the API

Run the Flask server locally:

```bash
python api.py
```

By default, the API will be available at:

```
http://localhost:3000
```

---

## 🧩 Endpoints

### `GET /extrair-parametros-exemplo`

Returns a predefined example of parameter extraction.

**Example request:**

```
GET http://localhost:3000/extrair-parametros-exemplo
```

**Response:**

```json
{
  "Parametros": ["altura", "largura", "profundidade"],
  "Texto": "Create me a cabinet with height 2000 ,wide 1900 ,depth 700 ...",
  "resultado": {
    "altura": 2000,
    "largura": 1900,
    "profundidade": 700
  }
}
```

---

### `POST /extrair-parametros`

Extracts the specified parameters from a custom natural language text.
The result is also saved as a `.json` file in the current directory.

**Request body (JSON or form-data):**

```json
{
  "texto": "Create a table 80cm high, 120cm wide and 60cm deep",
  "parametros": ["altura", "largura", "profundidade"]
}
```

**Response:**

```json
{
  "altura": "80cm",
  "largura": "120cm",
  "profundidade": "60cm"
}
```

**Alternative query string:**

```
GET /extrair-parametros?texto=...&parametros=altura,largura,profundidade
```

---

## 🧰 Technical Details

* **Framework:** Flask
* **LLM:** Google Gemini (`gemini-2.5-pro`)
* **Environment:** `.env` loaded via `python-dotenv`
* **Persistence:** Optional (`.json` output saved locally)
* **Error handling:** API initialization, invalid JSON, missing parameters

---

## 🧪 Testing with Postman

A Postman collection is included with all routes and ready-to-run examples.
Import it into Postman and update the `base_url` variable if needed.
