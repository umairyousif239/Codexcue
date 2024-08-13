import random
import string
import json

from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}

# Function to generate a random short URL
def generate_short_url(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

# Function to generate a random short URL
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["original_url"]
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()
        shortened_urls[short_url] = original_url
        with open("generatedURLs.json", "w") as f:
            json.dump(shortened_urls, f)
        return f"Shortened URL: {request.url_root}{short_url}" 
    return render_template ("index.html")

# Function to redirect to the original URL
@app.route("/<short_url>")
def redirect_url(short_url):
    original_url = shortened_urls.get(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return "URL Not Found", 404

# Main
if __name__ == "__main__":
    with open("generatedURLs.json", "r") as f:
        shortened_urls = json.load(f)
    app.run(debug=True)