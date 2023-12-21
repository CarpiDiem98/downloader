def create_annotation(cursor, title, url):
    """
    Create a new annotation in the database.

    Args:
        cursor: The database cursor.
        id: The ID of the annotation.
        title: The title of the annotation.
        url: The URL of the annotation.

    Returns:
        None
    """
    cursor.execute(
        """
        INSERT INTO annotations (title, url) VALUES (?, ?)
        """,
        (title, url),
    )


def read_annotation(cursor, id):
    cursor.execute(
        """
        SELECT * FROM annotations WHERE id = ?
        """,
        (id,),
    )
    return cursor.fetchone()


def update_annotation(cursor, id, title, url):
    cursor.execute(
        """
        UPDATE annotations SET title = ?, url = ? WHERE id = ?
        """,
        (title, url, id),
    )


def delete_annotation(cursor, id):
    cursor.execute(
        """
        DELETE FROM annotations WHERE id = ?
        """,
        (id,),
    )
