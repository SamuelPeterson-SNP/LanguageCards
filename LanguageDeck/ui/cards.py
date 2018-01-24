import datetime
from LanguageDeck.models import Cards
"""Interface for Card and Deck objects.  Contains the obvious observer, creator and mutator functions"""


def get_text(card):
    return str(card.text)


def get_translations(card):
    return card.translations


def get_score(session, user, card):
    if card.scores:
        s = session.query(card.score_type).filter_by(user_id=user.id, card_id=card.id).one()
        return int(s.score)
    else:
        return None


def get_examples(card):
    return card.examples


def get_creation_date(card):
    if card.date_created:
        d = card.date_created
        return datetime.date(d.year, d.month, d.day)
    return None


def get_touch_date(card):
    if card.date_last_touched:
        d = card.date_last_touched
        return datetime.date(d.year, d.month, d.day)
    return None


def get_g_type(card):
    return str(card.g_type)


def get_paradigms(card):
    return card.grammar


def get_paradigm_content(card):
    assert type(card) == Cards.Grammar, "card must be of type Grammar"
    return str(card.paradigm)


def edit_text(card, edit):
    assert type(edit) == str, "edit must be a string."
    card.text = edit


def edit_score(session, card, user, score):
    query = session.query(card.score_type).filter_by(user_id=user.id, card_id=card.id)
    if query.count() == 0:
        score = card.score_type(card_id=card.id, user_id=user.id, score=score)
        session.add(score)
    else:
        q = query.one()
        q.score = score


def edit_date_touched(card, date):
    card.date_last_touched = date


def edit_g_paradigm(card, edit):
    assert type(card) == Cards.Grammar, "card type needs to be Grammar"
    card.paradigm = edit


def add_example(card, example):
    assert type(example) == card.example_type, "incorrect example type"
    card.examples.append(example)


def add_translation(card, translation):
    assert Cards.translation_types[type(card)] == type(translation), "wrong card type for translation"
    card.translations.append(translation)


def add_grammar(card, grammar):
    assert type(grammar) == Cards.Grammar, "Can only insert Grammar class"
    assert type(card) == Cards.LanguageBVocab, "Only LanguageBVocab cards have a grammar property"
    card.grammar.append(grammar)


def remove_grammar(card, grammar):
    assert type(grammar) == Cards.Grammar, "Can only insert Grammar class"
    assert type(card) == Cards.LanguageBVocab, "Only LanguageBVocab cards have a grammar property"
    assert grammar in card.grammar, "grammar object not in card"

    card.grammar.remove(grammar)


def remove_example(card, example):
    assert example in card.examples, "example not in card"
    card.examples.remove(example)


def remove_translation(card, translation):
    assert translation in card.translations, "translation not in card"
    card.translations.remove(translation)
