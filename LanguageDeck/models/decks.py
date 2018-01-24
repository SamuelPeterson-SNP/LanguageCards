import sqlalchemy
import sqlalchemy.orm
from LanguageDeck.models import associations as assoc
from LanguageDeck.models import Base, Cards
import datetime


# Deck object: is a collection of Cards
class Deck(Base):
    __tablename__ = "decks"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column("name", sqlalchemy.Text, nullable=False)
    date_created = sqlalchemy.Column("date_created", sqlalchemy.Date, nullable=False, default=datetime.date.today())
    date_last_touched = sqlalchemy.Column("date_last_touched", sqlalchemy.Date)
    score = sqlalchemy.Column("score", sqlalchemy.Integer)
    user_id = sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relation("User", back_populates="decks")
    vocab_a = sqlalchemy.orm.relation("LanguageAVocab", secondary=assoc.LAV_Deck)
    vocab_b = sqlalchemy.orm.relation("LanguageBVocab", secondary=assoc.LBV_Deck)
    examples_a = sqlalchemy.orm.relation("LanguageAExample", secondary=assoc.LAE_Deck)
    examples_b = sqlalchemy.orm.relation("LanguageBExample", secondary=assoc.LBE_Deck)
