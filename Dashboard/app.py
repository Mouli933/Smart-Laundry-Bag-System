from flask import Flask, render_template, jsonify
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import os

app = Flask(__name__)

print("\n=========================================")
print("🔵 STARTING SMART LAUNDRY FLASK SERVER")
print("=========================================\n")

# -------------------------------------------------------------
# 1️⃣ GOOGLE DRIVE LOGIN USING SERVICE ACCOUNT
# -------------------------------------------------------------
try:
    print("🔐 Authenticating Google Drive using Service Account...")

    gauth = GoogleAuth()

    gauth.settings['client_config_backend'] = 'service'
    gauth.settings['service_config'] = {
        "client_json_file_path": "service_key.json",
        "client_user_email": "testservice@my-project-41379-476713.iam.gserviceaccount.com"
    }

    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    print("✅ Service Account Authentication Successful!\n")

except Exception as e:
    print("❌ Google Drive Authentication FAILED:", e)
    exit()



# -------------------------------------------------------------
# 2️⃣ GOOGLE DRIVE FOLDER ID
# -------------------------------------------------------------
FOLDER_ID = "1LE5emx7gzrbfjUe8jM9Onx2bu_T6o2SE"
print(f"📁 Reading from Google Drive Folder: {FOLDER_ID}\n")


# -------------------------------------------------------------
# 3️⃣ FETCH LATEST metadata_*.json FILE
# -------------------------------------------------------------
def get_latest_metadata():

    print("\n========== FETCHING METADATA ==========\n")

    try:
        file_list = drive.ListFile(
            {'q': f"'{FOLDER_ID}' in parents and trashed=false"}
        ).GetList()
    except Exception as e:
        print("❌ ERROR: Cannot fetch file list:", e)
        return {"error": "Drive fetch failed"}

    print("📄 Files found:")
    for f in file_list:
        print("  •", f['title'])

    # Filter metadata files
    meta_files = [f for f in file_list if f['title'].startswith("metadata_")]

    if not meta_files:
        print("⚠️ No metadata_*.json files found!")
        return {
            "Tag_ID": "-",
            "Rack_Level": "-",
            "Box_Number": "-",
            "Timestamp": "-",
            "Video_File": "-"
        }

    print("\n🔍 Metadata files:")
    for f in meta_files:
        print("  ✔", f['title'])

    # Sort to get newest file
    meta_files.sort(key=lambda f: f['title'], reverse=True)
    latest = meta_files[0]

    print("\n➡ Latest File:", latest['title'])

    # Download JSON
    try:
        latest.GetContentFile("latest.json")
        with open("latest.json", "r") as f:
            data = json.load(f)
        os.remove("latest.json")
    except Exception as e:
        print("❌ ERROR reading latest JSON:", e)
        return {"error": "JSON read failed"}

    print("\n📤 Returning data:", data)
    print("\n=========================================\n")

    return {
        "Tag_ID": data.get("Tag_ID", "-"),
        "Rack_Level": data.get("Rack_Level", "-"),
        "Box_Number": data.get("Box_Number", "-"),
        "Timestamp": data.get("Timestamp", "-"),
        "Video_File": data.get("Video_File", "-")
    }


# -------------------------------------------------------------
# 4️⃣ ROUTES
# -------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data")
def get_data():
    return jsonify(get_latest_metadata())


# -------------------------------------------------------------
# 5️⃣ RUN FLASK SERVER
# -------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Flask running at http://localhost:5000")
    app.run(port=5000, debug=True)
