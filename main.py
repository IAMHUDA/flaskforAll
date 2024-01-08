# digunakan untuk import modul 
from flask import Flask, render_template, request,redirect,url_for
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/enternew')
def data_siswa():
    return render_template('siswa.html') 

@app.route('/addrec', methods=['POST', 'GET'])  
def addrec(): 
    if request.method == 'POST': 
        try:
            nama = request.form['nama']
            kd_MK = request.form['kd_MK']
            kelas = request.form['kelas']
            nilai = request.form['nilai']

            with sql.connect("Mahasiswa.db") as con: 
                cur = con.cursor()

                
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS InputNilai (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT,
                        kd_MK TEXT,
                        kelas TEXT,
                        nilai TEXT
                    )
                ''')

                cur.execute('''
                    INSERT INTO InputNilai (nama, kd_MK, kelas, nilai)
                    VALUES (?, ?, ?, ?)''', (nama, kd_MK, kelas, nilai)) 

                con.commit()
                msg = "Data berhasil disimpan" 
        except sql.Error as e:
            con.rollback() 
            msg = f"Data tidak berhasil disimpan: {e}" 
        finally:
            con.close()  
            return redirect(url_for('list')) 

@app.route('/list') 
def list(): 
    con = sql.connect("Mahasiswa.db") 
    con.row_factory = sql.Row 

    cur = con.cursor() 
    cur.execute("SELECT * FROM InputNilai") 
    rows = cur.fetchall() 
    con.close() 

    return render_template("list.html", rows=rows)

if __name__ == '__main__': 
    app.run(debug=True)
