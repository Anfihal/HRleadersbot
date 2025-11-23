# -*- coding: utf-8 -*-
import sqlite3
import os

DATABASE_PATH = "bot_data.db"

def init_db():
    """Create DB and tables"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()

def save_user_role(user_id: int, role: str):
    """Save user role"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, role)
                VALUES (?, ?)
            ''', (user_id, role))
            conn.commit()
    except Exception as e:
        print(f"[DB] Error: {e}")