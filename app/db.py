"""
Database module - SQLite operations for users and leads.

This module handles:
- Database initialization
- User language preferences
- Lead (application) storage and retrieval

Design: All functions are pure and side effects are explicit.
Testing: Connection can be injected for testing purposes.
"""
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Create and return database connection.
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        SQLite connection with row factory enabled
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    """
    Initialize database schema - create users and leads tables.
    
    Args:
        db_path: Path to SQLite database file
        
    Side effects:
        - Creates database file if it doesn't exist
        - Creates tables if they don't exist
        - Prints confirmation message
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_user_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL CHECK(language IN ('ru', 'me', 'en')),
            created_at TEXT NOT NULL
        )
    """)
    
    # Leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            description TEXT NOT NULL,
            files TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")


def get_user_language(tg_user_id: int, db_path: str) -> Optional[str]:
    """
    Get user's selected language.
    
    Args:
        tg_user_id: Telegram user ID
        db_path: Path to database file
        
    Returns:
        Language code ('ru', 'me', 'en') or None if user not found
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT language FROM users WHERE tg_user_id = ?",
        (tg_user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return result['language'] if result else None


def save_user_language(tg_user_id: int, language: str, db_path: str) -> None:
    """
    Save user's selected language.
    
    Args:
        tg_user_id: Telegram user ID
        language: Language code ('ru', 'me', 'en')
        db_path: Path to database file
        
    Raises:
        ValueError: If language code is invalid
    """
    valid_languages = {'ru', 'me', 'en'}
    if language not in valid_languages:
        raise ValueError(f"Invalid language code: {language}. Must be one of {valid_languages}")
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO users (tg_user_id, language, created_at)
        VALUES (?, ?, ?)
    """, (
        tg_user_id,
        language,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()


def save_lead(
    tg_user_id: int,
    full_name: str,
    phone: str,
    description: str,
    db_path: str,
    email: Optional[str] = None,
    files: Optional[str] = None
) -> int:
    """
    Save lead (application) to database.
    
    Args:
        tg_user_id: Telegram user ID
        full_name: User's full name
        phone: Phone number
        description: Project description
        db_path: Path to database file
        email: Email address (optional)
        files: JSON string with file IDs (optional)
        
    Returns:
        ID of created lead
        
    Raises:
        ValueError: If required fields are empty or invalid
    """
    # Validate required fields
    if not full_name or not full_name.strip():
        raise ValueError("Full name cannot be empty")
    if not phone or not phone.strip():
        raise ValueError("Phone cannot be empty")
    if not description or not description.strip():
        raise ValueError("Description cannot be empty")
    if len(description.strip()) < 10:
        raise ValueError("Description must be at least 10 characters")
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO leads (tg_user_id, full_name, phone, email, description, files, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        tg_user_id,
        full_name.strip(),
        phone.strip(),
        email.strip() if email else None,
        description.strip(),
        files,
        datetime.now().isoformat()
    ))
    
    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return lead_id


def get_last_lead_by_user(tg_user_id: int, db_path: str) -> Optional[Dict[str, Any]]:
    """
    Get last lead submitted by user (for pre-filling repeat applications).
    
    Args:
        tg_user_id: Telegram user ID
        db_path: Path to database file
        
    Returns:
        Dictionary with lead data or None if no previous leads
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM leads WHERE tg_user_id = ? ORDER BY created_at DESC LIMIT 1",
        (tg_user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None


def get_lead_by_id(lead_id: int, db_path: str) -> Optional[Dict[str, Any]]:
    """
    Get lead by ID.
    
    Args:
        lead_id: Lead ID
        db_path: Path to database file
        
    Returns:
        Dictionary with lead data or None if not found
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None


def get_all_leads(db_path: str) -> list[Dict[str, Any]]:
    """
    Get all leads ordered by creation date (newest first).
    
    Args:
        db_path: Path to database file
        
    Returns:
        List of lead dictionaries
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def get_user_leads(tg_user_id: int, db_path: str) -> list[Dict[str, Any]]:
    """
    Get all leads for specific user.
    
    Args:
        tg_user_id: Telegram user ID
        db_path: Path to database file
        
    Returns:
        List of user's lead dictionaries
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM leads WHERE tg_user_id = ? ORDER BY created_at DESC",
        (tg_user_id,)
    )
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]


def delete_lead(lead_id: int, tg_user_id: int, db_path: str) -> bool:
    """
    Delete lead from database.
    
    Verifies that lead belongs to the user before deletion.
    
    Args:
        lead_id: Lead ID to delete
        tg_user_id: Telegram user ID (for verification)
        db_path: Path to database file
        
    Returns:
        True if deleted, False if lead not found or doesn't belong to user
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Verify lead belongs to user
    cursor.execute(
        "SELECT id FROM leads WHERE id = ? AND tg_user_id = ?",
        (lead_id, tg_user_id)
    )
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return False
    
    # Delete lead
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    
    return True
