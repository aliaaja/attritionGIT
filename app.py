from flask import Flask, render_template, request, jsonify
import os

import dagshub
import mlflow

import psycopg2

dagshub.init(repo_owner='rahayuya2005', repo_name='attrition', mlflow=True)


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="attrition",
        user="postgres",
        password=""
    )
    return conn

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/form_prediction')
def predict_page():
    return render_template('form_prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    print("DATA MASUK:", data)

    # 🔥 contoh logika dummy dulu
    age = int(data.get('Age', 0))
    income = int(data.get('MonthlyIncome', 0))

    if age < 30 and income < 4000:
        result = "Berpotensi Resign"
    else:
        result = "Cenderung Bertahan"

    # 🔥 WAJIB pakai JSON
    return jsonify({'result': result})

from flask import jsonify

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()

    age = int(data.get('Age', 0))
    income = int(data.get('MonthlyIncome', 0))
    overtime = data.get('OverTime')
    job_level = int(data.get('JobLevel', 0))
    total_years = int(data.get('TotalWorkingYears', 0))
    result = data.get('result')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions 
        (age, monthly_income, overtime, job_level, total_working_years, result)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (age, income, overtime, job_level, total_years, result))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Data berhasil disimpan ke database!'})

if __name__ == '__main__':
    app.run(debug=True, port=5002)