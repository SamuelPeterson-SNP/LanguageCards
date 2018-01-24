import sqlalchemy

if __name__ == "__main__":
    import LanguageDeck.models as models

    # engine = sqlalchemy.create_engine(params[db_conn])
    engine = sqlalchemy.create_engine('postgresql+psycopg2://samuel:1812@localhost/languagedeck', echo=True)

    models.Base.metadata.create_all(engine)


