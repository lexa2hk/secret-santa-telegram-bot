import os
import psycopg
from psycopg.rows import tuple_row
from psycopg_pool import ConnectionPool
from typing import Optional, List, Tuple
import random
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        # Get database connection parameters from environment
        self.db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://secretsanta:secretsanta@localhost:5432/secretsanta"
        )

        # Initialize connection pool
        try:
            self.pool = ConnectionPool(
                self.db_url,
                min_size=2,
                max_size=10,
                timeout=30,
                max_idle=300,  # 5 minutes
                max_lifetime=3600,  # 1 hour
            )
            logger.info("Database connection pool initialized")
            self.init_db()
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_connection(self):
        """Get a connection from the pool"""
        return self.pool.connection()

    def init_db(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # Groups table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS groups (
                        group_id BIGINT PRIMARY KEY,
                        admin_id BIGINT NOT NULL,
                        event_date TEXT,
                        max_price REAL,
                        language TEXT DEFAULT 'ru',
                        is_assigned BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Participants table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS participants (
                        id SERIAL PRIMARY KEY,
                        group_id BIGINT NOT NULL,
                        user_id BIGINT NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        assigned_to BIGINT,
                        wish TEXT,
                        FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
                        UNIQUE(group_id, user_id)
                    )
                """)

                # Add wish column if it doesn't exist (migration)
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns
                            WHERE table_name = 'participants' AND column_name = 'wish'
                        ) THEN
                            ALTER TABLE participants ADD COLUMN wish TEXT;
                        END IF;
                    END $$;
                """)

                conn.commit()
                logger.info("Database tables initialized")

    def create_group(self, group_id: int, admin_id: int) -> bool:
        """Create a new Secret Santa group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO groups (group_id, admin_id)
                        VALUES (%s, %s)
                        ON CONFLICT (group_id)
                        DO UPDATE SET admin_id = EXCLUDED.admin_id
                        """,
                        (group_id, admin_id)
                    )
                    conn.commit()
                    return True
        except psycopg.Error as e:
            logger.error(f"Error creating group {group_id}: {e}")
            return False

    def get_group(self, group_id: int) -> Optional[Tuple]:
        """Get group information"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT group_id, admin_id, event_date, max_price, language, is_assigned
                        FROM groups WHERE group_id = %s
                        """,
                        (group_id,)
                    )
                    result = cursor.fetchone()
                    return result
        except psycopg.Error as e:
            logger.error(f"Error getting group {group_id}: {e}")
            return None

    def update_group_settings(self, group_id: int, event_date: Optional[str] = None, max_price: Optional[float] = None) -> bool:
        """Update group settings"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    if event_date is not None:
                        cursor.execute(
                            "UPDATE groups SET event_date = %s WHERE group_id = %s",
                            (event_date, group_id)
                        )

                    if max_price is not None:
                        cursor.execute(
                            "UPDATE groups SET max_price = %s WHERE group_id = %s",
                            (max_price, group_id)
                        )

                    conn.commit()
                    return True
        except psycopg.Error as e:
            logger.error(f"Error updating group settings for {group_id}: {e}")
            return False

    def add_participant(self, group_id: int, user_id: int, username: Optional[str], first_name: Optional[str]) -> bool:
        """Add a participant to a group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO participants (group_id, user_id, username, first_name)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (group_id, user_id) DO NOTHING
                        """,
                        (group_id, user_id, username, first_name)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg.Error as e:
            logger.error(f"Error adding participant {user_id} to group {group_id}: {e}")
            return False

    def get_participants(self, group_id: int) -> List[Tuple]:
        """Get all participants in a group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT user_id, username, first_name, assigned_to
                        FROM participants WHERE group_id = %s
                        """,
                        (group_id,)
                    )
                    results = cursor.fetchall()
                    return results
        except psycopg.Error as e:
            logger.error(f"Error getting participants for group {group_id}: {e}")
            return []

    def assign_secret_santas(self, group_id: int) -> bool:
        """Randomly assign Secret Santas ensuring no one gets themselves"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get all participants
                    cursor.execute(
                        "SELECT user_id FROM participants WHERE group_id = %s",
                        (group_id,)
                    )
                    participants = [row[0] for row in cursor.fetchall()]

                    if len(participants) < 2:
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
                            """
                            UPDATE participants
                            SET assigned_to = %s
                            WHERE group_id = %s AND user_id = %s
                            """,
                            (receiver, group_id, giver)
                        )

                    # Mark group as assigned
                    cursor.execute(
                        "UPDATE groups SET is_assigned = TRUE WHERE group_id = %s",
                        (group_id,)
                    )

                    conn.commit()
                    logger.info(f"Secret Santas assigned for group {group_id}")
                    return True
        except psycopg.Error as e:
            logger.error(f"Error assigning secret santas for group {group_id}: {e}")
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
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT p2.user_id, p2.username, p2.first_name, p2.wish
                        FROM participants p1
                        JOIN participants p2 ON p1.assigned_to = p2.user_id AND p1.group_id = p2.group_id
                        WHERE p1.group_id = %s AND p1.user_id = %s
                    """, (group_id, user_id))
                    result = cursor.fetchone()
                    return result
        except psycopg.Error as e:
            logger.error(f"Error getting assignment for user {user_id} in group {group_id}: {e}")
            return None

    def is_group_assigned(self, group_id: int) -> bool:
        """Check if Secret Santas have been assigned for a group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT is_assigned FROM groups WHERE group_id = %s", (group_id,))
                    result = cursor.fetchone()
                    return result[0] if result else False
        except psycopg.Error as e:
            logger.error(f"Error checking if group {group_id} is assigned: {e}")
            return False

    def get_language(self, group_id: int) -> str:
        """Get language preference for a group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT language FROM groups WHERE group_id = %s", (group_id,))
                    result = cursor.fetchone()
                    return result[0] if result else "ru"
        except psycopg.Error as e:
            logger.error(f"Error getting language for group {group_id}: {e}")
            return "ru"

    def set_language(self, group_id: int, language: str) -> bool:
        """Set language preference for a group"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE groups SET language = %s WHERE group_id = %s",
                        (language, group_id)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg.Error as e:
            logger.error(f"Error setting language for group {group_id}: {e}")
            return False

    def get_user_groups(self, user_id: int) -> List[Tuple]:
        """Get all groups where user is a participant with assigned Secret Santas"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT DISTINCT g.group_id, g.language
                        FROM participants p
                        JOIN groups g ON p.group_id = g.group_id
                        WHERE p.user_id = %s AND g.is_assigned = TRUE
                    """, (user_id,))
                    results = cursor.fetchall()
                    return results
        except psycopg.Error as e:
            logger.error(f"Error getting user groups for user {user_id}: {e}")
            return []

    def get_secret_santa_for_user(self, group_id: int, user_id: int) -> Optional[Tuple]:
        """Get who is the Secret Santa for a given user (reverse lookup of assignment)"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT user_id, username, first_name
                        FROM participants
                        WHERE group_id = %s AND assigned_to = %s
                    """, (group_id, user_id))
                    result = cursor.fetchone()
                    return result
        except psycopg.Error as e:
            logger.error(f"Error getting secret santa for user {user_id} in group {group_id}: {e}")
            return None

    def set_wish(self, group_id: int, user_id: int, wish: str) -> bool:
        """Set a wish for a participant"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE participants
                        SET wish = %s
                        WHERE group_id = %s AND user_id = %s
                    """, (wish, group_id, user_id))
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg.Error as e:
            logger.error(f"Error setting wish for user {user_id} in group {group_id}: {e}")
            return False

    def get_wish(self, group_id: int, user_id: int) -> Optional[str]:
        """Get a participant's wish"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT wish
                        FROM participants
                        WHERE group_id = %s AND user_id = %s
                    """, (group_id, user_id))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except psycopg.Error as e:
            logger.error(f"Error getting wish for user {user_id} in group {group_id}: {e}")
            return None

    def close(self):
        """Close the connection pool"""
        if hasattr(self, 'pool'):
            self.pool.close()
            logger.info("Database connection pool closed")
