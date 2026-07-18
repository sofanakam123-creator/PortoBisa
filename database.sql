
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nama_lengkap VARCHAR(100),
    nama_panggilan VARCHAR(50),
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    email VARCHAR(100),
    telepon VARCHAR(20),
    universitas VARCHAR(100),
    fakultas VARCHAR(100),
    prodi VARCHAR(100),
    semester VARCHAR(20),
    alamat TEXT,
    foto_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nama_skill VARCHAR(50) NOT NULL,
    icon_class VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    posisi VARCHAR(100) NOT NULL,
    perusahaan VARCHAR(100) NOT NULL,
    durasi VARCHAR(50),
    deskripsi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    judul VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    gambar_url VARCHAR(255),
    link_project VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default admin user (password is 'admin123' using pbkdf2:sha256)
-- Password hash generated using: werkzeug.security.generate_password_hash('admin123')
INSERT INTO users (username, password_hash, role) 
VALUES ('admin', 'scrypt:32768:8:1$DkZ2T1Y2H1sVvA8k$360822180860361395b282d8c3606b297a7a102927e1f4404cf9833783a48e895b6c31a721d0ab91df79075be8c0ed6a74601362e847c211cc5cf39f99e3ab2b', 'admin')
ON DUPLICATE KEY UPDATE username=username;
