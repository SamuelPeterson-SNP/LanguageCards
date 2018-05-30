import sqlalchemy
import tkinter as tk
import LanguageDeck.ui.CardView as cdv

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

    sess.add(user)
    sess.add(decka)
    sess.add(vocabaa)
    sess.add(vocabba)
    sess.add(vocabbb)
    sess.add(exampleaa)
    sess.add(exampleba)
    sess.add(va12)
    sess.add(va21)
    sess.add(exb2)

    sess.commit()

    cds.add_translation(vocabaa, vocabba)
    cds.add_translation(va12, vocabba)
    cds.add_translation(va21, vocabbb)
    cds.add_example(vocabba, exampleba)
    cds.add_example(vocabba, exb2)

    sess.commit()


    root = tk.Tk()
    ap = cdv.CardView(vocabba, master=root, session_factory=session)
    ap.mainloop()



