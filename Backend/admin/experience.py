from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_db_connection

admin_experience_bp = Blueprint('admin_experience', __name__, url_prefix='/admin')

@admin_experience_bp.route('/experience', methods=['GET', 'POST'])
def experience():
    if 'user_id' not in session:
        return redirect(url_for('admin_login.login'))
        
    conn = get_db_connection()
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            posisi = request.form.get('posisi')
            perusahaan = request.form.get('perusahaan')
            durasi = request.form.get('durasi')
            deskripsi = request.form.get('deskripsi')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO experiences (user_id, posisi, perusahaan, durasi, deskripsi) VALUES (%s, %s, %s, %s, %s)', 
                                   (user_id, posisi, perusahaan, durasi, deskripsi))
                    conn.commit()
                flash('Experience added successfully!', 'success')
                
        elif action == 'edit':
            exp_id = request.form.get('exp_id')
            posisi = request.form.get('posisi')
            perusahaan = request.form.get('perusahaan')
            durasi = request.form.get('durasi')
            deskripsi = request.form.get('deskripsi')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE experiences SET posisi=%s, perusahaan=%s, durasi=%s, deskripsi=%s WHERE id=%s AND user_id=%s', 
                                   (posisi, perusahaan, durasi, deskripsi, exp_id, user_id))
                    conn.commit()
                flash('Experience updated successfully!', 'success')
                
        elif action == 'delete':
            exp_id = request.form.get('exp_id')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM experiences WHERE id=%s AND user_id=%s', (exp_id, user_id))
                    conn.commit()
                flash('Experience deleted successfully!', 'success')
                
        return redirect(url_for('admin_experience.experience'))

    exp_list = []
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM experiences WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
            exp_list = cursor.fetchall()
        conn.close()
        
    return render_template('admin/experience.html', experiences=exp_list)
