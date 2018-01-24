import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

md = sqlalchemy.MetaData()
Base = declarative_base(metadata=md)

from LanguageDeck.models import associations
from LanguageDeck.models import Cards
from LanguageDeck.models import decks
