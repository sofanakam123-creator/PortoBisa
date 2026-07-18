import os
from flask import Flask
from config import Config

def create_app():
    # Using 'Frontend' as template and static folder to match project structure
    app = Flask(__name__, template_folder='Frontend', static_folder='Frontend')
    app.config.from_object(Config)
    
    
    from Backend.admin.login import admin_login_bp
    from Backend.admin.dashboard import admin_dashboard_bp
    from Backend.admin.profiles import admin_profiles_bp
    from Backend.admin.skills import admin_skills_bp
    from Backend.admin.experience import admin_experience_bp
    from Backend.admin.projects import admin_projects_bp
    from Backend.utama.utama import utama_bp

    # Register blueprints
    app.register_blueprint(admin_login_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_profiles_bp)
    app.register_blueprint(admin_skills_bp)
    app.register_blueprint(admin_experience_bp)
    app.register_blueprint(admin_projects_bp)
    app.register_blueprint(utama_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
