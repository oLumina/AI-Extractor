from flask import Flask, request, jsonify
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)
load_dotenv()

def process_text_and_create_mod_file(natural_language_text: str, parameters_to_extract: list[str], createFile) -> dict | None:
    try:
        now = datetime.now()
        output_filename = f"{now.strftime('%Y%m%d_%H%M%S')}_extracted"
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not configured.")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error while initializing API: {e}")
        return None

    prompt = f"""
You are an expert AI assistant specializing in extracting structured data from technical descriptions.
Your task is to analyze the user's text and extract the values for a given list of parameters.
You must return the result as a single, valid JSON object and nothing else.

INSTRUCTIONS:
1. The keys of the JSON object must be the exact parameter names from the provided list.
2. If a parameter is found, its value should be the corresponding value in the JSON. The value should be a number if it's purely numeric, otherwise a string.
3. If a parameter from the list is NOT found in the text, its value in the JSON must be `null`.
4. Do not include explanations, comments, or any text other than the final JSON object in your response.

---
EXAMPLE 1:
PARAMETERS TO EXTRACT: ["height", "width", "depth", "material"]
USER TEXT: "Create a cabinet with height 2000, wide 1900, and depth 700."
YOUR RESPONSE:
{{
  "height": 2000,
  "width": 1900,
  "depth": 700,
  "material": null
}}
---
EXAMPLE 2:
PARAMETERS TO EXTRACT: ["width", "depth", "drawers", "color"]
USER TEXT: "I need a desk, depth is 60cm and the width is 1.2m. It should have 2 drawers and be made of oak."
YOUR RESPONSE:
{{
  "width": "1.2m",
  "depth": "60cm",
  "drawers": 2,
  "color": null
}}
---

Now, process the following request.

PARAMETERS TO EXTRACT: {json.dumps(parameters_to_extract)}
USER TEXT: "{natural_language_text}"
YOUR RESPONSE:
"""

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        start, end = response_text.find("{"), response_text.rfind("}")
        if start != -1 and end != -1:
            response_text = response_text[start:end+1]

        extracted_data = json.loads(response_text)
        if createFile:
            with open(f"{output_filename}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)

        return extracted_data
    except Exception as e:
        print(f"Error while processing response: {e}")
        return None
    


@app.route('/example-extraction', methods=['GET'])
def example():
    print("--- Real example ---")
    print()

    parameters: dict= ["Height", "Width", "Depth"]

    text = "Create me a cabinet with height 2000 ,wide 1900 ,depth 700 with 2 vertical divider , 2 horizontal divider , and remove part 2 and the part 6 has a double opening door"
   
    model_result = process_text_and_create_mod_file(text, parameters, False)

    output_str = "-- Parameters --\n"
    for parameter in parameters:
        output_str += f"- {parameter}\n"

    output_str += "-- Text --\n"
    output_str += f"{text}\n"

    output_str += "-- Result --\n"
    for key, value in model_result.items():
        output_str += f"{key}: {value}\n"
    
    print(output_str)
    return jsonify({"Parameters": parameters, "Text": text,"Result":model_result}) if output_str else (jsonify({"error": "Error while processing text"}), 500)

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    try:
        data = request.args.to_dict()
        if request.is_json:
            data.update(request.get_json() or {})
        else:
            data.update(request.form.to_dict())
        if not data or 'text' not in data or 'parameters' not in data:
            return jsonify({"error": "Request must include: 'text' (str) and 'parameters' (list[str]/str)"}), 400
        if type(data['parameters']) == str:
            data['parameters'] = [p.strip() for p in data['parameters'].split(',') if p.strip()]
        result = process_text_and_create_mod_file(data['text'], data['parameters'], True)
        print(result if result else "Error while processing text")
        return jsonify(result) if result else (jsonify({"error": "Error while processing text"}), 500)
    except Exception:
        return jsonify({"error": "Error while processing text"}), 500


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=3000)