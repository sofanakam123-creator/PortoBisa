from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import get_db_connection
from Backend.admin.upload import upload_image

admin_profiles_bp = Blueprint('admin_profiles', __name__, url_prefix='/admin')

@admin_profiles_bp.route('/profiles', methods=['GET', 'POST'])
def profiles():
    if 'user_id' not in session:
        return redirect(url_for('admin_login.login'))
        
    conn = get_db_connection()
    user_id = session['user_id']
    
    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap')
        nama_panggilan = request.form.get('nama_panggilan')
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        email = request.form.get('email')
        telepon = request.form.get('telepon')
        universitas = request.form.get('universitas')
        fakultas = request.form.get('fakultas')
        prodi = request.form.get('prodi')
        semester = request.form.get('semester')
        alamat = request.form.get('alamat')
        
        file = request.files.get('foto')
        foto_url = upload_image(file) if file else None

        if conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, foto_url FROM profiles WHERE user_id = %s', (user_id,))
                existing = cursor.fetchone()
                
                if foto_url is None and existing:
                    foto_url = existing['foto_url']
                    
                if existing:
                    cursor.execute('''
                        UPDATE profiles SET 
                        nama_lengkap=%s, nama_panggilan=%s, tempat_lahir=%s, tanggal_lahir=%s, 
                        email=%s, telepon=%s, universitas=%s, fakultas=%s, prodi=%s, 
                        semester=%s, alamat=%s, foto_url=%s
                        WHERE user_id=%s
                    ''', (nama_lengkap, nama_panggilan, tempat_lahir, tanggal_lahir, email, telepon, 
                          universitas, fakultas, prodi, semester, alamat, foto_url, user_id))
                else:
                    cursor.execute('''
                        INSERT INTO profiles 
                        (user_id, nama_lengkap, nama_panggilan, tempat_lahir, tanggal_lahir, email, telepon, universitas, fakultas, prodi, semester, alamat, foto_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (user_id, nama_lengkap, nama_panggilan, tempat_lahir, tanggal_lahir, email, telepon, universitas, fakultas, prodi, semester, alamat, foto_url))
                conn.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('admin_profiles.profiles'))

    profile = None
    if conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM profiles WHERE user_id = %s', (user_id,))
            profile = cursor.fetchone()
        conn.close()
        
    return render_template('admin/profiles.html', profile=profile)
