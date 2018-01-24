import unittest
import sqlalchemy
import datetime
from LanguageDeck.models import Cards, associations, Base, decks
import LanguageDeck.ui.cards as cds
import LanguageDeck.ui.decks as dks


def create_test_db():
    engine = sqlalchemy.create_engine('sqlite://')
    Base.metadata.schema = ""
    Base.metadata.create_all(engine)
    return engine


class UITests(unittest.TestCase):

    def setUp(self):
        import sqlalchemy.orm

        self.engine = None
        self.engine = create_test_db()
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sess = self.session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.sess.close()

    def test_get_text(self):
        c = Cards.LanguageAVocab(text="heythere!")
        ans = cds.get_text(c)
        self.assertEqual(ans, "heythere!")

    def test_get_translations(self):
        c = Cards.LanguageAVocab(text="hello")
        v1 = Cards.LanguageBVocab(text="hallo")
        v2 = Cards.LanguageBVocab(text="gutentag")

        self.sess.add(c)
        self.sess.add(v1)
        self.sess.add(v2)

        self.sess.commit()

        c.translations.append(v1)
        c.translations.append(v2)

        self.sess.commit()

        ans = cds.get_translations(c)
        self.assertEqual(ans, [v1, v2])

        e = Cards.LanguageAExample(text="this is an example")
        t1 = Cards.LanguageBExample(text="Diese ist ein Beispiel")

        self.sess.add(e)
        self.sess.add(t1)
        e.translations.append(t1)
        self.sess.commit()

        ans = cds.get_translations(e)
        self.assertEqual(ans, [t1])

    def test_get_score(self):
        c = Cards.LanguageBExample(text="hallo, bob")
        u1 = Cards.User(name="user1")
        u2 = Cards.User(name="user2")

        self.sess.add_all([c, u1, u2])
        self.sess.commit()

        s1 = associations.LanguageBExampleScore(user_id=u1.id, card_id=c.id, score=3)
        s2 = associations.LanguageBExampleScore(user_id=u2.id, card_id=c.id, score=1)

        self.sess.add_all([s1, s2])
        self.sess.commit()

        self.assertEqual(c.scores, [s1, s2])

        probe = cds.get_score(self.sess, u1, c)
        ans = 3
        self.assertEqual(probe, ans)

        probe = cds.get_score(self.sess, u2, c)
        ans = 1
        self.assertEqual(probe, ans)

    def test_get_creation_date(self):
        c = Cards.LanguageAExample(text="dude, howdyeedoo!")

        self.sess.add(c)
        self.sess.commit()

        probe = cds.get_creation_date(c)
        ans = datetime.date.today()
        self.assertEqual(probe, ans)

    def test_get_paradigms(self):
        c = Cards.LanguageBVocab(text="laufen", g_type="verb")
        g1 = Cards.Grammar(paradigm="laufe, laeufst, laeuft", irregular=True)
        g2 = Cards.Grammar(paradigm="laufe, laufst, lauft", irregular=True)

        self.sess.add_all([c, g1, g2])
        self.sess.commit()

        c.grammar.append(g1)
        c.grammar.append(g2)

        self.sess.commit()

        probe = cds.get_paradigms(c)
        ans = [g1, g2]
        self.assertEqual(probe, ans)

    def test_edit_text(self):
        c = Cards.LanguageBVocab(text="GutenTag", g_type="idiom")
        self.sess.add(c)
        self.sess.commit()

        cds.edit_text(c, "g'day")

        probe = cds.get_text(c)
        ans = "g'day"
        self.assertEqual(probe, ans)

    def test_edit_score(self):
        import LanguageDeck.session_tools.session_scope as scp

        c = Cards.LanguageBVocab(text="Es sieht aus, wie du errungen hast.")
        u1 = Cards.User(name="dude")
        self.sess.add_all([c, u1])
        self.sess.commit()

        with scp.session_scope(self.session) as sess:
            cds.edit_score(sess, c, u1, 8)

        with scp.session_scope(self.session) as sess:
            probe = cds.get_score(sess, u1, c)
            ans = 8
            self.assertEqual(probe, ans)

        with scp.session_scope(self.session) as sess:
            cds.edit_score(sess, c, u1, 3)

        with scp.session_scope(self.session) as sess:

            c = sess.query(Cards.LanguageBVocab).filter_by(id=c.id).one()
            probe = cds.get_score(self.sess, u1, c)
            ans = 3
            self.assertEqual(probe, ans)

    def test_edit_date_touched(self):
        import LanguageDeck.session_tools.session_scope as scp

        with scp.session_scope(self.session) as sess:
            c = Cards.LanguageBVocab(text="Es sieht aus, wie du errungen hast.")

            d1 = datetime.date(2017, 4, 3)
            sess.add_all([c])
            sess.commit()

            cds.edit_date_touched(c, d1)
            sess.commit()

            probe = cds.get_touch_date(c)
            ans = datetime.date(2017, 4, 3)
            self.assertEqual(probe, ans)

            d2 = datetime.date(2017, 5, 2)
            cds.edit_date_touched(c, d2)
            sess.commit()

            probe = cds.get_touch_date(c)
            ans = datetime.date(2017, 5, 2)
            self.assertEqual(probe, ans)

    def test_edit_paradigm(self):
        import LanguageDeck.session_tools.session_scope as scp
        with scp.session_scope(self.session) as sess:
            c1 = Cards.LanguageAVocab(text="error")
            c2 = Cards.Grammar(paradigm="old paradigm")

            sess.add_all([c1, c2])
            sess.commit()

            try:
                cds.edit_g_paradigm(c1, "new paradigm")
            except AssertionError:
                print("caught assertion error")

            cds.edit_g_paradigm(c2, "new paradigm")
            sess.commit()

            probe = cds.get_paradigm_content(c2)
            ans = "new paradigm"
            self.assertEqual(probe, ans)

    def test_get_examples(self):
        import LanguageDeck.session_tools.session_scope as scp
        with scp.session_scope(self.session) as sess:
            cv1 = Cards.LanguageBVocab(text="allerdings", g_type="prep")
            ce1 = Cards.LanguageBExample(text="Es ist allerdings moeglich")
            ce2 = Cards.LanguageBExample(text="allerdings, du bist verklapt.")

            sess.add_all([cv1, ce1, ce2])
            sess.commit()

            probe = cds.get_examples(cv1)
            ans = []
            self.assertEqual(probe, ans)

            cv1.examples.append(ce1)
            cv1.examples.append(ce2)

            sess.commit()

            probe = cds.get_examples(cv1)
            ans = [ce1, ce2]
            self.assertEqual(probe, ans)

    def test_add_examples(self):
        import LanguageDeck.session_tools.session_scope as scp
        with scp.session_scope(self.session) as sess:
            cvb = Cards.LanguageBVocab(text="lbv")
            cvb2 = Cards.LanguageBVocab(text="lbv2")
            cva = Cards.LanguageAVocab(text="lav")
            ceb = Cards.LanguageBExample(text="example lbv")
            cea = Cards.LanguageAExample(text="example lav")

            sess.add_all([cvb, cvb2, cva, ceb, cea])
            sess.commit()

            cds.add_example(cvb, ceb)
            sess.commit()
            probe = cds.get_examples(cvb)
            ans = [ceb]
            self.assertEqual(probe, ans)

            cds.add_example(cvb2, ceb)
            sess.commit()
            probe = cds.get_examples(cvb2)
            ans = [ceb]
            self.assertEqual(probe, ans)

            cds.add_example(cva, cea)
            sess.commit()
            probe = cds.get_examples(cva)
            ans = [cea]
            self.assertEqual(probe, ans)

            cds.add_example(cvb, ceb)
            cds.add_example(cvb, ceb)
            sess.commit()
            probe = cds.get_examples(cvb)
            ans = [ceb]
            self.assertEqual(probe, ans)

    def test_add_translations(self):
        c = Cards.LanguageBVocab(text="Morgen")
        tr1 = Cards.LanguageAVocab(text="Morning")
        tr2 = Cards.LanguageAVocab(text="tomorrow")
        tr3 = Cards.LanguageAExample(text="not supposed to be here")

        self.sess.add_all([c, tr1, tr2, tr3])
        self.sess.commit()

        cds.add_translation(c, tr1)

        probe = cds.get_translations(c)
        ans = [tr1]
        self.assertEqual(probe, ans)

        cds.add_translation(c, tr2)

        probe = cds.get_translations(c)
        ans = [tr1, tr2]
        self.assertEqual(probe, ans)

        try:
            cds.add_translation(c, tr3)
            self.assertTrue(False)
        except AssertionError:
            print("caught assertion error")

    def test_add_grammar(self):
        c = Cards.LanguageBVocab(text="machen")
        g = Cards.Grammar(paradigm="machen, mache, machst, macht...")

        self.sess.add_all([c, g])

        cds.add_grammar(c, g)

        probe = cds.get_paradigms(c)
        ans = [g]
        self.assertEqual(probe, ans)

    def test_remove_grammar(self):
        c = Cards.LanguageBVocab(text="machen")
        g = Cards.Grammar(paradigm="this is a grammar")
        g2 = Cards.Grammar(paradigm="this is also a grammar")
        g3 = Cards.Grammar(paradigm="this grammar is not in c")

        self.sess.add_all([c, g, g2, g3])

        c.grammar += [g, g2]
        self.sess.commit()

        self.assertEqual(cds.get_paradigms(c), [g, g2])

        cds.remove_grammar(c, g)
        self.sess.commit()

        c = self.sess.query(Cards.LanguageBVocab).filter_by(id=1).one()
        probe = cds.get_paradigms(c)
        ans = [g2]

        self.assertEqual(probe, ans)

        try:
            cds.remove_grammar(c, g3)
            self.fail()
        except AssertionError:
            print("Caught assertion error")

    def test_remove_translation(self):
        c = Cards.LanguageBVocab(text="machen")
        tr1 = Cards.LanguageAVocab(text="this is a translation")
        tr2 = Cards.LanguageAVocab(text="this is not a translation")

        self.sess.add_all([c, tr1, tr2])

        c.translations.append(tr1)
        self.sess.commit()

        self.assertEqual(cds.get_translations(c), [tr1])

        cds.remove_translation(c, tr1)

        probe = cds.get_translations(c)
        ans = []
        self.assertEqual(probe, ans)

        try:
            cds.remove_translation(c, tr2)
            self.fail()
        except AssertionError:
            print("Caught assertion error")

    def test_remove_examples(self):
        c = Cards.LanguageBVocab(text="machen")
        tr1 = Cards.LanguageBExample(text="this is a translation")
        tr2 = Cards.LanguageBExample(text="this is not a translation")

        self.sess.add_all([c, tr1, tr2])

        c.examples.append(tr1)
        self.sess.commit()

        self.assertEqual(cds.get_examples(c), [tr1])

        cds.remove_example(c, tr1)
        self.sess.commit()

        c = self.sess.query(Cards.LanguageBVocab).filter_by(id=1).one()

        probe = cds.get_examples(c)
        ans = []
        self.assertEqual(probe, ans)

        try:
            cds.remove_example(c, tr2)
            self.fail()
        except AssertionError:
            print("Caught assertion error")


