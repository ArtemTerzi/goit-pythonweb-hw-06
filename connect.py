from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql+psycopg2://postgres:postgres@localhost:5434/postgres"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
