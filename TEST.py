
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"  # change if deploying

CONTACTS_FILE = "Contacts.csv"
RECYCLE_FILE = "recycle_bin.csv"

def ensure_files():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "w", newline="", encoding="utf-8") as f:
            pass
    if not os.path.exists(RECYCLE_FILE):
        with open(RECYCLE_FILE, "w", newline="", encoding="utf-8") as f:
            pass

def read_rows(filename):
    ensure_files()
    rows = []
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            rows.append(row)
    return rows

def write_rows(filename, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def append_row(filename, row):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def contact_exists(name, number):
    rows = read_rows(CONTACTS_FILE)
    for r in rows:
        if len(r) < 2:
            continue
        if r[0].strip().lower() == name.strip().lower() or r[1].strip() == number.strip():
            return True
    return False

def clean_recycle_bin():
    rows = read_rows(RECYCLE_FILE)
    kept = []
    now = datetime.now()
    for r in rows:
        if len(r) < 3:
            kept.append(r)
            continue
        try:
            dt = datetime.strptime(r[2], "%Y-%m-%d %H:%M:%S")
            if (now - dt) < timedelta(days=30):
                kept.append(r)
        except ValueError:
            kept.append(r)
    write_rows(RECYCLE_FILE, kept)

def valid_number(num):
    n = num.strip()
    return n.isdigit() and 7 <= len(n) <= 15

@app.before_request
def before_every_request():
    ensure_files()
    clean_recycle_bin()

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()
    rows = read_rows(CONTACTS_FILE)
    contacts = []
    for r in rows:
        if len(r) < 2:
            continue
        name, number = r[0], r[1]
        if q:
            if q.lower() in name.lower() or q in number:
                contacts.append({"name": name, "number": number})
        else:
            contacts.append({"name": name, "number": number})
    return render_template("index.html", contacts=contacts, q=q)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    number = request.form.get("number", "").strip()
    if not name or not number:
        flash("Name and Number are required.", "danger")
        return redirect(url_for("index"))
    if not valid_number(number):
        flash("Invalid number. Use digits only (7-15 digits).", "danger")
        return redirect(url_for("index"))
    if contact_exists(name, number):
        choice = request.form.get("force_add", "no")
        if choice != "yes":
            flash("Contact already exists! Click 'Add Anyway' to force add.", "warning")
            return redirect(url_for("index", q=name))
    append_row(CONTACTS_FILE, [name, number])
    flash("Contact saved successfully!", "success")
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete():
    key = request.form.get("key", "").strip()
    if not key:
        flash("Provide a Name or Number to delete.", "danger")
        return redirect(url_for("index"))
    rows = read_rows(CONTACTS_FILE)
    kept, deleted = [], []
    for r in rows:
        if len(r) < 2: 
            continue
        if r[0].strip().lower() == key.lower() or r[1].strip() == key:
            deleted.append(r)
        else:
            kept.append(r)
    if not deleted:
        flash("Contact not found.", "warning")
        return redirect(url_for("index"))
    write_rows(CONTACTS_FILE, kept)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for d in deleted:
        append_row(RECYCLE_FILE, [d[0], d[1], ts])
    flash(f"Deleted {len(deleted)} contact(s).", "success")
    return redirect(url_for("index"))

@app.route("/recycle-bin", methods=["GET"])
def recycle_bin():
    rows = read_rows(RECYCLE_FILE)
    bin_items = []
    for r in rows:
        if len(r) >= 2:
            deleted_at = r[2] if len(r) > 2 else "N/A"
            bin_items.append({"name": r[0], "number": r[1], "deleted_at": deleted_at})
    return render_template("recycle_bin.html", items=bin_items)

@app.route("/restore", methods=["POST"])
def restore():
    key = request.form.get("key", "").strip()
    if not key:
        flash("Provide a Name or Number to restore.", "danger")
        return redirect(url_for("recycle_bin"))
    rows = read_rows(RECYCLE_FILE)
    kept = []
    restored = 0
    for r in rows:
        if len(r) < 2:
            kept.append(r)
            continue
        if r[0].strip().lower() == key.lower() or r[1].strip() == key:
            if not contact_exists(r[0], r[1]):
                append_row(CONTACTS_FILE, [r[0], r[1]])
                restored += 1
        else:
            kept.append(r)
    write_rows(RECYCLE_FILE, kept)
    if restored:
        flash(f"Restored {restored} contact(s).", "success")
    else:
        flash("Nothing restored (maybe already existed or not found).", "warning")
    return redirect(url_for("recycle_bin"))

@app.route("/recycle-delete", methods=["POST"])
def recycle_delete():
    key = request.form.get("key", "").strip()
    if not key:
        flash("Provide a Name or Number to permanently delete.", "danger")
        return redirect(url_for("recycle_bin"))
    rows = read_rows(RECYCLE_FILE)
    kept = []
    deleted = 0
    for r in rows:
        if len(r) < 2:
            kept.append(r)
            continue
        if r[0].strip().lower() == key.lower() or r[1].strip() == key:
            deleted += 1
        else:
            kept.append(r)
    write_rows(RECYCLE_FILE, kept)
    if deleted:
        flash(f"Permanently deleted {deleted} contact(s) from recycle bin.", "success")
    else:
        flash("Contact not found in recycle bin.", "warning")
    return redirect(url_for("recycle_bin"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
