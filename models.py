from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_url = db.Column(db.String(500), index=True)
    product_title = db.Column(db.String(500))
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_history(product_url):
        return PriceHistory.query.filter_by(product_url=product_url).order_by(PriceHistory.timestamp.asc()).all() 