from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Mengarah ke home.html (pastikan file ini juga sudah dibuat)
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    # Ini akan memanggil file dashboard yang Anda buat tadi
    return render_template('dashboard.html')

@app.route('/form_prediction') # Link yang diketik di browser/tombol
def predict_page():
    return render_template('form_prediction.html') # Nama file asli di folder templates

@app.route('/predict', methods=['POST'])
def predict():
    # ambil data dari form (contoh)
    data = request.form.to_dict()

    print(data)  # debug lihat input

    # sementara tampilkan hasil dummy
    return "Prediksi berhasil diproses!"

if __name__ == '__main__':
    # Aktifkan debug=True agar perubahan langsung terlihat tanpa restart manual
    app.run(debug=True, port=5002) # 8000