class DecksTests(unittest.TestCase):
    """Test cases for the decs object"""

    def setUp(self):
        import sqlalchemy.orm

        self.engine = None
        self.engine = create_test_db()
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.sess = self.session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.sess.close()

    def test_add_card(self):
        d = decks.Deck(name="Testdeck")
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        self.sess.add_all([d, cb, cb2, ca1, cea1, ceb1])

        self.sess.commit()

        self.assertEqual(d.examples_a, [])
        self.assertEqual(d.examples_b, [])
        self.assertEqual(d.vocab_a, [])
        self.assertEqual(d.vocab_b, [])

        dks.add_card(d, cb)
        self.sess.commit()

        self.assertEqual(d.examples_a, [])
        self.assertEqual(d.examples_b, [])
        self.assertEqual(d.vocab_a, [])
        self.assertEqual(d.vocab_b, [cb])

        dks.add_card(d, cb2)
        dks.add_card(d, ca1)
        dks.add_card(d, cea1)
        dks.add_card(d, ceb1)

        self.sess.commit()

        self.assertEqual(d.examples_a, [cea1])
        self.assertEqual(d.examples_b, [ceb1])
        self.assertEqual(d.vocab_a, [ca1])
        self.assertEqual(d.vocab_b, [cb, cb2])

        try:
            dks.add_card(d, 4)
            self.fail("assertion error was not caught")
        except AssertionError:
            print("assertion error caught")

    def test_get_low_scores(self):
        d = decks.Deck(name="Testdeck")
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        u = Cards.User(name="jack")

        self.sess.add_all([d, cb, cb2, ca1, cea1, ceb1, u])

        self.sess.commit()

        dks.add_card(d, cb)
        dks.add_card(d, cb2)
        dks.add_card(d, ca1)
        dks.add_card(d, cea1)
        dks.add_card(d, ceb1)

        cds.edit_score(self.sess, cb, u, 5)
        cds.edit_score(self.sess, cb2, u, 10)
        cds.edit_score(self.sess, ceb1, u, 8)

        u.decks.append(d)

        self.sess.commit()

        probe = dks.get_low_scores(self.sess, d, 3)
        ans = []
        self.assertEqual(probe, ans)

        probe = dks.get_low_scores(self.sess, d, 7)
        ans = [cb]

        self.assertEqual(probe, ans)

        probe = dks.get_low_scores(self.sess, d, 9)
        ans = [cb, ceb1]
        self.assertEqual(probe, ans)

    def test_add_all_cards(self):
        d = decks.Deck(name="Testdeck")
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        u = Cards.User(name="jack")

        self.sess.add_all([d, cb, cb2, ca1, cea1, ceb1, u])

        self.sess.commit()

        dks.add_all_cards(d, [cb, cb2, ca1, cea1, ceb1])

        self.sess.commit()

        probe = dks.get_examples_a(d)
        ans = [cea1]
        self.assertEqual(probe, ans)

        probe = dks.get_examples_b(d)
        ans = [ceb1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_a(d)
        ans = [ca1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_b(d)
        ans = [cb, cb2]
        self.assertEqual(probe, ans)

    def test_remove_cards(self):
        d = decks.Deck(name="Testdeck")
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        u = Cards.User(name="jack")

        self.sess.add_all([d, cb, cb2, ca1, cea1, u])

        self.sess.commit()

        dks.add_all_cards(d, [cb, cb2, ca1, cea1])

        self.sess.commit()

        dks.remove_card(d, cb)

        self.sess.commit()

        probe = dks.get_vocab_b(d)
        ans = [cb2]
        self.assertEqual(probe, ans)

        dks.remove_card(d, ca1)
        self.sess.commit()

        self.assertEqual(dks.get_vocab_a(d), [])

        dks.remove_card(d, cea1)
        self.sess.commit()

        self.assertEqual(dks.get_examples_a(d), [])

        try:
            dks.remove_card(d, ceb1)
            self.sess.commit()

            self.fail()

        except ValueError:

            print("value error caught")

    def test_new_deck(self):
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        u = Cards.User(name="jack")

        self.sess.add_all([cb, cb2, ca1, cea1, ceb1, u])

        self.sess.commit()

        d = dks.new_deck(self.sess, [cb, cb2, ca1, cea1, ceb1], u, "test_deck")

        self.sess.commit()

        probe = dks.get_examples_a(d)
        ans = [cea1]
        self.assertEqual(probe, ans)

        probe = dks.get_examples_b(d)
        ans = [ceb1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_a(d)
        ans = [ca1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_b(d)
        ans = [cb, cb2]
        self.assertEqual(probe, ans)

        probe = d.user_id
        ans = u.id
        self.assertEqual(probe, ans)

    def test_clone_deck(self):
        d = decks.Deck(name="Testdeck")
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")

        u = Cards.User(name="jack")
        u2 = Cards.User(name="jill")

        self.sess.add_all([d, cb, cb2, ca1, cea1, u, ceb1, u2])

        self.sess.commit()

        dks.add_all_cards(d, [cb, cb2, ca1, cea1, ceb1])

        self.sess.commit()

        d2 = dks.clone_deck(self.sess, d, u2, "cloned deck")

        self.sess.commit()

        probe = dks.get_examples_a(d2)
        ans = [cea1]
        self.assertEqual(probe, ans)

        probe = dks.get_examples_b(d2)
        ans = [ceb1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_a(d2)
        ans = [ca1]
        self.assertEqual(probe, ans)

        probe = dks.get_vocab_b(d2)
        ans = [cb, cb2]
        self.assertEqual(probe, ans)

        self.assertEqual(d2.name, "cloned deck")
        self.assertEqual(d2.user, u2)

    def test_delete_deck(self):
        d = decks.Deck(name="Testdeck")
        self.sess.add(d)
        self.sess.commit()

        alldecks = self.sess.query(decks.Deck).all()
        self.assertEqual(alldecks, [d])

        dks.delete_deck(self.sess, d)
        self.sess.commit()

        alldecks = self.sess.query(decks.Deck).all()
        self.assertEqual(alldecks, [])

        # Deletion of decks should not delete cards
        cb = Cards.LanguageBVocab(text="worte1")
        cb2 = Cards.LanguageBVocab(text="worte2")
        ca1 = Cards.LanguageAVocab(text="word1")
        cea1 = Cards.LanguageAExample(text="example1")
        ceb1 = Cards.LanguageBExample(text="Beispiel1")
        self.sess.add_all([cb, cb2, ca1, cea1, ceb1])
        self.sess.commit()

        d = decks.Deck(name="Testdeck")
        self.sess.add(d)
        self.sess.commit()

        dks.add_all_cards(d, [cb, cb2, ca1, cea1, ceb1])
        self.sess.commit()

        dks.delete_deck(self.sess, d)
        self.sess.commit()

        bvocab = self.sess.query(Cards.LanguageBVocab).all()

        self.assertTrue(cb in bvocab)
        self.assertTrue(cb2 in bvocab)
        self.assertEqual(len(bvocab), 2)


if __name__ == "__main__":
    unittest.main()
