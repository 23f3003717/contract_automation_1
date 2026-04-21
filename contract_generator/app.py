from flask import Flask, render_template, request, send_file, jsonify
import asyncio
from playwright.async_api import async_playwright
import io
import os
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

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = get_form_data(request.form)
        html_content = render_template('contract.html', **data)

        pdf_bytes = asyncio.run(html_to_pdf(html_content))

        filename = f"POP_Contract_{data['provider_name'].replace(' ', '_')}.pdf"

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        app.logger.error(f"PDF generation error: {str(e)}")
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

async def html_to_pdf(html_content):
    """Convert HTML string to PDF bytes using Playwright"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html_content, wait_until='networkidle')
            pdf_bytes = await page.pdf()
            await browser.close()
            return pdf_bytes
    except Exception as e:
        app.logger.error(f"Playwright error: {str(e)}")
        raise

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
