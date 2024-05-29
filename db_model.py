from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, insert, delete, select
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from sqlalchemy import create_engine

class Base(DeclarativeBase):
     pass


class User(Base):
     __tablename__ = "users"

     id: Mapped[int] = mapped_column(primary_key=True)
     username: Mapped[str] = mapped_column(String(50))
     game: Mapped["Game"] = relationship(back_populates="user")

     def __repr__(self) -> str:
         return f"User(id={self.id!r}, username={self.username!r})"

class GameStatus(Base):
     __tablename__ = "game_statuses"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))

     games: Mapped[List["Game"]] = relationship(back_populates="status")
     def __repr__(self) -> str:
         return f"GameStatus(id={self.id!r}, name={self.name!r})"
class WordTheme(Base):
     __tablename__ = "themes"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))
     # word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
     # game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))

     words: Mapped[List["Word"]] = relationship(back_populates="theme")
     games: Mapped[List["Game"]] = relationship(back_populates="theme")
     def __repr__(self) -> str:
         return f"WordTheme(id={self.id!r}, name={self.name!r})"
class Word(Base):
     __tablename__ = "words"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))
     theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"), nullable=True)

     theme: Mapped["WordTheme"] = relationship(back_populates="words")
     def __repr__(self) -> str:
         return f"Word(id={self.id!r}, name={self.name!r})"
class Game(Base):
     __tablename__ = "games"

     id: Mapped[int] = mapped_column(primary_key=True)
     telegram_game_id: Mapped[int] = mapped_column(Integer(), nullable=False)
     themes_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
     status_id: Mapped[int] = mapped_column(ForeignKey("game_statuses.id"))
     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

     theme: Mapped["WordTheme"] = relationship(back_populates="games")
     status: Mapped["GameStatus"] = relationship(back_populates="games")
     user: Mapped["User"] = relationship(back_populates="game")
     def __repr__(self) -> str:
         return f"Word(id={self.id!r}, telegram_game_id={self.telegram_game_id!r})"

engine = create_engine("sqlite:///test.db", echo=True)

Base.metadata.create_all(engine)
# Session factory, bound to the engine
Session = sessionmaker(bind=engine)

# Create a new session
session = Session()

# session.execute(
#     insert(GameStatus),
#     [
#         {"name": "подготовка"},
#         {"name": "идет игра"},
#         {"name": "ПОБЕДА"},
#         {"name": "проиграли"}
#     ],
# )
#
# session.execute(
#     insert(WordTheme),
#     [
#         {"name": "ХИМИЧЕСКИЙ ЭЛЕМЕНТ"},
#         {"name": "ТКАНЬ"},
#         {"name": "СОРТ СЫРА"}
#     ],
# )
#
# session.execute(
#     insert(Word),
#     [
#         {"name": "АРГОН", "theme_id": 1},
#         {"name": "АСТАТ", "theme_id": 1},
#         {"name": "БАРИЙ", "theme_id": 1},
#         {"name": "БОРИЙ", "theme_id": 1},
#         {"name": "ГЕЛИЙ", "theme_id": 1},
#         {"name": "ИНДИЙ", "theme_id": 1},
#         {"name": "АКРИЛ", "theme_id": 2},
#         {"name": "АТЛАС", "theme_id": 2},
#         {"name": "БАЙКА", "theme_id": 2},
#         {"name": "БАРЕЖ", "theme_id": 2},
#         {"name": "БУРЕТ", "theme_id": 2},
#         {"name": "ВЕЛЮР", "theme_id": 2},
#         {"name": "АНАРИ", "theme_id": 3},
#         {"name": "БАНОН", "theme_id": 3},
#         {"name": "БОФОР", "theme_id": 3},
#         {"name": "ВИОЛА", "theme_id": 3},
#         {"name": "ГАУДА", "theme_id": 3},
#         {"name": "ДАНБО", "theme_id": 3}
#     ],
# )
#
# user = User(username='people')
# session.add(user)
#
# game = Game(telegram_game_id=123, themes_id=1, status_id=2, user_id=1)
# session.add(game)

#
# SELECT *
# FROM themes t
# full JOIN  words w
# on w.theme_id = t.i


# stmt = select(WordTheme, Word).join(Word).where(WordTheme.name == "ТКАНЬ")
#
# query = stmt.compile()
# print(query)
# result = session.execute(stmt).all()
#
# results = [res for res in result]
#
#
# print(print(results))
# Добавление одного обьекта
# theme = WordTheme(name='подготовка')
# session.add(game_status)
# word = Word(name='подготовка')
# word.theme = theme

# game_status = GameStatus(name='подготовка')
# session.add(game_status)

# Добавление нескольких обьектов
# session.execute(
#     insert(GameStatus),
#     [
#         {"name": "идет игра"},
#         {"name": "ПОБЕДА"},
#         {"name": "проиграли"}
#     ],
# )

# Удаление обьекта
# stmt = delete(GameStatus).where(GameStatus.name == "подготовка")
# query = stmt.compile()
# print(query)
# session.execute(stmt)

# Замена обьекта
# stmt = (update(GameStatus).
#         where(GameStatus.id == 2).
#         values(name="игра в процессе"))
# session.execute(stmt)

session.commit()


# one to many
# class Parent(Base):
#     __tablename__ = "parent_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List["Child"]] = relationship(back_populates="parent")
#
#
# class Child(Base):
#     __tablename__ = "child_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
#     parent: Mapped["Parent"] = relationship(back_populates="children")

# many to one
# class Parent(Base):
#     __tablename__ = "parent_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     child_id: Mapped[int] = mapped_column(ForeignKey("child_table.id"))
#     child: Mapped["Child"] = relationship(back_populates="parents")
#
#
# class Child(Base):
#     __tablename__ = "child_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parents: Mapped[List["Parent"]] = relationship(back_populates="child")

# one to one
# class Parent(Base):
#     __tablename__ = "parent_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     child: Mapped["Child"] = relationship(back_populates="parent")
#
#
# class Child(Base):
#     __tablename__ = "child_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
#     parent: Mapped["Parent"] = relationship(back_populates="child")



#we'll add classes here

#creates a create_engine instance at the bottom of the file

