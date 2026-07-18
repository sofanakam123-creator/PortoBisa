from flask import Blueprint, render_template, request, flash, redirect, url_for
from model import get_db_connection
import resend
from config import Config

utama_bp = Blueprint('utama', __name__)
resend.api_key = Config.RESEND_API_KEY

@utama_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        try:
            r = resend.Emails.send({
                "from": "Portfolio <onboarding@resend.dev>",
                "to": "delivered@resend.dev",  # Using resend's testing email or replace with real
                "subject": f"New Contact Message from {name}",
                "html": f"<p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong><br>{message}</p>"
            })
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            print(e)
            flash('Failed to send message. Please try again later.', 'error')
            
        return redirect(url_for('utama.index') + '#contact')

    # Fetch data for the portfolio
    conn = get_db_connection()
    data = {'profile': None, 'skills': [], 'experiences': [], 'projects': []}
    
    if conn:
        with conn.cursor() as cursor:
            # Assuming we display the first user's profile (admin)
            cursor.execute('SELECT id FROM users ORDER BY id ASC LIMIT 1')
            user = cursor.fetchone()
            if user:
                user_id = user['id']
                cursor.execute('SELECT * FROM profiles WHERE user_id = %s', (user_id,))
                data['profile'] = cursor.fetchone()
                
                cursor.execute('SELECT * FROM skills WHERE user_id = %s', (user_id,))
                data['skills'] = cursor.fetchall()
                
                cursor.execute('SELECT * FROM experiences WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
                data['experiences'] = cursor.fetchall()
                
                cursor.execute('SELECT * FROM projects WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
                data['projects'] = cursor.fetchall()
        conn.close()

    return render_template('utama/index.html', data=data)
