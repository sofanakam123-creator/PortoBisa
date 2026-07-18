from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from model import get_db_connection

admin_login_bp = Blueprint('admin_login', __name__, url_prefix='/admin')

@admin_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    return redirect(url_for('admin_dashboard.dashboard'))
                else:
                    flash('Username atau Password salah!', 'error')
            conn.close()
        else:
            flash('Database connection failed', 'error')
            
    return render_template('admin/login.html')

@admin_login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_login.login'))
