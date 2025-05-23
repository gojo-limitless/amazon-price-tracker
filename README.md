# Amazon Price Tracker

A web application that tracks Amazon product prices over time, featuring a beautiful UI with real-time price tracking and historical price charts.

## Features

- 🎯 Real-time price tracking from Amazon product pages
- 📊 Interactive price history charts
- 💫 Modern, responsive design with gradient backgrounds
- 🔄 Animated hexagonal logo
- 🌟 Glassmorphism design elements
- 📱 Mobile-friendly interface

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: 
  - HTML5/CSS3
  - Tailwind CSS
  - Chart.js for data visualization
- **Deployment**: Ready for Render.com deployment

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd amazon-price-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Production Deployment

The application is configured for deployment on Render.com with the following features:
- Automatic PostgreSQL database setup
- HTTPS enabled
- Production-grade Gunicorn server

## Usage

1. Navigate to the application's homepage
2. Copy an Amazon product URL
3. Paste it into the search bar
4. Click "Track Price"
5. View current price and historical price chart

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 