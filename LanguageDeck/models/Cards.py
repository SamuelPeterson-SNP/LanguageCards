import sqlalchemy
import sqlalchemy.orm
from LanguageDeck.models import associations as assoc
from LanguageDeck.models import Base, decks
import datetime


# LanguageB_Example: sentences featuring language B.
# Contains the following relationships
#     * many-to-many: LanguageB_Vocab
#     * many-to-many: LanguageA_Example
#     * many-to-many association: User (record of scores)
class LanguageBExample(Base):
    __tablename__ = "lang_b_examples"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    translations = sqlalchemy.orm.relation("LanguageAExample", secondary=assoc.LAE_LBE,
                                           back_populates="translations")
    words = sqlalchemy.orm.relation("LanguageBVocab", secondary=assoc.LBV_LBE,
                                    back_populates="examples")
    scores = sqlalchemy.orm.relation(assoc.LanguageBExampleScore, cascade="all")
    date_created = sqlalchemy.Column("date_created", sqlalchemy.Date, default=datetime.date.today(), nullable=False)
    date_last_touched = sqlalchemy.Column("datetime_touched", sqlalchemy.DateTime)
    text = sqlalchemy.Column("example", sqlalchemy.Text, nullable=False)
    score_type = assoc.LanguageBExampleScore


# LanguageAExample: Sentences featuring language A.  Intended for idioms
# Contains the following relationships
#     * many-to-many: LanguageBExample
class LanguageAExample(Base):
    __tablename__ = "lang_a_examples"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    translations = sqlalchemy.orm.relation("LanguageBExample", secondary=assoc.LAE_LBE,
                                           back_populates="translations")
    date_created = sqlalchemy.Column("date_created", sqlalchemy.Date, default=datetime.date.today(), nullable=False)
    date_last_touched = sqlalchemy.Column("datetime_touched", sqlalchemy.DateTime)
    text = sqlalchemy.Column("example", sqlalchemy.Text, nullable=False)
    words = sqlalchemy.orm.relation("LanguageAVocab", secondary=assoc.LAV_LAE,
                                    back_populates="examples")


# Language A vocab deck.  In our case, LanguageA is English
class LanguageAVocab(Base):
    __tablename__ = "lang_a_vocab"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    text = sqlalchemy.Column("word", sqlalchemy.String, nullable=False)
    g_type = sqlalchemy.Column("type", sqlalchemy.String)
    date_created = sqlalchemy.Column("date_created", sqlalchemy.Date, default=datetime.date.today(), nullable=False)
    date_last_touched = sqlalchemy.Column("date_touched", sqlalchemy.Date)
    translations = sqlalchemy.orm.relation("LanguageBVocab", secondary=assoc.LAV_LBV,
                                           back_populates="translations")
    examples = sqlalchemy.orm.relation("LanguageAExample", secondary=assoc.LAV_LAE,
                                       back_populates="words")
    scores = sqlalchemy.orm.relation(assoc.LanguageAVocabScore, cascade="all, delete")
    score_type = assoc.LanguageAVocabScore
    example_type = LanguageAExample


# LanguageB_Vocab cards.  In our case, LanguageA is German
# There the following relationships between with LanguageB_Vocab:
#     * many-to-many: LanguageA_Vocab
#     * many-to-many: LanguageB_Examples
#     * many-to-many association: User (record of scores)
#     * one-to-many: grammar
class LanguageBVocab(Base):
    __tablename__ = "lang_b_vocab"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    translations = sqlalchemy.orm.relation("LanguageAVocab", secondary=assoc.LAV_LBV,
                                           back_populates="translations")
    examples = sqlalchemy.orm.relation("LanguageBExample", secondary=assoc.LBV_LBE,
                                       back_populates="words")
    g_type = sqlalchemy.Column("type", sqlalchemy.Text)
    scores = sqlalchemy.orm.relation(assoc.LanguageBVocabScore, cascade="all")
    grammar = sqlalchemy.orm.relation("Grammar", cascade="all")
    date_created = sqlalchemy.Column("date_created", sqlalchemy.Date, default=datetime.date.today(), nullable=False)
    date_last_touched = sqlalchemy.Column("datetime_touched", sqlalchemy.DateTime)
    text = sqlalchemy.Column("word", sqlalchemy.Text, nullable=False)
    score_type = assoc.LanguageBVocabScore
    example_type = LanguageBExample


# Grammar object:  Specifies grammatical details of a given word.
# Contains the following relationships
#     * many-to-one: LanguageBVocab
class Grammar(Base):
    __tablename__ = "grammar"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    word = sqlalchemy.Column("word_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_b_vocab.id"))
    paradigm = sqlalchemy.Column("paradigm", sqlalchemy.Text)
    irregular = sqlalchemy.Column("irregular", sqlalchemy.Boolean)


# User
class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    vocab_a_scores = sqlalchemy.orm.relation(assoc.LanguageAVocabScore, cascade="all")
    decks = sqlalchemy.orm.relation("Deck", back_populates="user", cascade="all")
    name = sqlalchemy.Column("user_name", sqlalchemy.Text)

# lookup dictionary mapping card type to correct translation type
translation_types = {LanguageAVocab: LanguageBVocab,
                    LanguageBVocab: LanguageAVocab,
                    LanguageAExample: LanguageBExample,
                    LanguageBExample: LanguageAExample}
