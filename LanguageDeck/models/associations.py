from . import Base
import sqlalchemy


# LanguageBVocabScore: Association between LanguageBVocab and User.  Records Score on the Vocab
# object for a given user
class LanguageBVocabScore(Base):
    __tablename__ = "lang_b_vocab_scores"
    __table_args__ = (
        sqlalchemy. UniqueConstraint("user_id", "card_id", name="uix_VBS"),
    )
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    card_id = sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_b_vocab.id"))
    score = sqlalchemy.Column("score", sqlalchemy.Float)


# LanguageAVocabScore: Association between LanguageBVocab and User.  Records Score on the Vocab
# object for a given user
class LanguageAVocabScore(Base):
    __tablename__ = "lang_a_vocab_scores"
    __table_args__ = (
        sqlalchemy.UniqueConstraint("user_id", "card_id", name="uix_VAS"),
    )
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    card_id = sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_a_vocab.id"))
    score = sqlalchemy.Column("score", sqlalchemy.Float)


# LanguageBExampleScore: Association between LanguageBExamples and User.  Records Score on the Example
# Object for a given user
class LanguageBExampleScore(Base):
    __tablename__ = "lang_b_examples_scores"
    __table_args__ = (
        sqlalchemy.UniqueConstraint("user_id", "card_id", name="uix_EBS"),
    )
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    card_id = sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_b_examples.id"))
    score = sqlalchemy.Column("score", sqlalchemy.Float)


LAV_Deck = sqlalchemy.Table("lav_deck", Base.metadata,
                            sqlalchemy.Column("deck_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("decks.id")),
                            sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_a_vocab.id")))

LBV_Deck = sqlalchemy.Table("lbv_deck", Base.metadata,
                            sqlalchemy.Column("deck_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("decks.id")),
                            sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("lang_b_vocab.id")))

LAE_Deck = sqlalchemy.Table("lae_deck", Base.metadata,
                            sqlalchemy.Column("deck_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("decks.id")),
                            sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.
                                              ForeignKey("lang_a_examples.id")))

LBE_Deck = sqlalchemy.Table("lbe_deck", Base.metadata,
                            sqlalchemy.Column("deck_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("decks.id")),
                            sqlalchemy.Column("card_id", sqlalchemy.Integer, sqlalchemy.
                                              ForeignKey("lang_b_examples.id")))


# LAV_LBV:  association table for many-to-many mapping of LanguageAVocab
# to LanguageBVocab
LAV_LBV = sqlalchemy.Table("lav_lbv", Base.metadata,
                           sqlalchemy.Column("lang_a_vocab_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_a_vocab.id"), primary_key=True),
                           sqlalchemy.Column("lang_b_vocab_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_b_vocab.id"), primary_key=True),
                           sqlalchemy.PrimaryKeyConstraint("lang_a_vocab_id", "lang_b_vocab_id")
                           )


# LBV_LBE: association table for many-to-many mapping of LanguageBVocab to LanguageBExample
LBV_LBE = sqlalchemy.Table("lbv_lbe", Base.metadata,
                           sqlalchemy.Column("lang_b_vocab_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_b_vocab.id"), primary_key=True),
                           sqlalchemy.Column("lang_b_example_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_b_examples.id"), primary_key=True),
                           sqlalchemy.PrimaryKeyConstraint("lang_b_vocab_id", "lang_b_example_id")
                           )

# LAV_LAE: association table for many-to-many mapping of LanguageAVocab to LanguageAExample
LAV_LAE = sqlalchemy.Table("lav_lae", Base.metadata,
                           sqlalchemy.Column("lang_a_vocab_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_a_vocab.id"), primary_key=True),
                           sqlalchemy.Column("lang_a_example_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_a_examples.id"), primary_key=True),
                           sqlalchemy.PrimaryKeyConstraint("lang_a_vocab_id", "lang_a_example_id")
                           )


# LAE_LBE: association table for many-to-manymapping of LanguageAExample to LanguageBExample
LAE_LBE = sqlalchemy.Table("lbe_lbe", Base.metadata,
                           sqlalchemy.Column("lang_a_example_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_a_examples.id"), primary_key=True),
                           sqlalchemy.Column("lang_b_example_id", sqlalchemy.Integer,
                                             sqlalchemy.ForeignKey("lang_b_examples.id"), primary_key=True),
                           sqlalchemy.PrimaryKeyConstraint("lang_a_example_id", "lang_b_example_id")
                           )
