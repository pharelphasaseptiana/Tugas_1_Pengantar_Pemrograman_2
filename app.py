from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "calcspace-pixel-match-v30-final-validation"

DEFAULT_HISTORY: List[Dict[str, str]] = []


CATEGORIES: Dict[str, Dict[str, str]] = {
    "arithmetic": {
        "slug": "arithmetic",
        "title": "Aritmatika",
        "subtitle": "Operasi dasar matematika seperti tambah, kurang, kali, dan bagi.",
        "icon": "arithmetic",
    },
    "logic": {
        "slug": "logic",
        "title": "Logika",
        "subtitle": "Operasi logika seperti AND, OR, NOT, NAND, NOR, XOR, dan XNOR.",
        "icon": "logic",
    },
    "base": {
        "slug": "base",
        "title": "Basis Bilangan",
        "subtitle": "Konversi antar basis bilangan biner, desimal, heksadesimal, dan oktal.",
        "icon": "base",
    },
    "temperature": {
        "slug": "temperature",
        "title": "Suhu",
        "subtitle": "Konversi satuan suhu seperti Celsius, Fahrenheit, Kelvin, dan Reamur.",
        "icon": "temperature",
    },
    "currency": {
        "slug": "currency",
        "title": "Mata Uang",
        "subtitle": "Konversi antar mata uang berdasarkan kurs terbaru.",
        "icon": "currency",
    },
    "factorial": {
        "slug": "factorial",
        "title": "Faktorial",
        "subtitle": "Hitung faktorial dari suatu bilangan (n!).",
        "icon": "factorial",
    },
    "fibonacci": {
        "slug": "fibonacci",
        "title": "Fibonacci",
        "subtitle": "Generate dan lihat deret Fibonacci hingga n suku.",
        "icon": "fibonacci",
    },
}

LOGIC_OPERATORS = ["AND", "OR", "NOT", "XOR", "NAND", "NOR"]
BASES = {"Binary": 2, "Decimal": 10, "Octal": 8, "Hexadecimal": 16}
TEMP_UNITS = {"Celcius": "C", "Fahrenheit": "F", "Kelvin": "K", "Reamur": "R"}
CURRENCY_RATES_IDR = {
    "IDR": 1.0,
    "USD": 16000.0,
    "EUR": 17500.0,
    "SGD": 11900.0,
    "JPY": 110.0,
    "MYR": 3400.0,
}


def get_history() -> List[Dict[str, str]]:
    """Ambil riwayat dari session. Awal aplikasi selalu kosong."""
    return list(session.get("history", DEFAULT_HISTORY.copy()))


def filter_history(category: str | None = None) -> List[Dict[str, str]]:
    history = get_history()
    if not category or category == "all":
        return history
    return [item for item in history if item.get("slug") == category]


def save_history(item: Dict[str, str]) -> None:
    history = get_history()
    history.insert(0, item)
    session["history"] = history[:12]


def add_history(
    title: str,
    detail: str,
    icon: str,
    slug: str,
    result: str = "",
    formula: str = "",
    steps: List[str] | None = None,
) -> None:
    save_history(
        {
            "title": title,
            "detail": detail,
            "time": datetime.now().strftime("%H:%M"),
            "icon": icon,
            "slug": slug,
            "result": result,
            "formula": formula,
            "steps": steps or [],
        }
    )


def require_text(data: Dict[str, Any], key: str, label: str) -> str:
    value = str(data.get(key, "")).strip()
    if value == "":
        raise ValueError(f"{label} belum diisi.")
    return value


def require_float(data: Dict[str, Any], key: str, label: str) -> float:
    value = require_text(data, key, label)
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{label} harus berupa angka.") from exc


def require_int(data: Dict[str, Any], key: str, label: str) -> int:
    value = require_text(data, key, label)
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{label} harus berupa bilangan bulat.") from exc


def format_number(value: float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:,.6f}".rstrip("0").rstrip(".")


def convert_base(value: int, base: int) -> str:
    if base == 2:
        return bin(value)[2:]
    if base == 8:
        return oct(value)[2:]
    if base == 10:
        return str(value)
    if base == 16:
        return hex(value)[2:].upper()
    raise ValueError("Basis tujuan tidak valid.")


