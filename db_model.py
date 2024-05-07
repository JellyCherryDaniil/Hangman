from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

class Base(DeclarativeBase):
     pass


class User(Base):
     __tablename__ = "users"

     id: Mapped[int] = mapped_column(primary_key=True)
     username: Mapped[str] = mapped_column(String(50))
     def __repr__(self) -> str:
         return f"User(id={self.id!r}, username={self.username!r})"

class GameStatus(Base):
     __tablename__ = "game_statuses"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))
     def __repr__(self) -> str:
         return f"GameStatus(id={self.id!r}, name={self.name!r})"
class WordTheme(Base):
     __tablename__ = "themes"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))
     word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))

     word: Mapped["Word"] = relationship(back_populates="themes")
     def __repr__(self) -> str:
         return f"WordTheme(id={self.id!r}, name={self.name!r}, word_id={self.word_id!r})"
class Word(Base):
     __tablename__ = "words"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(50))

     themes: Mapped[List["WordTheme"]] = relationship(back_populates="word")
     def __repr__(self) -> str:
         return f"Word(id={self.id!r}, name={self.name!r})"


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





#we'll add classes here

#creates a create_engine instance at the bottom of the file
engine = create_engine("sqlite:///test.db", echo=True)

Base.metadata.create_all(engine)
