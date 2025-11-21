import sqlite3
from typing import Optional, List, Tuple
import random


class Database:
    def __init__(self, db_path: str = "secret_santa.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Groups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                admin_id INTEGER NOT NULL,
                event_date TEXT,
                max_price REAL,
                language TEXT DEFAULT 'en',
                is_assigned BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Participants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                assigned_to INTEGER,
                FOREIGN KEY (group_id) REFERENCES groups(group_id),
                UNIQUE(group_id, user_id)
            )
        """)

        conn.commit()
        conn.close()

    def create_group(self, group_id: int, admin_id: int) -> bool:
        """Create a new Secret Santa group"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO groups (group_id, admin_id) VALUES (?, ?)",
                (group_id, admin_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def get_group(self, group_id: int) -> Optional[Tuple]:
        """Get group information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT group_id, admin_id, event_date, max_price, language, is_assigned FROM groups WHERE group_id = ?",
            (group_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result

    def update_group_settings(self, group_id: int, event_date: Optional[str] = None, max_price: Optional[float] = None) -> bool:
        """Update group settings"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if event_date is not None:
                cursor.execute(
                    "UPDATE groups SET event_date = ? WHERE group_id = ?",
                    (event_date, group_id)
                )

            if max_price is not None:
                cursor.execute(
                    "UPDATE groups SET max_price = ? WHERE group_id = ?",
                    (max_price, group_id)
                )

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def add_participant(self, group_id: int, user_id: int, username: Optional[str], first_name: Optional[str]) -> bool:
        """Add a participant to a group"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO participants (group_id, user_id, username, first_name) VALUES (?, ?, ?, ?)",
                (group_id, user_id, username, first_name)
            )
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def get_participants(self, group_id: int) -> List[Tuple]:
        """Get all participants in a group"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, first_name, assigned_to FROM participants WHERE group_id = ?",
            (group_id,)
        )
        results = cursor.fetchall()
        conn.close()
        return results

    def assign_secret_santas(self, group_id: int) -> bool:
        """Randomly assign Secret Santas ensuring no one gets themselves"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Get all participants
            cursor.execute(
                "SELECT user_id FROM participants WHERE group_id = ?",
                (group_id,)
            )
            participants = [row[0] for row in cursor.fetchall()]

            if len(participants) < 2:
                conn.close()
                return False

            # Create assignments (shuffle until valid)
            assigned = participants.copy()
            max_attempts = 100
            for _ in range(max_attempts):
                random.shuffle(assigned)
                # Check if anyone got themselves
                if all(participants[i] != assigned[i] for i in range(len(participants))):
                    break
            else:
                # If we couldn't find valid assignment, use derangement algorithm
                assigned = self._derangement(participants)

            # Save assignments
            for giver, receiver in zip(participants, assigned):
                cursor.execute(
                    "UPDATE participants SET assigned_to = ? WHERE group_id = ? AND user_id = ?",
                    (receiver, group_id, giver)
                )

            # Mark group as assigned
            cursor.execute(
                "UPDATE groups SET is_assigned = 1 WHERE group_id = ?",
                (group_id,)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False

    def _derangement(self, items: List[int]) -> List[int]:
        """Create a derangement (permutation where no item is in its original position)"""
        n = len(items)
        result = items.copy()

        for i in range(n - 1):
            j = random.randint(i + 1, n - 1)
            result[i], result[j] = result[j], result[i]

        # Fix if last element is in original position
        if result[-1] == items[-1]:
            swap_idx = random.randint(0, n - 2)
            result[-1], result[swap_idx] = result[swap_idx], result[-1]

        return result

    def get_assignment(self, group_id: int, user_id: int) -> Optional[Tuple]:
        """Get the Secret Santa assignment for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p2.user_id, p2.username, p2.first_name
            FROM participants p1
            JOIN participants p2 ON p1.assigned_to = p2.user_id AND p1.group_id = p2.group_id
            WHERE p1.group_id = ? AND p1.user_id = ?
        """, (group_id, user_id))
        result = cursor.fetchone()
        conn.close()
        return result

    def is_group_assigned(self, group_id: int) -> bool:
        """Check if Secret Santas have been assigned for a group"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT is_assigned FROM groups WHERE group_id = ?", (group_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] == 1 if result else False

    def get_language(self, group_id: int) -> str:
        """Get language preference for a group"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM groups WHERE group_id = ?", (group_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "en"

    def set_language(self, group_id: int, language: str) -> bool:
        """Set language preference for a group"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE groups SET language = ? WHERE group_id = ?",
                (language, group_id)
            )
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def get_user_groups(self, user_id: int) -> List[Tuple]:
        """Get all groups where user is a participant with assigned Secret Santas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT g.group_id, g.language
            FROM participants p
            JOIN groups g ON p.group_id = g.group_id
            WHERE p.user_id = ? AND g.is_assigned = 1
        """, (user_id,))
        results = cursor.fetchall()
        conn.close()
        return results

    def get_secret_santa_for_user(self, group_id: int, user_id: int) -> Optional[Tuple]:
        """Get who is the Secret Santa for a given user (reverse lookup of assignment)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, username, first_name
            FROM participants
            WHERE group_id = ? AND assigned_to = ?
        """, (group_id, user_id))
        result = cursor.fetchone()
        conn.close()
        return result
