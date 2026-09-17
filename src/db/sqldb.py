from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import Optional
from sqlalchemy import create_engine, select

Session = None

class Base(DeclarativeBase):
	pass

class ChatsBase(Base):
	__tablename__ = "chats"
	tg_chat_id: Mapped[int] = mapped_column(primary_key=True)
	tg_thread_id: Mapped[Optional[int]] = mapped_column(primary_key=True)
	max_chat_id: Mapped[int] = mapped_column(primary_key=True)


async def init_db():
    global Session
    engine = create_engine("sqlite:///chatids.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)


async def new_chat(tg_chat_id: int, tg_thread_id: Optional[int], max_chat_id: int):
	if not Session:
		raise
	
	with Session() as session:
		try:
			chatdata = ChatsBase(tg_chat_id=tg_chat_id, tg_thread_id=tg_thread_id, max_chat_id=max_chat_id)
			session.add(chatdata)
		except:
			session.rollback()
			raise

		else:
			session.commit()


async def get_max_chat_id(tg_chat_id: int, tg_thread_id: Optional[int] = None) -> Optional[int]:
	"""
	Получает max_chat_id по tg_chat_id и tg_thread_id.
	"""
	if not Session:
			raise
	with Session() as session:
		
		stmt = select(ChatsBase.max_chat_id).where(
			ChatsBase.tg_chat_id == tg_chat_id,
			ChatsBase.tg_thread_id == tg_thread_id
		)

		return session.execute(stmt).scalar_one_or_none()


async def get_tg_chat_and_thread_ids(max_chat_id: int) -> Optional[tuple[int, Optional[int]]]:
	"""
	Получает кортеж (tg_chat_id, tg_thread_id) по max_chat_id.
	"""
	if not Session:
		raise

	with Session() as session:
		stmt = select(ChatsBase.tg_chat_id, ChatsBase.tg_thread_id).where(
            ChatsBase.max_chat_id == max_chat_id
        )
		result = session.execute(stmt).first()
		if result:
			return (result.tg_chat_id, result.tg_thread_id)
		return None
