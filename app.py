import requests
from flask import Flask, render_template, url_for, request, session, jsonify, redirect, flash
import os
#from scraper import get_car_data
from urllib.parse import urlencode
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import func, case
import random
from math import ceil
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import current_user, login_required, LoginManager, login_user, logout_user, current_user, UserMixin
from flask import abort
from math import ceil
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://d0n0ts1lly:diwtas-hEnwyf-8rafha@"
    "d0n0ts1lly.mysql.pythonanywhere-services.com/"
    "d0n0ts1lly$bwauto"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
API_TOKEN = 'D2_FNI5LjIsTXxUhTq1VgpMKURTd99rF'
API_URL = 'https://api.tehnomir.com.ua/'

TELEGRAM_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_url = db.Column(db.String(255))
    lot_number = db.Column(db.String(50))
    retail_value = db.Column(db.String(50))
    sale_date = db.Column(db.String(100))
    year = db.Column(db.Integer)
    make = db.Column(db.String(50))
    model = db.Column(db.String(100))
    engine = db.Column(db.String(100))
    cylinders = db.Column(db.String(10))
    vin = db.Column(db.String(50))
    title = db.Column(db.String(100))
    odometer = db.Column(db.String(50))
    odometer_desc = db.Column(db.String(50))
    damage = db.Column(db.String(100))
    current_bid = db.Column(db.String(50))
    my_bid = db.Column(db.String(50))
    item_number = db.Column(db.String(50))
    sale_name = db.Column(db.String(100))
    auto_grade = db.Column(db.String(50))
    sale_light = db.Column(db.String(50))
    announcements = db.Column(db.String(255))
    sort_order = db.Column(db.Integer)  # фиксированный порядок

    likes = db.relationship('Like', back_populates='car', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    liked_cars = db.relationship('Like', back_populates='user', lazy=True)

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='liked_cars')
    car = db.relationship('Car', back_populates='likes')

    __table_args__ = (db.UniqueConstraint('user_id', 'car_id', name='unique_like'),)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    part_code = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10))
    quantity = db.Column(db.Integer, default=1)
    delivery_type = db.Column(db.String(20))
    delivery_time = db.Column(db.String(50))
    is_return = db.Column(db.Boolean)
    price_logo = db.Column(db.String(20))
    price_quality = db.Column(db.Integer)
    is_price_final = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewCartItem(db.Model):
    __tablename__ = 'new_cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100), default='Volkswagen')
    price = db.Column(db.Numeric(10, 2), nullable=False)
    part_code = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # якщо є users
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    np_office = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    part_code = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10))
    quantity = db.Column(db.Integer, default=1)
    delivery_type = db.Column(db.String(20))
    delivery_time = db.Column(db.String(50))
    is_return = db.Column(db.Boolean)
    price_logo = db.Column(db.String(20))
    price_quality = db.Column(db.Integer)
    is_price_final = db.Column(db.Boolean, default=False)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    subcategories = db.relationship('Subcategory', backref='category', cascade='all, delete')

class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    part_code = db.Column(db.String(100))  # код детали
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(500))

    subcategory = db.relationship('Subcategory', backref='parts')

class NewOrder(db.Model):
    __tablename__ = 'new_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    np_office = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('NewOrderItem', backref='order', cascade="all, delete-orphan")


class NewOrderItem(db.Model):
    __tablename__ = 'new_order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('new_orders.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    part_code = db.Column(db.String(100))

def parse_price(price_str):
    if not price_str:
        return 0
    # Удаляем всё, кроме цифр и точки
    clean_str = re.sub(r"[^\d.]", "", price_str)
    try:
        return float(clean_str)
    except ValueError:
        return 0


