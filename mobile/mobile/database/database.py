import sqlite3
from pathlib import Path
from datetime import datetime


DB_NAME = "frahoosh.db"


class Database:

    def __init__(self):

        self.path = Path(DB_NAME)

        self.conn = sqlite3.connect(
            self.path,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self.create_tables()



    def create_tables(self):

        cursor = self.conn.cursor()


        # ==========================
        # SCHOOL INFO
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS school_info (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                school_name TEXT,

                academic_year TEXT,

                manager_name TEXT,

                phone TEXT,

                address TEXT,

                logo TEXT

            )
            """
        )


        # ==========================
        # USERS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                national_code TEXT UNIQUE,

                password_hash TEXT,

                first_name TEXT,

                last_name TEXT,

                role TEXT,

                mobile TEXT,

                active INTEGER DEFAULT 1,

                must_change_password INTEGER DEFAULT 1,

                created_at TEXT

            )
            """
        )


        # ==========================
        # STUDENTS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                national_code TEXT UNIQUE,

                first_name TEXT,

                last_name TEXT,

                grade TEXT,

                class_name TEXT,

                parent_id INTEGER,

                created_at TEXT

            )
            """
        )


        # ==========================
        # PARENTS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS parents (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                national_code TEXT UNIQUE,

                first_name TEXT,

                last_name TEXT,

                mobile TEXT,

                student_id INTEGER

            )
            """
        )


        # ==========================
        # TEACHERS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teachers (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                national_code TEXT UNIQUE,

                first_name TEXT,

                last_name TEXT,

                subject TEXT,

                mobile TEXT

            )
            """
        )


        # ==========================
        # CLASSES
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS classes (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,

                grade TEXT,

                teacher_id INTEGER,

                capacity INTEGER

            )
            """
        )


        # ==========================
        # PAYMENTS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER,

                parent_id INTEGER,

                title TEXT,

                amount INTEGER,

                payment_date TEXT,

                gateway TEXT,

                transaction_id TEXT,

                status TEXT

            )
            """
        )


        # ==========================
        # MESSAGES
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sender_id INTEGER,

                receiver_id INTEGER,

                message TEXT,

                created_at TEXT,

                status TEXT

            )
            """
        )


        # ==========================
        # ATTENDANCE
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attendance (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER,

                date TEXT,

                status TEXT

            )
            """
        )


        # ==========================
        # SETTINGS
        # ==========================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                key TEXT UNIQUE,

                value TEXT

            )
            """
        )


        self.conn.commit()



    # ==========================
    # INSERT
    # ==========================

    def insert(
        self,
        table,
        data
    ):

        keys = ",".join(data.keys())

        values = tuple(
            data.values()
        )


        placeholders = ",".join(
            ["?"] * len(values)
        )


        query = f"""
        INSERT INTO {table}
        ({keys})
        VALUES
        ({placeholders})
        """


        cursor = self.conn.cursor()

        cursor.execute(
            query,
            values
        )


        self.conn.commit()

        return cursor.lastrowid



    # ==========================
    # SELECT ONE
    # ==========================

    def fetch_one(
        self,
        query,
        params=()
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            query,
            params
        )

        return cursor.fetchone()



    # ==========================
    # SELECT ALL
    # ==========================

    def fetch_all(
        self,
        query,
        params=()
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            query,
            params
        )

        return cursor.fetchall()



    # ==========================
    # EXECUTE
    # ==========================

    def execute(
        self,
        query,
        params=()
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            query,
            params
        )

        self.conn.commit()

        return cursor

         
