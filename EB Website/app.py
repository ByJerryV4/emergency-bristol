from flask import Flask, render_template, request, jsonify
from requests_toolbelt import MultipartEncoder
import requests, json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

WEBHOOK_URL = "https://discord.com/api/webhooks/1387093169425879060/RsHmcqVTlCwn-tJMRTft_nHmAzt-pjSvjE_ZZjkC0J-PrVbWM2PYyTNWUeoHwtl0XkIK"

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        payload = {
            "embeds": [{
                "title": "📬 Contact Form Submission",
                "fields": [
                    {"name": "Discord Username", "value": data['username'], "inline": True},
                    {"name": "Reason", "value": data['reason'], "inline": True},
                    {"name": "Message", "value": data['message'], "inline": False}
                ],
                "color": 16711680
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        return jsonify(success=True)
    return render_template('pages/contact.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        data = request.form
        file = request.files.get('evidence')

        form_type = request.args.get("type", "player")
        embed_title = "🚨 Player Report" if form_type == "player" else "🐞 Bug Report"

        fields = [
            {"name": "Discord Username", "value": data['username'], "inline": True},
            {"name": "Reason", "value": data.get('report_reason') or data.get('bug_type'), "inline": True},
            {"name": "Message", "value": data['message'], "inline": False}
        ]

        payload = {
            "embeds": [{
                "title": embed_title,
                "fields": fields,
                "color": 16711680,
                "footer": {"text": "Emergency Bristol Report"},
            }]
        }

        if file:
            # Embed file in message and link to it
            file_url = f"attachment://{file.filename}"
            payload["embeds"][0]["fields"].append({
                "name": "📎 Evidence File",
                "value": f"[Click to view attachment]({file_url})",
                "inline": False
            })
            # Optional preview if image
            if file.mimetype.startswith("image/"):
                payload["embeds"][0]["image"] = {"url": file_url}

            m = MultipartEncoder(
                fields={
                    'payload_json': json.dumps(payload),
                    'file': (file.filename, file.stream, file.mimetype)
                }
            )
            headers = {'Content-Type': m.content_type}
            requests.post(WEBHOOK_URL, data=m, headers=headers)
        else:
            requests.post(WEBHOOK_URL, json=payload)

        return jsonify(success=True)

    return render_template('pages/report.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("pages/404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
