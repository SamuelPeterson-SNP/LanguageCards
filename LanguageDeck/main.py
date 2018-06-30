import sqlalchemy
import configparser
import LanguageDeck.session_tools.session_scope as s_scope
import LanguageDeck.ui.DeckView as dkv
import tkinter as tk

if __name__ == "__main__":
    import LanguageDeck.models as models

    config = configparser.ConfigParser()
    config.read('config.ini')

    engine = sqlalchemy.create_engine(config['connection']['connection_string'], echo=True)
    models.Base.metadata.create_all(engine)
    session = sqlalchemy.orm.sessionmaker(bind=engine)
    with s_scope.session_scope(session) as sess:
        deck = sess.query(models.decks.Deck).filter_by(name="master").one_or_none()
        if not deck:
            deck = models.decks.Deck(name="master")

    root = tk.Tk()
    ap = dkv.BrowseDeckView(deck, root, session)
    ap.mainloop()

