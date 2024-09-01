# app/routes/main.py
import random
from flask import Blueprint, render_template, request, jsonify, url_for, \
    flash, redirect
# from app.models import Service, BlogPost
from app import db
from app.utils import send_email

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """
    Renders the home page of the web application.

    This function serves as the view for the root URL of the web application.
    It renders the 'index.html' template with a context variable 'title'
    that is set to 'Home'.

    Returns:
        Response: A Flask Response object containing the rendered HTML of
        the home page.
    :return:
    """
    return render_template('index.html', title='Home')


@bp.route('/features')
def features():
    """Renders the Features page of the web application."""
    return render_template('features.html', title='Features')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/how')
def how():
    """Renders the How it works page of the web application."""
    return render_template('how-it-works.html', title='How It Works')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Renders the Contact me page of the web application."""
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Construct email content
        text_body = f"""
            You have received a new message from the contact form on your website.

            Details:
            ---------
            Name: {name}
            Email: {email}
            Subject: {subject}

            Message:
            --------
            {message}

            Best regards,
            EcoGuide App - Your personal assistant for sustainable living
            """

        html_body = f"""
            <html>
            <head>
                <style>
                    .email-container {{
                        font-family: Arial, sans-serif;
                        color: #333;
                        line-height: 1.5;
                    }}
                    .email-header {{
                        background-color: #f8f8f8;
                        padding: 10px;
                        border-bottom: 2px solid #ddd;
                    }}
                    .email-content {{
                        padding: 20px;
                    }}
                    .email-footer {{
                        margin-top: 20px;
                        padding: 10px;
                        background-color: #f8f8f8;
                        border-top: 2px solid #ddd;
                        text-align: center;
                        font-size: 0.9em;
                        color: #777;
                    }}
                    .email-footer a {{
                        color: #333;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h2>New Contact Form Submission</h2>
                    </div>
                    <div class="email-content">
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>Subject:</strong> {subject}</p>
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                    </div>
                    <div class="email-footer">
                        <p>Best regards,<br>Your Website</p>
                        <p><a href="https://emtechzambia.net">Visit our website</a></p>
                    </div>
                </div>
            </body>
            </html>
            """

        # Send email
        try:
            send_email(
                subject=subject,
                sender=email,
                recipients=['martinnyemba@gmail.com'],
                text_body=text_body,
                html_body=html_body
            )
            return jsonify({'success': True, 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'An error occurred while sending your message. Please try again later.'})

    return render_template('contact.html', title='Contact Us')
