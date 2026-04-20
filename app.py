from flask import Flask, render_template, jsonify
import datetime
import json

app = Flask(__name__)

with open("fish_data.json", "r") as f:
    fish_list = json.load(f)

def get_fish_of_the_day():
    today = datetime.date.today()
    days_since_start = (today - datetime.date(2026, 4, 20)).days
    index = days_since_start % len(fish_list)
    return fish_list[index]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/fish-of-the-day")
def fish_api():
    return jsonify(get_fish_of_the_day())

if __name__ == "__main__":
    app.run(debug=True)