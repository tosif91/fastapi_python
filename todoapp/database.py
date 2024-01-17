from  sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""SQLALCHEMY_DATABASE_URL:
Purpose: This variable holds the connection URL for the database.
Use: It specifies the location and type of the database. In your example, it's set to a SQLite database URL (sqlite:///./sql_app.db). You also have a commented out example for a PostgreSQL database URL. Depending on the project requirements, you can switch between different database engines.
"""
DATABASE_URL= 'sqlite:///./todo.db' #this url is  an location to create a database on our fast api
"""engine:
Purpose: Represents the database engine.
Use: It's created using create_engine from SQLAlchemy, and it takes the SQLALCHEMY_DATABASE_URL as an argument. This engine is responsible for managing database connections and executing SQL statements. The connect_args={"check_same_thread": False} is specific to SQLite and allows multiple threads to access the database."""
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
"""SessionLocal:
Purpose: A factory for creating database sessions.
Use: Created using sessionmaker from SQLAlchemy. Sessions are used to interact with the database. The settings autocommit=False and autoflush=False define the default behavior of the sessions. autocommit=False means that changes won't be committed automatically, allowing you to control when to commit. autoflush=False means that the session won't automatically flush changes to the database."""
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
"""Base:
Purpose: An instance of the declarative_base class from SQLAlchemy.
Use: Used as a base class for your declarative models. Declarative models allow you to define your database tables using Python classes. Any class that inherits from Base can be mapped to a database table. This is a fundamental part of the SQLAlchemy ORM, providing a way to define your data model in a Pythonic way."""
Base = declarative_base()



