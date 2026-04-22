from flask import Flask, render_template, request, send_file, jsonify
import asyncio
from playwright.async_api import async_playwright
import os
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import io
from datetime import datetime

app = Flask(__name__)

def ordinal(n):
    """Convert number to ordinal string: 1 -> 1st, 20 -> 20th"""
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return f"{n}{suffix}"

def format_date(date_str):
    """Format date string to '20th April 2026' style"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day = ordinal(dt.day)
        month = dt.strftime("%B")
        year = dt.year
        return f"{day} {month} {year}"
    except:
        return date_str

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/preview', methods=['POST'])
def preview():
    data = get_form_data(request.form)
    return render_template('contract.html', **data)


@app.route('/download', methods=['POST'])
def download():
    data = get_form_data(request.form)

    html = render_template('contract.html', **data)

    pdf = HTML(string=html).write_pdf()

    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name="contract.pdf"
    )
def get_form_data(form):
    agreement_date = format_date(form.get('agreement_date', '2026-04-20'))
    effective_date = format_date(form.get('effective_date', '2026-03-21'))
    commission = form.get('commission', '20')
    provider_name = form.get('provider_name', 'Service Provider')
    city = form.get('city', 'Greater Noida')
    provider_designation = form.get('provider_designation', '')

    # Commission as words
    commission_words = {
        '5': 'five', '10': 'ten', '15': 'fifteen', '20': 'twenty',
        '25': 'twenty-five', '30': 'thirty', '35': 'thirty-five',
        '40': 'forty', '45': 'forty-five', '50': 'fifty'
    }
    commission_word = commission_words.get(commission, f'{commission}')

    return {
        'agreement_date': agreement_date,
        'effective_date': effective_date,
        'commission': commission,
        'commission_word': commission_word,
        'provider_name': provider_name,
        'city': city,
        'provider_designation': provider_designation,
    }

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, port=5000)
