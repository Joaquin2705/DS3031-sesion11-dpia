# app.py  —  pip install -r requirements.txt ; FLASK_APP=app python3 -m flask run --port 5050
import sqlite3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
db = sqlite3.connect("lab.db", check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS registro (
    id        INTEGER PRIMARY KEY,
    nombres   TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    correo    TEXT NOT NULL,
    telefono  TEXT,
    creado_en TEXT DEFAULT CURRENT_TIMESTAMP)""")

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

@app.post("/registro")
def registrar():
    d = request.get_json()
    db.execute("INSERT INTO registro (nombres, apellidos, correo, telefono) "
               "VALUES (?, ?, ?, ?)",
               (d["nombres"], d["apellidos"], d["correo"], d.get("telefono")))
    db.commit()
    return {"ok": True}, 201

@app.get("/registros")
def listar():
    return jsonify(db.execute("SELECT * FROM registro").fetchall())
