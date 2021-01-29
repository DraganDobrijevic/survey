import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("user") or not request.form.get("gender"):
        return render_template("error.html", message="You must fill out the form correctly.")
    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("user"), request.form.get("gender"), request.form.get("country")))

    return redirect("/sheet", code=302)

@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        if not file:
            return render_template("error.html", message="no csv file")
        reader = csv.reader(file)
        data = list(reader)
        return render_template("sheet.html", data=data)


