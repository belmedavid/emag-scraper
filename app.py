from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = "somesecretkey"


@app.route("/")
def route_index():
    note_text = None
    if "note" in session:
        note_text = session['note']
    return render_template('index2.html', note=note_text)


@app.route("/edit_note")
def route_edit():
    note_text = None
    if "note" in session:
        note_text = session["note"]
    return render_template("edit.html", note=note_text)


@app.route("/edit_note", methods=['POST'])
def route_save():
    session["note"] = request.form["note"]
    return redirect("/")


