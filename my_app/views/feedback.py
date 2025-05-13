"""
Blueprint для обработки форм обратной связи
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from my_app.extensions import db
from my_app.models import FeedbackMessage
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Создаем Blueprint
feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/submit', methods=['POST'])
def submit():
    """Обработка формы обратной связи"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        message_text = request.form.get('message')
        recipient_email = request.form.get('recipient_email', 'qqdslk@gmail.com')
        
        # Создаем тему сообщения
        subject = f"Обратная связь от {name}"
        
        # Формируем сообщение для записи в базу данных
        feedback = FeedbackMessage(
            name=name,
            email=email,
            subject=subject,
            message=f"Телефон: {phone}\n\n{message_text}"
        )
        
        try:
            # Сохраняем сообщение в базу данных
            db.session.add(feedback)
            db.session.commit()
            
            # Отправляем email
            send_email(recipient_email, subject, name, email, phone, message_text)
            
            # Уведомляем пользователя об успешной отправке
            flash('Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.', 'success')
        except Exception as e:
            # Логируем ошибку
            current_app.logger.error(f"Ошибка при отправке сообщения: {str(e)}")
            flash('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'error')
            db.session.rollback()
    
    # Перенаправляем на страницу контактов
    return redirect(url_for('static_pages.contact'))


def send_email(recipient, subject, name, sender_email, phone, message_text):
    """Отправляет электронное письмо с данными формы обратной связи"""
    try:
        # Формируем текст письма
        email_content = f"""
        Новое сообщение с формы обратной связи!
        
        Имя: {name}
        Email: {sender_email}
        Телефон: {phone}
        
        Сообщение:
        {message_text}
        
        Дата отправки: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        """
        
        # Создаем объект сообщения
        msg = EmailMessage()
        msg.set_content(email_content)
        
        # Указываем заголовки
        msg['Subject'] = subject
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = recipient
        
        # Отправляем сообщение
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            if current_app.config['MAIL_USE_TLS']:
                server.starttls()
            
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            server.send_message(msg)
        
        return True
    except Exception as e:
        current_app.logger.error(f"Ошибка отправки email: {str(e)}")
        return False 