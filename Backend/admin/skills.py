from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_db_connection

admin_skills_bp = Blueprint('admin_skills', __name__, url_prefix='/admin')

@admin_skills_bp.route('/skills', methods=['GET', 'POST'])
def skills():
    if 'user_id' not in session:
        return redirect(url_for('admin_login.login'))
        
    conn = get_db_connection()
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            nama_skill = request.form.get('nama_skill')
            icon_class = request.form.get('icon_class')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO skills (user_id, nama_skill, icon_class) VALUES (%s, %s, %s)', 
                                   (user_id, nama_skill, icon_class))
                    conn.commit()
                flash('Skill added successfully!', 'success')
                
        elif action == 'edit':
            skill_id = request.form.get('skill_id')
            nama_skill = request.form.get('nama_skill')
            icon_class = request.form.get('icon_class')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE skills SET nama_skill=%s, icon_class=%s WHERE id=%s AND user_id=%s', 
                                   (nama_skill, icon_class, skill_id, user_id))
                    conn.commit()
                flash('Skill updated successfully!', 'success')
                
        elif action == 'delete':
            skill_id = request.form.get('skill_id')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM skills WHERE id=%s AND user_id=%s', (skill_id, user_id))
                    conn.commit()
                flash('Skill deleted successfully!', 'success')
                
        return redirect(url_for('admin_skills.skills'))

    skills_list = []
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM skills WHERE user_id = %s', (user_id,))
            skills_list = cursor.fetchall()
        conn.close()
        
    return render_template('admin/skills.html', skills=skills_list)
