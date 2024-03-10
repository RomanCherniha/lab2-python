from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# стрінг для створення зв'язку з бд, вкзаує на тип sql, бібліотеку яка використовується для роботи з цим sql, логін і пароль для бд, хост і порт та назва бд(схеми)
database = 'mysql+pymysql://root:admin@localhost:3306/dbpython' 

engine = create_engine(database)# sqlalchemy двигун для бд

session_local = sessionmaker(autocommit = False, autoflush=False, bind=engine) # створення сесії, не дає стерти дані автоматично, під'єднює двигун
base = declarative_base()#фактична допомога орм для того щоб орм мала базовий функціонал