def tehnomir_query(method, data):
    data['apiToken'] = API_TOKEN
    response = requests.post(
        API_URL + method,
        json=data,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
    )
    return response.json()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            login_user(user)
            flash('Успешный вход', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Проверка на пустые поля
        if not username or not password:
            flash('Заповніть усі поля', 'danger')
            return redirect(url_for('register'))

        # Проверка, что пользователь с таким логином уже есть
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Цей логін вже зайнятий', 'danger')
            return redirect(url_for('register'))

        # Хэшируем пароль
        password_hash = generate_password_hash(password)

        # Создаём пользователя с ролью "user"
        new_user = User(username=username, password_hash=password_hash, role='user')
        db.session.add(new_user)
        db.session.commit()

        # Авторизуем сразу после регистрации
        login_user(new_user)
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['role'] = new_user.role

        flash('Реєстрація успішна! Ви увійшли в систему.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/cabinet')
def cabinet():
    if 'user_id' not in session:
        flash("Будь ласка, увійдіть", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']
    username = session['username']
    tab = request.args.get('tab', 'profile')

    context = {
        'username': username,
        'role': role,
        'active_tab': tab
    }

    if tab == 'likes':
        liked_cars = Car.query.join(Like).filter(Like.user_id == user_id).all()
        context['liked_cars'] = liked_cars

    elif tab == 'likes_admin' and role == 'admin':
        likes_info = db.session.query(Like, User, Car).join(User).join(Car).all()
        context['likes_info'] = likes_info

    elif tab == 'cart':
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        new_cart_items = NewCartItem.query.filter_by(user_id=user_id).all()
        context['cart_items'] = cart_items
        context['new_cart_items'] = new_cart_items

    elif tab == 'orders_admin' and role == 'admin':
        orders = db.session.query(Order, User, OrderDetail).\
            join(User, Order.user_id == User.id).\
            join(OrderDetail, OrderDetail.order_id == Order.id).\
            order_by(Order.created_at.desc()).all()
        context['orders_info'] = orders

    elif tab == 'orders':
        if role == 'admin':
            orders = Order.query.order_by(Order.created_at.desc()).all()
            new_orders = NewOrder.query.order_by(NewOrder.created_at.desc()).all()
        else:
            orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
            new_orders = NewOrder.query.filter_by(user_id=user_id).order_by(NewOrder.created_at.desc()).all()

        context['orders'] = orders
        context['new_orders'] = new_orders

    return render_template('cabinet.html', **context)

@app.route('/error')
def error():
    return render_template("error.html")


@app.route('/cars')
def cars():
    page = request.args.get('page', 1, type=int)
    per_page = 8

    make_filter = request.args.get('make')
    model_filter = request.args.get('model')
    engine_filter = request.args.get('engine')
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    query = Car.query
    if make_filter:
        query = query.filter(Car.make == make_filter)
    if model_filter:
        # фильтруем все модели, начинающиеся с выбранной
        query = query.filter(Car.model.like(f"{model_filter}%"))
    if engine_filter:
        query = query.filter(Car.engine == engine_filter)
    if year_from:
        query = query.filter(Car.year >= int(year_from))
    if year_to:
        query = query.filter(Car.year <= int(year_to))

    # сортировка
    query = query.order_by(
        case(
            (Car.sale_date == 'Будущий (-ие)', 1),
            else_=0
        ),
        Car.sale_date.desc(),
        Car.sort_order
    )

    cars = query.all()

    # цены
    def parse_price(value):
        if not value or 'CAD' in value:
            return None
        try:
            return int(''.join(filter(str.isdigit, value)))
        except:
            return 0

    filtered = []
    for car in cars:
        price = parse_price(car.current_bid)
        if price is None:
            continue
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        car.numeric_price = price
        filtered.append(car)

    total = len(filtered)
    total_pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    cars_on_page = filtered[start:end]

    start_page = max(page - 5, 1)
    end_page = min(page + 5, total_pages)

    makes = [m[0] for m in db.session.query(Car.make).distinct().all()]

    # получаем "чистые" модели (без комплектации)
    raw_models = db.session.query(Car.model).distinct().all()
    models = sorted(set(m[0].split()[0] for m in raw_models if m[0]))

    # фильтр по двигателям (оставь условие своё)
    raw_engines = db.session.query(Car.engine).distinct().all()
    engines = []
    for e in raw_engines:
        eng = e[0]
        if not eng:
            continue
        if eng == "N/A":  # 👈 тут условие, можешь менять сам
            continue
        engines.append(eng)
    engines = sorted(set(engines))

    years = [y[0] for y in db.session.query(Car.year).distinct().order_by(Car.year.desc()).all()]

    if current_user.is_authenticated:
        user_liked_car_ids = [like.car_id for like in current_user.liked_cars]
    else:
        user_liked_car_ids = []

    return render_template(
        'cars.html',
        cars=cars_on_page,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        makes=makes,
        models=models,
        engines=engines,
        years=years,
        selected_make=make_filter,
        selected_model=model_filter,
        selected_engine=engine_filter,
        selected_year_from=year_from,
        selected_year_to=year_to,
        min_price=min_price,
        max_price=max_price,
        user_liked_car_ids=user_liked_car_ids
    )

@app.route("/get_models/<make>")
def get_models(make):
    models = db.session.query(Car.model).filter(Car.make == make).all()
    unique_models = sorted({m[0].split()[0] for m in models if m[0]})  # CR-V вместо CR-V LX
    return jsonify(models=unique_models)

@app.route("/get_engines/<model>")
def get_engines(model):
    engines = db.session.query(Car.engine).filter(Car.model.like(f"{model}%")).all()
    unique_engines = sorted({e[0] for e in engines if e[0]})
    return jsonify(engines=unique_engines)


@app.route('/parts', methods=['GET', 'POST'])
def parts():
    parts = []
    searched = False
    code = ''
    selected_brand_id = None
    brands = []

    if request.method == 'POST':
        code = request.form.get('code')
        selected_brand_id = request.form.get('brandId')
        searched = True

        # Получаем список брендов по коду
        brand_response = tehnomir_query('info/getBrandsByCode', {
            'code': code
        })

        if brand_response.get('success'):
            brands = brand_response.get('data', [])

        # Если выбран бренд — ищем только по нему, иначе как обычно
        search_payload = {
            'code': code,
            'isShowAnalogs': 0,
            'currency': 'USD'
        }

        if selected_brand_id:
            search_payload['brandId'] = int(selected_brand_id)

        response = tehnomir_query('price/search', search_payload)

        if response.get('success', False):
            for part in response.get('data', []):
                item = {
                    'productId': part.get('productId'),
                    'brandId': part.get('brandId'),
                    'brandGroupId': part.get('brandGroupId'),
                    'brand': part.get('brand'),
                    'code': part.get('code'),
                    'descriptionRus': part.get('descriptionRus'),
                    'descriptionUa': part.get('descriptionUa'),
                    'weight': part.get('weight'),
                    'isOriginal': part.get('isOriginal'),
                    'isExistProductInfo': part.get('isExistProductInfo'),
                    'rests': [],
                    'properties': [],
                    'images': [],
                    'analogs': []
                }

                for rest in part.get('rests', []):
                    item['rests'].append({
                        'priceLogo': rest.get('priceLogo'),
                        'price': rest.get('price'),
                        'currency': rest.get('currency'),
                        'quantity': rest.get('quantity'),
                        'quantityType': rest.get('quantityType'),
                        'multiplicity': rest.get('multiplicity'),
                        'priceQuality': rest.get('priceQuality'),
                        'deliveryTypeId': rest.get('deliveryTypeId'),
                        'deliveryType': rest.get('deliveryType'),
                        'deliveryTime': rest.get('deliveryTime'),
                        'deliveryDate': rest.get('deliveryDate'),
                        'deliveryPercent': rest.get('deliveryPercent'),
                        'priceChangeDate': rest.get('priceChangeDate'),
                        'isReturn': rest.get('isReturn'),
                        'isPriceFinal': rest.get('isPriceFinal'),
                    })

                # Дополнительный запрос info/getProductInfo
                if part.get('brandId') and part.get('code'):
                    detail = tehnomir_query('info/getProductInfo', {
                        'brandId': part['brandId'],
                        'code': part['code']
                    })

                    if detail.get('success', False):
                        data = detail['data']
                        item['properties'] = data.get('properties', [])
                        item['images'] = data.get('images', [])
                        item['analogs'] = data.get('analogs', [])
                        item['descriptionRus'] = data.get('descriptionRus') or item['descriptionRus']
                        item['descriptionUa'] = data.get('descriptionUa') or item['descriptionUa']
                        item['weight'] = data.get('weight') or item['weight']

                parts.append(item)

    return render_template('parts.html', parts=parts, searched=searched, code=code, brands=brands, selected_brand_id=selected_brand_id)

@app.route('/razborka/aparts')
def aparts_catalog():
    categories = Category.query.order_by(Category.name).all()
    return render_template('aparts_catalog.html', categories=categories)

@app.route('/razborka/aparts/<int:subcategory_id>')
def parts_list(subcategory_id):
    sort = request.args.get('sort')  # price_asc или price_desc
    subcategory = Subcategory.query.get_or_404(subcategory_id)

    # Получаем все детали по подкатегории
    parts = Part.query.filter_by(subcategory_id=subcategory_id).all()

    # Разделяем на с ценой и без цены
    parts_with_price = []
    parts_without_price = []

    for p in parts:
        if p.price is not None:
            parts_with_price.append(p)
        else:
            parts_without_price.append(p)

    # Сортировка только для тех, у кого есть цена
    if sort == 'price_asc':
        parts_with_price.sort(key=lambda x: x.price)
    elif sort == 'price_desc':
        parts_with_price.sort(key=lambda x: x.price, reverse=True)

    # Итоговый список: сначала с ценой, потом без
    parts = parts_with_price + parts_without_price

    return render_template(
        'aparts_list.html',
        subcategory=subcategory,
        parts=parts,
        selected_sort=sort
    )


@app.route('/add_to_new_cart', methods=['POST'])
def add_to_new_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.form
    user_id = session['user_id']

    item = NewCartItem(
        user_id=user_id,
        name=data.get('name'),
        brand=data.get('brand') or 'Volkswagen',
        price=data.get('price') or 0,
        part_code=data.get('part_code')
    )
    db.session.add(item)
    db.session.commit()
    flash("Товар додано в нову корзину", "success")
    return redirect(request.referrer or url_for('cabinet', tab='cart'))


@app.route('/remove_from_new_cart/<int:item_id>', methods=['POST'])
def remove_from_new_cart(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item = NewCartItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        flash("Товар видалено з нової корзини", "success")
    return redirect(url_for('cabinet', tab='cart'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.form
    user_id = session['user_id']

    part_code = data.get('code')
    brand = data.get('brand')
    quantity_to_add = int(data.get('quantity', 1))

    new_item = CartItem(
        user_id=user_id,
        part_code=part_code,
        brand=brand,
        price=data.get('price') or 0,
        currency=data.get('currency') or '',
        quantity=quantity_to_add,
        price_logo=data.get('priceLogo') or '',
        price_quality=safe_int(data.get('priceQuality')),
        is_price_final=data.get('isPriceFinal') == 'true',
        is_return=data.get('isReturn') == 'true',
        delivery_type=data.get('deliveryType') or '',
        delivery_time=data.get('deliveryTime') or ''
    )

    db.session.add(new_item)
    db.session.commit()

    flash("Додано до кошика", "success")
    return redirect(request.referrer or url_for('parts'))


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item = CartItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        flash('Товар видалено з кошика', 'success')
    return redirect(url_for('cabinet', tab='cart'))


@app.route('/checkot', methods=['POST'])
def checkot():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    for item in cart_items:
        available_quantity = get_available_quantity(item.part_code)  # тут виклик до API або БД
        if item.quantity > available_quantity:
            flash(f"На жаль, доступно лише {available_quantity} од. для {item.part_code}", "danger")
            return redirect(url_for('cabinet', tab='cart'))


@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        flash("Кошик порожній", "warning")
        return redirect(url_for('cabinet', tab='cart'))

    # Отримання даних з форми
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    city = request.form.get('city')
    np_office = request.form.get('np_office')

    # Створення замовлення
    order = Order(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        city=city,
        np_office=np_office
    )
    db.session.add(order)
    db.session.flush()  # Щоб отримати order.id до commit

    # Додавання товарів із кошика до order_items
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            part_code=item.part_code,
            brand=item.brand,
            price=item.price,
            currency=item.currency,
            quantity=item.quantity,
            delivery_type=item.delivery_type,
            delivery_time=item.delivery_time,
            is_return=item.is_return,
            price_logo=item.price_logo,
            price_quality=item.price_quality,
            is_price_final=item.is_price_final
        )
        db.session.add(order_item)

    # Очищення кошика
    CartItem.query.filter_by(user_id=user_id).delete()

    db.session.commit()
    flash("Замовлення оформлено успішно", "success")
    return redirect(url_for('cabinet'))

@app.route('/checkout_new', methods=['POST'])
def checkout_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cart_items = NewCartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        flash("Нова корзина порожня", "warning")
        return redirect(url_for('cabinet', tab='cart'))

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    city = request.form.get('city')
    np_office = request.form.get('np_office')

    order = NewOrder(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        city=city,
        np_office=np_office
    )
    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        order_item = NewOrderItem(
            order_id=order.id,
            name=item.name,
            brand=item.brand,
            price=item.price,
            part_code=item.part_code
        )
        db.session.add(order_item)

    NewCartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    flash("Замовлення з нової корзини оформлено успішно", "success")
    return redirect(url_for('cabinet'))


@app.route('/admin/orders')
def admin_orders():
    if not session.get('is_admin'):
        abort(403)

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@app.route('/update_cart_quantity/<int:item_id>', methods=['POST'])
def update_cart_quantity(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    new_quantity = int(request.form.get('quantity', 1))
    if new_quantity < 1:
        flash("Кількість має бути більше 0", "warning")
        return redirect(url_for('cabinet', tab='cart'))

    item = CartItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        item.quantity = new_quantity
        db.session.commit()
        flash("Кількість оновлено", "success")

    return redirect(url_for('cabinet', tab='cart'))



@app.route('/get_brands', methods=['POST'])
def get_brands():
    code = request.json.get('code')
    if not code:
        return jsonify({'success': False, 'brands': []})

    response = tehnomir_query('info/getBrandsByCode', {'code': code})

    if response.get('success'):
        brands = response['data']
        return jsonify({'success': True, 'brands': brands})
    return jsonify({'success': False, 'brands': []})


@app.route('/like/<int:car_id>', methods=['POST'])
@login_required
def toggle_like(car_id):
    existing_like = Like.query.filter_by(user_id=current_user.id, car_id=car_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        action = "unliked"
    else:
        new_like = Like(user_id=current_user.id, car_id=car_id)
        db.session.add(new_like)
        db.session.commit()
        action = "liked"

    # Якщо це AJAX-запит — повертаємо JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "ok", "action": action})

    # Інакше — звичайний редірект
    return redirect(request.referrer)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    car = Car.query.get_or_404(car_id)

    if current_user.is_authenticated:
        user_liked_car_ids = [like.car_id for like in current_user.liked_cars]
    else:
        user_liked_car_ids = []

    return render_template('car_details.html', car=car, user_liked_car_ids=user_liked_car_ids)

@app.route('/razborka')
def razborka():
    return render_template("razborka.html")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/calculator')
def calculator():
    return render_template("calculator.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
