from sqlalchemy.orm import mapped_column, Mapped, declarative_base
from datetime import date

Base = declarative_base()

class RawComments(Base):

    __tablename__ = 'Raw Youtube Comments'

    id:Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    comment:Mapped[str]
    likes:Mapped[int]
    video_id:Mapped[str]
    date:Mapped[date]