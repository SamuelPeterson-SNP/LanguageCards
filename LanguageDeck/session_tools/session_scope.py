from contextlib import contextmanager


@contextmanager
def session_scope(session_factory, **args):
    """Provide transaction scope arround a series of operations."""
    sess = session_factory(**args)
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()
