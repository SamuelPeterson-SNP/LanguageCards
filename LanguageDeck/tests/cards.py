import unittest
import sqlalchemy
import datetime
from LanguageDeck.models import Cards, associations, Base, decks


def create_test_db():
    engine = sqlalchemy.create_engine('sqlite://')
    Base.metadata.create_all(engine)
    return engine


class VocabTests(unittest.TestCase):

    def setUp(self):
        import sqlalchemy.orm

        self.engine = None
        self.engine = create_test_db()
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sess = self.session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.sess.close()

    def test_sql_ids(self):
        worda = Cards.LanguageAVocab(text="word1")
        self.sess.add(worda)
        print("id is: {ids}".format(ids=worda.id))
        self.sess.flush()
        print("id is: {ids}".format(ids=worda.id))
        self.sess.commit()
        print("id is: {ids}".format(ids=worda.id))

    def test_translations(self):

        worda = Cards.LanguageAVocab(text="word1", date_created=datetime.date.today())
        self.sess.add(worda)

        wordb = Cards.LanguageAVocab()
        wordb.text = "word2"
        wordb.date_created = datetime.date.today()
        self.sess.add(wordb)

        fwordc = Cards.LanguageBVocab()
        fwordc.text = "translation11"
        fwordc.date_created = datetime.date.today()
        fwordc.translations.append(worda)
        self.sess.add(fwordc)

        fwordd = Cards.LanguageBVocab()
        fwordd.text = "translation12"
        fwordd.date_created = datetime.date.today()
        fwordd.translations.append(worda)
        fwordd.translations.append(wordb)
        self.sess.add(fwordd)

        self.sess.commit()

        self.assertEqual(worda.text, "word1")
        translations = [a.text for a in self.sess.query(Cards.LanguageAVocab).filter_by(id=worda.id).all()[0].
                        translations]

        self.assertTrue("translation11" in translations)
        self.assertTrue("translation12" in translations)

        translations = [a.text for a in self.sess.query(Cards.LanguageAVocab).filter_by(id=wordb.id).all()[0].
                        translations]
        self.assertTrue("translation11" not in translations)
        self.assertTrue("translation12" in translations)

    def test_deletions(self):

        worda = Cards.LanguageAVocab(text="word1", date_created=datetime.date.today())
        self.sess.add(worda)

        wordb = Cards.LanguageAVocab()
        wordb.text = "word2"
        wordb.date_created = datetime.date.today()
        self.sess.add(wordb)

        fwordc = Cards.LanguageBVocab()
        fwordc.text = "translation11"
        fwordc.date_created = datetime.date.today()
        fwordc.translations.append(worda)
        self.sess.add(fwordc)

        fwordd = Cards.LanguageBVocab()
        fwordd.text = "translation12"
        fwordd.date_created = datetime.date.today()
        fwordd.translations.append(worda)
        fwordd.translations.append(wordb)

        self.sess.add(fwordd)
        self.sess.commit()

        self.sess.delete(fwordc)
        self.sess.commit()

        self.assertTrue(len(self.sess.query(Cards.LanguageAVocab).filter_by(id=worda.id).one().translations) == 1)
        self.assertEqual(self.sess.query(Cards.LanguageAVocab).filter_by(id=worda.id).one().translations[0], fwordd)

        self.sess.delete(worda)
        self.sess.commit()

        self.assertTrue(len(self.sess.query(Cards.LanguageAVocab).filter_by(id=wordb.id).one().translations) == 1)

        user = Cards.User(name="bob")
        user2 = Cards.User(name="sally")
        self.sess.add(user)
        self.sess.add(user2)
        self.sess.commit()

        las = associations.LanguageAVocabScore(user_id=1, card_id=2, score=3)
        las2 = associations.LanguageAVocabScore(user_id=2, card_id=2, score=5)

        wordb.scores.append(las)
        wordb.scores.append(las2)

        self.sess.commit()

        self.assertEqual(self.sess.query(associations.LanguageAVocabScore).filter_by(card_id=2, user_id=1).one().score,
                         3)

        self.sess.delete(user2)
        self.sess.commit()

        self.assertEqual(len(self.sess.query(associations.LanguageAVocabScore).all()), 1)

        self.sess.delete(wordb)
        self.sess.commit()

        self.assertEqual(len(self.sess.query(associations.LanguageAVocabScore).all()), 0)

    def test_b_b_examples(self):

        worda = Cards.LanguageBVocab(text="Ergebnis", date_created=datetime.date.today())
        wordb = Cards.LanguageBVocab(text="doch", date_created=datetime.date.today())
        example1 = Cards.LanguageBExample(text="Die Ergebnis ist Unklar", date_created=datetime.date.today())
        example2 = Cards.LanguageBExample(text="Die Ergebnis ist doch Klar", date_created=datetime.date.today())
        example3 = Cards.LanguageBExample(text="Doch du hast es", date_created=datetime.date.today())

        self.sess.add(worda)
        self.sess.add(wordb)
        self.sess.add(example1)
        self.sess.add(example2)
        self.sess.add(example3)

        example1.words.append(worda)
        example2.words.append(worda)
        example2.words.append(wordb)
        example3.words.append(wordb)

        self.sess.commit()

        eb = self.sess.query(Cards.LanguageBExample).filter_by(id=2).one()
        self.assertEqual(len(eb.words), 2)
        ea = self.sess.query(Cards.LanguageBExample).filter_by(id=1).one()
        self.assertEqual(len(ea.words), 1)

        self.sess.delete(worda)
        self.sess.commit()

        eb = self.sess.query(Cards.LanguageBExample).filter_by(id=2).one()
        self.assertEqual(len(eb.words), 1)
        ea = self.sess.query(Cards.LanguageBExample).filter_by(id=1).one()
        self.assertEqual(len(ea.words), 0)

        self.sess.delete(example2)
        self.sess.commit()

        wb = self.sess.query(Cards.LanguageBVocab).filter_by(id=2).one()
        self.assertEqual(len(wb.examples), 1)
        self.assertTrue(wb.examples[0].text, "Doch du hast es")

    def test_grammar(self):
        worda = Cards.LanguageBVocab(text="Ergebnis", date_created=datetime.date.today(), g_type="Noun, m")
        wordb = Cards.LanguageBVocab(text="drucken", date_created=datetime.date.today())
        wordc = Cards.LanguageBVocab(text="weil")

        grammar_b = Cards.Grammar(irregular=False, paradigm="drucken, drucke, druckst, druckt, etc")
        grammar_c = Cards.Grammar(paradigm="der Ergebnis, die Ergebnisse")

        self.sess.add(worda)
        self.sess.add(wordb)
        self.sess.add(wordc)

        self.sess.add(grammar_b)
        self.sess.add(grammar_c)

        worda.grammar.append(grammar_c)
        wordb.grammar.append(grammar_b)

        self.sess.commit()

        wa = self.sess.query(Cards.LanguageBVocab).filter_by(id=1).one()
        self.assertEqual(wa.g_type, "Noun, m")

        self.sess.delete(grammar_c)
        self.sess.commit()

        wa = self.sess.query(Cards.LanguageBVocab).filter_by(id=1).one()
        self.assertEqual(len(wa.grammar), 0)

        print(type(worda.text))
        print(str(worda.text))
        print(type(str(worda.text)))
        print(datetime.date(worda.date_created.year, worda.date_created.month, worda.date_created.day))

    def test_decks(self):
        user = Cards.User(name="Samuel")
        decka = decks.Deck(name="decka")

        vocabaa = Cards.LanguageAVocab(text="howdy")
        vocabba = Cards.LanguageBVocab(text="gutentag")
        vocabbb = Cards.LanguageBVocab(text="wie geht's")
        exampleaa = Cards.LanguageAExample(text="dude, I'm an example")
        exampleba = Cards.LanguageBExample(text="Je, Ich bin ein Beispiel")

        self.sess.add(user)
        self.sess.add(decka)
        self.sess.add(vocabaa)
        self.sess.add(vocabba)
        self.sess.add(vocabbb)
        self.sess.add(exampleaa)
        self.sess.add(exampleba)

        decka.user_id = user.id
        decka.vocab_a.append(vocabaa)
        decka.vocab_b.append(vocabba)
        decka.vocab_b.append(vocabbb)
        decka.examples_a.append(exampleaa)
        decka.examples_b.append(exampleba)

        self.sess.commit()

        d = self.sess.query(type(decka)).filter_by(id=1).one()
        self.assertEqual(len(d.vocab_a), 1)
        self.assertEqual(len(d.vocab_b), 2)
        self.assertEqual(len(d.examples_a), 1)
        self.assertEqual(len(d.examples_b), 1)

        self.sess.delete(vocabbb)
        self.sess.commit()

        self.assertEqual(len(d.vocab_b), 1)

        self.sess.delete(decka)
        self.sess.commit()

        self.assertEqual(vocabaa.text, "howdy")


if __name__ == "__main__":
    unittest.main()
