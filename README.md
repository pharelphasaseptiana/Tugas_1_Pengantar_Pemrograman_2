# CalcSpace — Minimal Workspace Calculator

CalcSpace adalah aplikasi web kalkulator berbasis **Python Flask** dengan tampilan minimal, modern, dan responsif. Aplikasi ini dibuat untuk memenuhi tugas Pengantar Pemrograman dengan kategori utama **Operasi Aritmatika**, **Operator Logika**, dan **Transformasi Bilangan**.

## Teknologi yang Digunakan
- Python
- Flask
- HTML
- CSS custom
- JavaScript
- Jinja2 Template
- Bootstrap 5 CDN
- Session Flask untuk penyimpanan riwayat sementara

## Fitur Utama

### 1. Operasi Aritmatika

Mendukung operasi:

- Tambah
- Kurang
- Kali
- Bagi
- Pangkat
- Akar kuadrat
- Modulus
- Floor division

Validasi yang tersedia:

- Input wajib diisi.
- Input harus berupa angka.
- Pembagian, modulus, dan floor division dengan nol ditolak.
- Akar bilangan negatif ditolak.
- Operasi akar hanya membutuhkan satu input.

### 2. Operator Logika

Mendukung operator:

- AND
- OR
- NOT
- XOR
- NAND
- NOR
  Validasi yang tersedia:
- Nilai logika hanya boleh True atau False.
- Operator NOT hanya membutuhkan input P.
- Operator dua operand membutuhkan P dan Q.
- Hasil menampilkan rumus, langkah-langkah, dan diagram gerbang logika monochrome.

### 3. Transformasi Bilangan

Mendukung konversi antar basis:

- Binary
- Decimal
- Octal
- Hexadecimal
  Validasi yang tersedia:
- Input bilangan wajib diisi.
- Basis asal dan basis tujuan wajib dipilih.
- Bilangan yang tidak sesuai dengan basis asal akan ditolak dengan pesan error yang mudah dipahami.
  Contoh: `102` pada basis Binary akan ditolak karena digit `2` tidak valid pada bilangan biner.

### 4. Konversi Suhu

Mendukung konversi antar satuan:

- Celcius
- Fahrenheit
- Kelvin
- Reamur
  Setiap hasil menampilkan proses konversi melalui Celcius sebagai satuan perantara.

### 5. Konversi Mata Uang

Mendukung konversi mata uang berbasis kurs statis di `app.py`:

- IDR
- USD
- EUR
- SGD
- JPY
- MYR

Validasi yang tersedia:

- Jumlah wajib diisi.
- Jumlah harus berupa angka.
- Jumlah negatif ditolak.
- Mata uang asal dan tujuan wajib dipilih.
  Catatan: kurs mata uang bersifat **statis**, bukan real-time.

### 6. Fitur Bonus

- Faktorial
- Fibonacci
  Validasi tambahan:
- Faktorial hanya menerima bilangan bulat non-negatif.
- Fibonacci hanya menerima jumlah suku lebih dari 0.
- Batas input diterapkan agar aplikasi tetap aman dan responsif.

## Fitur UI/UX

- Tampilan minimal hitam-putih/grayscale.
- Dark mode dan light mode.
- Responsive untuk desktop, tablet, dan mobile.
- Navigasi kategori di bar atas pada halaman kalkulator.
- Menu cepat melalui tombol garis tiga.
- History semua kategori dan history per kategori.
- Detail history dapat dibuka untuk melihat hasil, rumus, dan langkah perhitungan.
- Input default kosong agar pengguna memilih dan mengisi data sendiri.

## Struktur Folder

```text
calcspace_project/
├── app.py
├── requirements.txt
├── Procfile
├── vercel.json
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   ├── arithmetic_generated.png
│   │   ├── base_generated.png
│   │   ├── currency_generated.png
│   │   ├── fibonacci_generated.png
│   │   └── temperature_generated.png
│   └── js/
│       └── app.js
└── templates/
    ├── base.html
    ├── calculator.html
    ├── history.html
    ├── history_panel.html
    ├── icons.html
    └── index.html
```
