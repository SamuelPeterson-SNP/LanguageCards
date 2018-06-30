import sqlalchemy
import tkinter as tk

import LanguageDeck.ui.DeckView as dkv
import LanguageDeck.ui.decks as dks

if __name__ == "__main__":
    from LanguageDeck.models import *
    import LanguageDeck.ui.cards as cds
    engine = sqlalchemy.create_engine('sqlite://')
    Base.metadata.create_all(engine)
    session = sqlalchemy.orm.sessionmaker(bind=engine)
    sess = session()

    user = Cards.User(name="Samuel")
    decka = decks.Deck(name="decka")

    vocabaa = Cards.LanguageAVocab(text="howdy")
    va12 = Cards.LanguageAVocab(text="hello")
    vocabba = Cards.LanguageBVocab(text="gutentag")
    va21 = Cards.LanguageAVocab(text="How are you?")
    vocabbb = Cards.LanguageBVocab(text="wie geht's")
    exampleaa = Cards.LanguageAExample(text="dude, I'm an example")
    exampleba = Cards.LanguageBExample(text="Je, Ich bin ein Beispiel")
    exb2 = Cards.LanguageBExample(text="Ich bin auch ein Beispiel")

    sess.add_all([user, decka, vocabaa, va12, vocabba, va21, vocabbb, exampleaa, exampleba, exb2])

    sess.commit()

    cds.add_translation(vocabaa, vocabba)
    cds.add_translation(va12, vocabba)
    cds.add_translation(va21, vocabbb)
    cds.add_example(vocabba, exampleba)
    cds.add_example(vocabba, exb2)
    dks.add_all_cards(decka,  [vocabaa, va12, vocabba, va21, vocabbb, exampleaa, exampleba, exb2])

    sess.commit()

    root = tk.Tk()
    #ap = cdv.CardView(vocabba, master=root, session_factory=session)
    ap = dkv.BrowseDeckView(decka, root, session)
    ap.mainloop()



