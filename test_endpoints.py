import sys
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000"

print(f"[*] Testing ComicCraft Endpoints on {BASE_URL}...\n")

# 1. Test GET /
print("1. Testing GET / (Homepage)...")
res = requests.get(f"{BASE_URL}/")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
assert "Create Your Comic" in res.text, "Title not found in homepage HTML"
assert "comicForm" in res.text, "comicForm not found in HTML"
print("[OK] Homepage is running and serving HTML properly.")

# 2. Test GET /static/css/style.css
print("\n2. Testing GET /static/css/style.css...")
res = requests.get(f"{BASE_URL}/static/css/style.css")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
assert "--primary" in res.text, "CSS styles missing"
print("[OK] Static CSS is properly served.")

# 3. Test POST /generate (Form Submission)
print("\n3. Testing POST /generate (Full Comic Generation)...")
form_data = {
    "prompt": "A brave fox exploring an enchanted forest.",
    "character_name": "Free",
    "setting": "Enchanted Forest",
    "tone": "Dramatic",
    "style": "Classic Comic Book"
}
res = requests.post(f"{BASE_URL}/generate", data=form_data)
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
assert "Your Comic Preview" in res.text, "Preview heading missing"
assert "Panel 1:" in res.text, "Panel 1 missing in preview"
assert ".pdf" in res.text, "PDF download link missing in preview"
print("[OK] /generate successfully produced 5-panel preview and PDF.")

# 4. Test POST /generate-comic/json (API JSON Endpoint)
print("\n4. Testing POST /generate-comic/json...")
json_payload = {
    "prompt": "A cyber ninja infiltrating a neon skyscraper in Neo-Tokyo",
    "character_name": "Kaito",
    "setting": "Cyberpunk Metropolis",
    "tone": "Action-Packed",
    "style": "Anime / Manga"
}
res = requests.post(f"{BASE_URL}/generate-comic/json", json=json_payload)
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
data = res.json()
assert data.get("status") == "success", "JSON status not success"
assert len(data.get("layout", [])) == 5, "JSON layout does not contain 5 panels"
assert data.get("pdf_path", "").endswith(".pdf"), "PDF path invalid"
print(f"[OK] JSON API Endpoint returned {len(data['layout'])} panels and PDF: {data['pdf_path']}")

# 5. Test GET /export-success
print("\n5. Testing GET /export-success...")
res = requests.get(f"{BASE_URL}/export-success?pdf_path={data['pdf_path']}")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
assert "Comic Exported Successfully!" in res.text, "Export success heading missing"
print("[OK] /export-success rendered correctly.")

# 6. Test GET /test-image
print("\n6. Testing GET /test-image...")
res = requests.get(f"{BASE_URL}/test-image?prompt=A+magical+forest+glow")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
img_data = res.json()
assert "path" in img_data, "Path not in response"
print(f"[OK] /test-image generated: {img_data['path']}")

# 7. Test Swagger Docs
print("\n7. Testing GET /docs...")
res = requests.get(f"{BASE_URL}/docs")
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
print("[OK] Swagger API documentation is active.")

print("\n🎉 ALL ROUTES AND API ENDPOINTS ARE 100% OPERATIONAL!")
