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
                "from": "Portfolio Contact <onboarding@resend.dev>",
                "to": "sofanakam123@gmail.com",
                "subject": f"Pesan Baru dari {name} - Portfolio Contact",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                    <h2 style="color: #8b5cf6; border-bottom: 2px solid #8b5cf6; padding-bottom: 10px;">Pesan Baru dari Portfolio</h2>
                    <p><strong>Nama:</strong> {name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                    <p><strong>Pesan:</strong></p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 4px; margin-top: 5px;">
                        {message}
                    </div>
                    <hr style="margin-top: 20px;">
                    <p style="color: #999; font-size: 12px;">Pesan ini dikirim melalui form kontak di portfolio Anda.</p>
                </div>
                """
            })
            flash('Pesan Anda berhasil terkirim! Terima kasih.', 'success')
        except Exception as e:
            print(f"Resend error: {e}")
            flash('Gagal mengirim pesan. Silakan coba lagi nanti.', 'error')
            
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
