import sqlalchemy

if __name__ == "__main__":
    import LanguageDeck.models as models

    engine = sqlalchemy.create_engine(params[db_conn])
    engine = sqlalchemy.create_engine('postgresql+psycopg2://samuel:1812@localhost/languagedeck', echo=True)

    #models.Base.metadata.create_all(engine)

    #engine = sqlalchemy.create_engine('sqlite://')
    #models.Base.metadata.create_all(engine)
    #self.engine = create_test_db()
    #self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)
    #self.sess = self.session()


