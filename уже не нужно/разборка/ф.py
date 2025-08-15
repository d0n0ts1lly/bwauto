import requests
from bs4 import BeautifulSoup
import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:23032023@localhost/copart_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель Part
class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    part_code = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(500))

    subcategory = db.relationship('Subcategory', backref='parts')

# Для примера нужна модель Subcategory (чтобы SQLAlchemy знал о таблице)
class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


def parse_and_save_parts(url, subcategory_id):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.find("div", class_="detail-cat_list mb")
    if not container:
        print("Блок с запчастями не найден")
        return

    parts_added = 0
    for link in container.find_all("a", href=True):
        text = link.get_text(strip=True)
        clean_text = re.sub(r"\s*\(\d+\)\s*$", "", text)

        # Создаём объект Part
        part = Part(
            subcategory_id=subcategory_id,
            name=clean_text
        )
        db.session.add(part)
        parts_added += 1

    db.session.commit()
    print(f"Добавлено запчастей: {parts_added}")

def parse_and_save_multiple(urls_and_ids):
    for url, subcategory_id in urls_and_ids:
        print(f"Обрабатываем подкатегорию {subcategory_id} с URL: {url}")
        parse_and_save_parts(url, subcategory_id)


if __name__ == '__main__':
    with app.app_context():
        urls_and_subcategories = [
            
        ]

        parse_and_save_multiple(urls_and_subcategories)
