from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_db_connection
from Backend.admin.upload import upload_image

admin_projects_bp = Blueprint('admin_projects', __name__, url_prefix='/admin')

@admin_projects_bp.route('/projects', methods=['GET', 'POST'])
def projects():
    if 'user_id' not in session:
        return redirect(url_for('admin_login.login'))
        
    conn = get_db_connection()
    user_id = session['user_id']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            judul = request.form.get('judul')
            deskripsi = request.form.get('deskripsi')
            link_project = request.form.get('link_project')
            
            file = request.files.get('gambar')
            gambar_url = upload_image(file) if file else None

            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO projects (user_id, judul, deskripsi, gambar_url, link_project) VALUES (%s, %s, %s, %s, %s)', 
                                   (user_id, judul, deskripsi, gambar_url, link_project))
                    conn.commit()
                flash('Project added successfully!', 'success')
                
        elif action == 'edit':
            project_id = request.form.get('project_id')
            judul = request.form.get('judul')
            deskripsi = request.form.get('deskripsi')
            link_project = request.form.get('link_project')
            
            file = request.files.get('gambar')
            gambar_url = upload_image(file) if file else None
            
            if conn:
                with conn.cursor() as cursor:
                    if gambar_url:
                        cursor.execute('UPDATE projects SET judul=%s, deskripsi=%s, gambar_url=%s, link_project=%s WHERE id=%s AND user_id=%s', 
                                       (judul, deskripsi, gambar_url, link_project, project_id, user_id))
                    else:
                        cursor.execute('UPDATE projects SET judul=%s, deskripsi=%s, link_project=%s WHERE id=%s AND user_id=%s', 
                                       (judul, deskripsi, link_project, project_id, user_id))
                    conn.commit()
                flash('Project updated successfully!', 'success')
                
        elif action == 'delete':
            project_id = request.form.get('project_id')
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM projects WHERE id=%s AND user_id=%s', (project_id, user_id))
                    conn.commit()
                flash('Project deleted successfully!', 'success')
                
        return redirect(url_for('admin_projects.projects'))

    projects_list = []
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM projects WHERE user_id = %s ORDER BY created_at DESC', (user_id,))
            projects_list = cursor.fetchall()
        conn.close()
        
    return render_template('admin/projects.html', projects=projects_list)
