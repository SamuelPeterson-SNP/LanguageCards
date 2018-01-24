# User interface for Decks object.  includes get, add, remove, clone, new methods.
import LanguageDeck.models.Cards as Cards
import LanguageDeck.models.decks as dks
import LanguageDeck.models.associations as assoc
import datetime


def get_all_cards(deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    return {"vocab_a": deck.vocab_a, "vocab_b": deck.vocab_b, "examples_a": deck.examples_a,
            "examples_b": deck.examples_b}


def get_vocab_a(deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    return deck.vocab_a


def get_vocab_b(deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    return deck.vocab_b


def get_examples_a(deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    return deck.examples_a


def get_examples_b(deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    return deck.examples_b


def get_low_scores(session, deck, score):
    assert type(deck) == dks.Deck, "deck must by a Deck type"

    va = session.query(Cards.LanguageAVocab).join(assoc.LanguageAVocabScore,
                                                  Cards.LanguageAVocab.id == assoc.LanguageAVocabScore.card_id).\
        filter(assoc.LanguageAVocabScore.score < score, assoc.LanguageAVocabScore.user_id == deck.user_id).all()

    vb = session.query(Cards.LanguageBVocab).join(assoc.LanguageBVocabScore,
                                                  Cards.LanguageBVocab.id == assoc.LanguageBVocabScore.card_id).\
        filter(assoc.LanguageBVocabScore.score < score, assoc.LanguageBVocabScore.user_id == deck.user_id).all()

    vbe = session.query(Cards.LanguageBExample).join(assoc.LanguageBExampleScore,
                                                     Cards.LanguageBExample.id == assoc.LanguageBExampleScore.card_id).\
        filter(assoc.LanguageBExampleScore.score < score, assoc.LanguageBExampleScore.user_id == deck.user_id).all()

    return va + vb + vbe


def add_card(deck, card):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    assert type(card) in [Cards.LanguageBExample, Cards.LanguageBVocab, Cards.LanguageAExample, Cards.LanguageAVocab], \
        "card must be a language card type"

    if type(card) == Cards.LanguageAVocab:
        deck.vocab_a.append(card)

    elif type(card) == Cards.LanguageBVocab:
        deck.vocab_b.append(card)

    elif type(card) == Cards.LanguageAExample:
        deck.examples_a.append(card)

    else:
        deck.examples_b.append(card)


def add_all_cards(deck, cards):
    for c in cards:
        add_card(deck, c)


def remove_card(deck, card):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    assert type(card) in [Cards.LanguageBExample, Cards.LanguageBVocab, Cards.LanguageAExample, Cards.LanguageAVocab], \
        "card must be a language card type"

    if type(card) == Cards.LanguageAVocab:
        deck.vocab_a.remove(card)

    elif type(card) == Cards.LanguageBVocab:
        deck.vocab_b.remove(card)

    elif type(card) == Cards.LanguageAExample:
        deck.examples_a.remove(card)

    elif type(card) == Cards.LanguageBExample:
        deck.examples_b.remove(card)


def new_deck(session, cards, user, name):
    ret = dks.Deck(name=name, date_created=datetime.date.today())
    ret.user = user
    add_all_cards(ret, cards)
    session.add(ret)
    return ret


def clone_deck(session, deck, user, name):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    ret = dks.Deck(name=name)

    add_all_cards(ret, deck.vocab_b + deck.vocab_a + deck.examples_a + deck.examples_b)
    ret.user = user
    session.add(ret)

    return ret


def delete_deck(session, deck):
    assert type(deck) == dks.Deck, "deck must by a Deck type"
    session.delete(deck)
