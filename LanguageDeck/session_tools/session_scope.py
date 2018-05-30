from contextlib import contextmanager

@contextmanager
def session_scope(session_factory):
    """Provide transaction scope arround a series of operations."""
    sess = session_factory()
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()
