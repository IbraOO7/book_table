import os

class Config:
    DB_USER = os.getenv("DB_USER", "root") 
    DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123") # Kosongkan admin123 jika konfigurasi tidak menggunkan password / sesuaikan dgn pasword db yang ada
    DB_NAME = os.getenv("DB_NAME", "db_tes")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    
    DB_CONFIG = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" # Ubah sesuai dengan database yang digunakan (Disini menggunakan mysql)



    