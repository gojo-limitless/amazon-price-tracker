from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import os
from models import db, PriceHistory

app = Flask(__name__)
# Use PostgreSQL URL from environment variable in production, fallback to SQLite for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///price_history.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

def clean_price_text(price_text):
    # Remove currency symbols and clean up the price
    price_text = re.sub(r'[^\d.,]', '', price_text)
    # Handle different decimal separators
    if ',' in price_text and '.' in price_text:
        price_text = price_text.replace(',', '')
    elif ',' in price_text:
        price_text = price_text.replace(',', '.')
    return price_text

def extract_price(soup):
    # List of possible price element selectors with their attributes
    price_selectors = [
        {'element': 'span', 'class': 'a-price-whole'},
        {'element': 'span', 'class': 'a-offscreen'},
        {'element': 'span', 'id': 'priceblock_ourprice'},
        {'element': 'span', 'id': 'priceblock_dealprice'},
        {'element': 'span', 'class': 'a-price'},
        {'element': 'span', 'class': 'a-color-price'},
        {'element': 'span', 'class': 'a-price-symbol'},
        {'element': 'span', 'class': 'a-text-price'}
    ]
    
    # Try each selector
    for selector in price_selectors:
        element_type = selector.pop('element', 'span')
        elements = soup.find_all(element_type, selector)
        
        for element in elements:
            try:
                # Get the text content
                price_text = element.text.strip()
                
                # If it's a price symbol element, try to get the next sibling
                if 'symbol' in str(element.get('class', [])):
                    next_element = element.find_next_sibling('span', class_='a-price-whole')
                    if next_element:
                        price_text = next_element.text.strip()
                
                # Clean and convert the price
                price_text = clean_price_text(price_text)
                if price_text:
                    try:
                        price = float(price_text)
                        if price > 0:  # Validate the price is positive
                            return price
                    except ValueError:
                        continue
            except Exception:
                continue
    
    # If no price found with selectors, try to find any text that looks like a price
    price_pattern = r'[\$£€]?\s*\d+([.,]\d{2})?'
    potential_prices = re.findall(price_pattern, str(soup))
    
    for price_match in potential_prices:
        try:
            price_text = clean_price_text(price_match)
            price = float(price_text)
            if price > 0:
                return price
        except ValueError:
            continue
    
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    url = request.form.get('url')
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get price using the improved function
        price = extract_price(soup)
        
        # Try to find the title with multiple selectors
        title_element = (
            soup.find('span', {'id': 'productTitle'}) or
            soup.find('h1', {'id': 'title'}) or
            soup.find('h1', class_='product-title')
        )
        title = title_element.text.strip() if title_element else 'Title not found'

        if price is not None:
            # Store the price in database
            price_record = PriceHistory(
                product_url=url,
                product_title=title,
                price=price
            )
            db.session.add(price_record)
            db.session.commit()

            # Get price history
            history = PriceHistory.get_history(url)
            price_history = [
                {
                    'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'price': "{:.2f}".format(entry.price)
                }
                for entry in history
            ]

            return jsonify({
                'success': True,
                'price': "{:.2f}".format(price),
                'title': title,
                'history': price_history
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Price not found'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 