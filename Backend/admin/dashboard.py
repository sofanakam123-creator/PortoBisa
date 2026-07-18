from flask import Blueprint, render_template, session, redirect, url_for
from model import get_db_connection

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard_bp.route('/')
@admin_dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('admin_login.login'))
        
    conn = get_db_connection()
    stats = {'projects': 0, 'skills': 0, 'experience': 0}
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) as c FROM projects WHERE user_id = %s', (session['user_id'],))
            stats['projects'] = cursor.fetchone()['c']
            cursor.execute('SELECT COUNT(*) as c FROM skills WHERE user_id = %s', (session['user_id'],))
            stats['skills'] = cursor.fetchone()['c']
            cursor.execute('SELECT COUNT(*) as c FROM experiences WHERE user_id = %s', (session['user_id'],))
            stats['experience'] = cursor.fetchone()['c']
        conn.close()
        
    return render_template('admin/dashboard.html', stats=stats)