def arithmetic_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    operation = require_text(data, "operation", "Operasi")
    a = require_float(data, "a", "Bilangan A")
    b = 0.0 if operation == "akar" else require_float(data, "b", "Bilangan B")

    if operation == "+":
        result = a + b
        formula = "a + b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Hitung {format_number(a)} + {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} + {format_number(b)}"
    elif operation == "-":
        result = a - b
        formula = "a - b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Hitung {format_number(a)} - {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} - {format_number(b)}"
    elif operation == "×":
        result = a * b
        formula = "a × b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Hitung {format_number(a)} × {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} × {format_number(b)}"
    elif operation == "÷":
        if b == 0:
            raise ValueError("Pembagian dengan nol tidak diperbolehkan.")
        result = a / b
        formula = "a ÷ b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Hitung {format_number(a)} ÷ {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} ÷ {format_number(b)}"
    elif operation == "pangkat":
        result = a**b
        formula = "a^b"
        steps = [f"Masukkan basis a = {format_number(a)} dan pangkat b = {format_number(b)}.", f"Hitung {format_number(a)}^{format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)}^{format_number(b)}"
    elif operation == "akar":
        if a < 0:
            raise ValueError("Akar bilangan negatif tidak didukung pada kalkulator real.")
        result = math.sqrt(a)
        formula = "√a"
        steps = [f"Masukkan a = {format_number(a)}.", f"Hitung akar kuadrat dari {format_number(a)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"√{format_number(a)}"
    elif operation == "modulus":
        if b == 0:
            raise ValueError("Modulus dengan nol tidak diperbolehkan.")
        result = a % b
        formula = "a mod b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Cari sisa pembagian {format_number(a)} oleh {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} mod {format_number(b)}"
    elif operation == "floor division":
        if b == 0:
            raise ValueError("Floor division dengan nol tidak diperbolehkan.")
        result = a // b
        formula = "a // b"
        steps = [f"Masukkan a = {format_number(a)} dan b = {format_number(b)}.", f"Hitung pembagian bulat ke bawah {format_number(a)} // {format_number(b)}.", f"Hasilnya adalah {format_number(result)}."]
        detail = f"{format_number(a)} // {format_number(b)}"
    else:
        raise ValueError("Operasi aritmatika tidak dikenali.")

    add_history("Aritmatika", detail, "arithmetic", "arithmetic", format_number(result), formula, steps)
    return {"result": format_number(result), "formula": formula, "steps": steps, "title": "Aritmatika"}


def logic_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    op = require_text(data, "operation", "Operator")
    p_text = require_text(data, "p", "Nilai P")
    if p_text.lower() not in {"true", "false"}:
        raise ValueError("Nilai P harus True atau False.")
    p = p_text.lower() == "true"

    q = False
    if op != "NOT":
        q_text = require_text(data, "q", "Nilai Q")
        if q_text.lower() not in {"true", "false"}:
            raise ValueError("Nilai Q harus True atau False.")
        q = q_text.lower() == "true"

    if op == "AND":
        result = p and q
        formula = "P AND Q"
        steps = [f"P = {p}, Q = {q}.", "AND bernilai True hanya jika P dan Q sama-sama True.", f"Hasilnya adalah {result}."]
        detail = f"{p} AND {q}"
    elif op == "OR":
        result = p or q
        formula = "P OR Q"
        steps = [f"P = {p}, Q = {q}.", "OR bernilai True jika minimal salah satu operand bernilai True.", f"Hasilnya adalah {result}."]
        detail = f"{p} OR {q}"
    elif op == "NOT":
        result = not p
        formula = "NOT P"
        steps = [f"P = {p}.", "NOT membalik nilai logika P.", f"Hasilnya adalah {result}."]
        detail = f"NOT {p}"
    elif op == "XOR":
        result = p != q
        formula = "P XOR Q"
        steps = [f"P = {p}, Q = {q}.", "XOR bernilai True jika P dan Q berbeda.", f"Hasilnya adalah {result}."]
        detail = f"{p} XOR {q}"
    elif op == "NAND":
        result = not (p and q)
        formula = "NOT (P AND Q)"
        steps = [f"P = {p}, Q = {q}.", f"P AND Q = {p and q}.", f"NAND adalah kebalikannya, jadi hasilnya {result}."]
        detail = f"{p} NAND {q}"
    elif op == "NOR":
        result = not (p or q)
        formula = "NOT (P OR Q)"
        steps = [f"P = {p}, Q = {q}.", f"P OR Q = {p or q}.", f"NOR adalah kebalikannya, jadi hasilnya {result}."]
        detail = f"{p} NOR {q}"
    else:
        raise ValueError("Operator logika tidak dikenali.")

    add_history("Logika", detail, "logic", "logic", str(result), formula, steps)
    return {"result": str(result), "formula": formula, "steps": steps, "title": "Logika"}



def base_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    raw = require_text(data, "number", "Bilangan").upper()
    from_name = require_text(data, "from_base", "Basis asal")
    to_name = require_text(data, "to_base", "Basis tujuan")
    from_base = BASES.get(from_name)
    to_base = BASES.get(to_name)
    if not from_base or not to_base:
        raise ValueError("Basis asal atau tujuan tidak valid.")
    try:
        decimal_value = int(raw, from_base)
    except ValueError as exc:
        raise ValueError(
            f"Bilangan '{raw}' tidak valid untuk basis {from_name}. "
            "Periksa kembali digit yang digunakan."
        ) from exc
    result = convert_base(decimal_value, to_base)
    formula = f"{from_name} → {to_name}"
    steps = [
        f"Baca bilangan {raw} sebagai basis {from_base}.",
        f"Ubah terlebih dahulu ke desimal: {decimal_value}.",
        f"Konversi {decimal_value} ke basis {to_base}, hasilnya {result}.",
    ]
    add_history("Basis Bilangan", f"{raw}₍{from_base}₎ → {result}₍{to_base}₎", "base", "base", result, formula, steps)
    return {"result": result, "formula": formula, "steps": steps, "title": "Basis Bilangan"}


def to_celsius(value: float, unit: str) -> float:
    if unit == "Celcius":
        return value
    if unit == "Fahrenheit":
        return (value - 32) * 5 / 9
    if unit == "Kelvin":
        return value - 273.15
    if unit == "Reamur":
        return value * 5 / 4
    raise ValueError("Satuan suhu tidak valid.")


def from_celsius(value: float, unit: str) -> float:
    if unit == "Celcius":
        return value
    if unit == "Fahrenheit":
        return value * 9 / 5 + 32
    if unit == "Kelvin":
        return value + 273.15
    if unit == "Reamur":
        return value * 4 / 5
    raise ValueError("Satuan suhu tidak valid.")


def temperature_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    value = require_float(data, "value", "Nilai Suhu")
    from_unit = require_text(data, "from_unit", "Satuan asal")
    to_unit = require_text(data, "to_unit", "Satuan tujuan")
    celsius = to_celsius(value, from_unit)
    result = from_celsius(celsius, to_unit)
    formula = f"{from_unit} → Celcius → {to_unit}"
    steps = [
        f"Masukkan suhu {format_number(value)} °{TEMP_UNITS[from_unit]}.",
        f"Ubah ke Celcius: {format_number(celsius)} °C.",
        f"Ubah Celcius ke {to_unit}: {format_number(result)} °{TEMP_UNITS[to_unit]}.",
    ]
    add_history("Suhu", f"{format_number(value)} °{TEMP_UNITS[from_unit]} → {format_number(result)} °{TEMP_UNITS[to_unit]}", "temperature", "temperature", f"{format_number(result)} °{TEMP_UNITS[to_unit]}", formula, steps)
    return {"result": f"{format_number(result)} °{TEMP_UNITS[to_unit]}", "formula": formula, "steps": steps, "title": "Suhu"}


def currency_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    amount = require_float(data, "amount", "Jumlah")
    if amount < 0:
        raise ValueError("Jumlah mata uang tidak boleh negatif.")
    from_cur = require_text(data, "from_currency", "Mata uang asal")
    to_cur = require_text(data, "to_currency", "Mata uang tujuan")
    if from_cur not in CURRENCY_RATES_IDR or to_cur not in CURRENCY_RATES_IDR:
        raise ValueError("Mata uang tidak valid.")
    amount_idr = amount * CURRENCY_RATES_IDR[from_cur]
    result = amount_idr / CURRENCY_RATES_IDR[to_cur]
    formula = f"{from_cur} → IDR → {to_cur}"
    steps = [
        f"Gunakan kurs statis: 1 {from_cur} = {format_number(CURRENCY_RATES_IDR[from_cur])} IDR.",
        f"Ubah ke IDR: {format_number(amount)} × {format_number(CURRENCY_RATES_IDR[from_cur])} = {format_number(amount_idr)} IDR.",
        f"Ubah IDR ke {to_cur}: {format_number(amount_idr)} ÷ {format_number(CURRENCY_RATES_IDR[to_cur])} = {format_number(result)} {to_cur}.",
    ]
    add_history("Mata Uang", f"{from_cur} → {to_cur}", "currency", "currency", f"{format_number(result)} {to_cur}", formula, steps)
    return {"result": f"{format_number(result)} {to_cur}", "formula": formula, "steps": steps, "title": "Mata Uang"}


def factorial_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    n = require_int(data, "n", "Nilai n")
    if n < 0:
        raise ValueError("Faktorial hanya berlaku untuk bilangan bulat non-negatif.")
    if n > 500:
        raise ValueError("Nilai n maksimal 500 agar hasil tetap aman diproses.")
    result = math.factorial(n)
    formula = "n! = n × (n-1) × ... × 1"
    preview = " × ".join(str(i) for i in range(n, max(n - 8, 0), -1))
    if n > 8:
        preview += " × ... × 1"
    elif n == 0:
        preview = "1"
    steps = [
        f"Masukkan n = {n}.",
        f"Gunakan rumus faktorial: {n}! = {preview}.",
        f"Hasilnya adalah {result}.",
    ]
    add_history("Faktorial", f"{n}!", "factorial", "factorial", str(result), formula, steps)
    return {"result": str(result), "formula": formula, "steps": steps, "title": "Faktorial"}


def fibonacci_calc(data: Dict[str, Any]) -> Dict[str, Any]:
    n = require_int(data, "n", "Jumlah Suku")
    if n <= 0:
        raise ValueError("Jumlah suku Fibonacci harus lebih dari 0.")
    if n > 100:
        raise ValueError("Jumlah suku maksimal 100 agar tampilan tetap rapi.")
    series: List[int] = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    formula = "F(n) = F(n-1) + F(n-2)"
    steps = [
        "Mulai dari F(0) = 0 dan F(1) = 1.",
        "Setiap suku berikutnya adalah penjumlahan dua suku sebelumnya.",
        f"{n} suku pertama adalah: {', '.join(map(str, series))}.",
    ]
    add_history("Fibonacci", f"{n} suku", "fibonacci", "fibonacci", ", ".join(map(str, series)), formula, steps)
    return {"result": ", ".join(map(str, series)), "formula": formula, "steps": steps, "title": "Fibonacci"}


CALCULATORS = {
    "arithmetic": arithmetic_calc,
    "logic": logic_calc,
    "base": base_calc,
    "temperature": temperature_calc,
    "currency": currency_calc,
    "factorial": factorial_calc,
    "fibonacci": fibonacci_calc,
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        categories=list(CATEGORIES.values()),
        history=filter_history("all"),
        current_category=None,
        history_scope="all",
        history_panel_visible=False,
        history_page_url="/history",
        body_class="home-view",
    )


@app.route("/calculator/<category>")
def calculator(category: str):
    if category not in CATEGORIES:
        category = "arithmetic"
    return render_template(
        "calculator.html",
        category=CATEGORIES[category],
        categories=list(CATEGORIES.values()),
        history=filter_history(category),
        current_category=category,
        history_scope=category,
        history_panel_visible=True,
        history_page_url=f"/history/{category}",
        body_class="calculator-view",
        logic_operators=LOGIC_OPERATORS,
        bases=list(BASES.keys()),
        temp_units=list(TEMP_UNITS.keys()),
        currencies=list(CURRENCY_RATES_IDR.keys()),
    )


@app.route("/history")
def history_page():
    return render_template(
        "history.html",
        title="Semua Riwayat",
        subtitle="Menampilkan seluruh riwayat perhitungan dari semua kategori.",
        history=filter_history("all"),
        categories=list(CATEGORIES.values()),
        current_category=None,
        history_scope="all",
        history_panel_visible=False,
        history_page_url="/history",
        body_class="history-view",
        back_url=url_for("index"),
        back_label="← Kembali ke Beranda",
    )


@app.route("/history/<category>")
def history_category(category: str):
    if category not in CATEGORIES:
        category = "arithmetic"
    title = f"Riwayat {CATEGORIES[category]['title']}"
    opened_from_all = request.args.get("from") == "all"
    return render_template(
        "history.html",
        title=title,
        subtitle=f"Menampilkan riwayat khusus kategori {CATEGORIES[category]['title']}.",
        history=filter_history(category),
        categories=list(CATEGORIES.values()),
        current_category=category,
        history_scope=category,
        history_panel_visible=False,
        history_page_url=f"/history/{category}",
        body_class="history-view",
        back_url=url_for("history_page") if opened_from_all else url_for("index"),
        back_label="← Kembali ke Semua Riwayat" if opened_from_all else "← Kembali ke Beranda",
    )


@app.post("/api/calculate/<category>")
def calculate(category: str):
    try:
        if category not in CALCULATORS:
            raise ValueError("Kategori kalkulator tidak ditemukan.")
        payload = request.get_json(force=True, silent=True) or {}
        response = CALCULATORS[category](payload)
        response["history"] = filter_history(category)
        return jsonify({"ok": True, **response})
    except Exception as exc:  # noqa: BLE001 - tampilkan pesan validasi ke pengguna
        return jsonify({"ok": False, "error": str(exc), "history": filter_history(category)}), 400


@app.get("/api/history")
def history_api():
    category = request.args.get("category", "all")
    return jsonify(filter_history(category))


@app.post("/api/history/clear")
def clear_history():
    payload = request.get_json(force=True, silent=True) or {}
    category = payload.get("category") or request.args.get("category", "all")
    if category and category != "all":
        session["history"] = [item for item in get_history() if item.get("slug") != category]
        return jsonify({"ok": True, "history": filter_history(category)})
    session["history"] = []
    return jsonify({"ok": True, "history": []})


if __name__ == "__main__":
    app.run(debug=True)
