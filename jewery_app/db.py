from sqlmodel import create_engine



eng = r"\Users\POPE's desk\Desktop\jewery_store\database.db"
sqlite_url = f'sqlite:///{eng}'
engine = create_engine(sqlite_url, echo=True)