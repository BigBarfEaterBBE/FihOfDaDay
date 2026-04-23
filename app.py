from flask import Flask, render_template, jsonify
import datetime
import json

app = Flask(__name__)

with open("data/fish_data_clean.json", "r", encoding="utf-8") as f:
    fish_list = json.load(f)

START_DATE = datetime.date(2026,4,20)

def get_fish_of_the_day():
    days = (datetime.date.today() - START_DATE).days
    return fish_list[days % len(fish_list)]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/fish-of-the-day")
def fish_api():
    return jsonify(get_fish_of_the_day())

if __name__ == "__main__":
    app.run(debug=True)