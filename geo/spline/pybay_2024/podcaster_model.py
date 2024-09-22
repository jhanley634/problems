from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Podcaster(Base):
    __tablename__ = "podcaster"
    name: Mapped[str] = mapped_column(primary_key=True)
    age: Mapped[int]
