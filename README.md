# 🔊 Horeg FC

## 🛠️ Setup Git dan GitHub
1. Buka Terminal VSCode dan ketik `git clone <link>`
2. Buat branch utama baru bernama main dengan `git branch -M main`
3. Tambahkan folder .gitignore
4. Melakukan testing dengan 
    ```bash
    git add .
    git commit -m "tes komen"
    git push -u origin main

## 🐍 Setup Virtual Environment dan Django
1. Buka virtual environment dengan `python -m venv env`
2. Ketik `env\Scripts\activate`
3. Buat berkas bernama `requirements.txt` dan tambahkan beberapa dependencies
4. Install dengan `pip install -r requirements.txt`
5. Buat proyek Django `django-admin startproject horeg_fc .`
6. Buat file `.env` dan `.env.prod`
7. Modifikasi `settings.py`
8. Lakukan migrate dengan `python manage.py migrate`
9. Jalankan server Django dengan `python manage.py runserver`

## 🔧 Setting PWS
1. Buat project baru pada PWS
2. Ubah raw environmentnya menjadi sesuai dengan `.env.prod`
3. Tambahkan `ALLOWED_HOST` di `settings.py`
4. Jalankan informasi Project Command di PWS

## 📱 Setup Aplikasi `main`
1. Buat aplikasi baru bernama main dengan `python manage.py startapp main`
2. Masukkan `main` ke dalam proyek
3. Buat folder templates dan buat file bernama `main.html` di dalamnya
4. Ubah isi dari `models.py`
5. Lakukan migrasi dengan `python manage.py makemigrations` dan `python manage.py migrate`
6. Masukkan data di `views.py`
7. Modifikasi template

## 🌐 URL Routing
1. Buat berkas `urls.py` di dalam `main`
2. Import `include` di `angkringan_cyberpunk/urls.py` dan tambahkan
    ```bash
    path('', include('main.urls'))

## Project siap dijalankan!
Jalankan proyek dengan `python manage.py runserver`

## Routing bekerja dengan cara
![Alur kerja Django](request_response.jpg)
`urls.py` mencocokan URL yang diakses browser dengan daftar path yang didefinisikan di file `urls.py`. Apabila cocok, request akan diarahkan ke view yang sesuai.

Setelah menerima request dari `urls.py`, `views.py` akan mengambil atau memodifikasi data di `models.py` jika perlu. Lalu mengirim data ke `Template` untuk dirender menjadi `HTML`. Hasil render tersebut yang menjadi `HTTP Response` dan dikirim kembali ke user.

`models.py` berfungsi sebagai tempat untuk mendefinisikan tabel `database` dalam bentuk class Python. Django bisa mengambil, mengubah, atau bahkkan menyimpan data di `database` tanpa pakai query SQL secara langsung. Models biasanya dipakai oleh `views.py` untuk mengambil atau menyimpan data, tetapi tidak berhubungan langsung dengan template ataupun URL.

Berkas `HTML` atau template `HTML` adalah berkas berisi tampilan halaman web. Namun, template tidak bisa mengambil datanya sendiri, semua data dikirim dari `views.py`, lalu views membuat `HTTP Response` dan dikirim ke browser

## Peran `settings.py` dalam proyek Django
Secara garis besar settings.py berguna untuk mengatur proyek Django yang digunakan.
Contohnya seperti `ALLOWED_HOST` untuk mengatur host/domain yang boleh mengakses aplikasi.
Lalu ada `Database` yang berfungsi ke dalam dua jalur, yaitu jika `PRODUCTION` bernilai `True`, Django akan menggunakan model `PostgreSQL`. Namun, jika `PODUCTION` bernilai `False`, Django akan menggunakan `SQLite`

## Cara kerja migrasi di database Django
Setiap perubahan di models.py harus dimigrasi. Migrasi bekerja dengan menyamakan bentuk database dengan model yang dibuat di models.py. Saat mengubah models.py, Django akan membuat file migrasi dengan `python manage.py makemigrations`. Setelah itu, jalankan `python manage.py migrate` agar menerapkan perubahan itu langsung ke Database.

## Alasan Django dijadikan permulaan pembelajaran
Django sudah menyediakan banyak fitur bawaan sehingga tidak perlu mengatur semuanya dari awal. Dengan Django, kita bisa langsung belajar konsep inti pengembangan perangkat lunak, seperti MVT. Hal ini membuat Django cocok dijadikan framework awal untuk memahami cara kerja pengembangan aplikasi yang terstruktur.

## Feedback untuk Asdos Tutorial 1
Tidak ada, kebetulan tutorial 1 tidak menemukan kesulitan