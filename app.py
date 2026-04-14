from flask import Flask, render_template, request, jsonify
import os
import dagshub
import mlflow
import psycopg2

# Inisialisasi DagsHub
dagshub.init(repo_owner='rahayuya2005', repo_name='attrition', mlflow=True)

os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv('MLFLOW_TRACKING_PASSWORD')

def get_db_connection():

    db_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(db_url)

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
    age = int(data.get('Age', 0))
    income = int(data.get('MonthlyIncome', 0))

    # Dummy logic
    if age < 30 and income < 4000:
        result = "Berpotensi Resign"
    else:
        result = "Cenderung Bertahan"

    return jsonify({'result': result})

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions 
        (age, monthly_income, overtime, job_level, total_working_years, result)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        int(data.get('Age', 0)), 
        int(data.get('MonthlyIncome', 0)), 
        data.get('OverTime'), 
        int(data.get('JobLevel', 0)), 
        int(data.get('TotalWorkingYears', 0)), 
        data.get('result')
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Data berhasil disimpan ke database!'})

if __name__ == '__main__':
    # Railway butuh host 0.0.0.0 dan port dinamis
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)