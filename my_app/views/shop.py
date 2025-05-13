"""
Blueprint для основных страниц магазина
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, abort
from sqlalchemy import func
from my_app.extensions import db
from my_app.models import Product, Category, Visitor

# Создаем Blueprint
shop_bp = Blueprint('shop', __name__, url_prefix='')

@shop_bp.route('/')
def home():
    """Главная страница"""
    # Получаем популярные товары
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    
    # Получаем новинки
    new_products = Product.query.filter_by(is_new=True).order_by(Product.created_at.desc()).limit(8).all()
    
    # Получаем товары со скидкой
    sale_products = Product.query.filter_by(is_sale=True).order_by(Product.created_at.desc()).limit(8).all()
    
    # Получаем категории для меню
    categories = Category.query.filter_by(parent_id=None).all()
    
    # Статистика
    stats = {
        'products_count': Product.query.count(),
        'categories_count': Category.query.count(),
    }
    
    # Получаем статистику посетителей
    try:
        visitor_stats = Visitor.get_visitors_stats()
        stats.update(visitor_stats)
    except Exception as e:
        current_app.logger.error(f"Ошибка получения статистики посетителей: {str(e)}")
    
    return render_template('index.html', 
                          featured_products=featured_products,
                          new_products=new_products,
                          sale_products=sale_products,
                          categories=categories,
                          stats=stats)

@shop_bp.route('/catalog')
def catalog():
    """Страница каталога"""
    categories = Category.query.filter_by(parent_id=None).all()
    return render_template('catalog.html', categories=categories)

@shop_bp.route('/category/<int:category_id>')
def category(category_id):
    """Страница категории"""
    category = Category.query.get_or_404(category_id)
    
    # Получаем все товары в этой категории
    products = Product.query.filter_by(category_id=category_id).all()
    
    # Получаем подкатегории
    subcategories = Category.query.filter_by(parent_id=category_id).all()
    
    return render_template('category.html', 
                          category=category, 
                          products=products, 
                          subcategories=subcategories)

@shop_bp.route('/product/<int:product_id>')
def product(product_id):
    """Страница товара"""
    product = Product.query.get_or_404(product_id)
    
    # Добавляем товар в список просмотренных, если его там еще нет
    if 'visited_products' not in session:
        session['visited_products'] = []
    
    visited_products = session['visited_products']
    if product_id not in visited_products:
        visited_products.append(product_id)
        session['visited_products'] = visited_products[:10]  # Храним только 10 последних
    
    return render_template('product.html', product=product)

@shop_bp.route('/search')
def search():
    """Поиск товаров"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('shop.catalog'))
    
    # Поиск товаров с похожим названием
    products = Product.query.filter(
        Product.name.ilike(f'%{query}%') | 
        Product.description.ilike(f'%{query}%')
    ).all()
    
    # Поиск категорий с похожим названием
    categories = Category.query.filter(
        Category.name.ilike(f'%{query}%')
    ).all()
    
    return render_template('search_results.html', 
                          query=query, 
                          products=products, 
                          categories=categories) 