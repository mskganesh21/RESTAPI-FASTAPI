from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models import NoteDB
from app.models import NoteCreate, NoteUpdate


async def list_notes(db: AsyncSession) -> list[NoteDB]:
    result = await db.execute(
        select(NoteDB).order_by(NoteDB.created_at.desc()),
    )
    return list(result.scalars().all())


async def get_note(db: AsyncSession, note_id: int) -> NoteDB | None:
    return await db.get(NoteDB, note_id)


async def create_note(db: AsyncSession, payload: NoteCreate) -> NoteDB:
    note = NoteDB(title=payload.title, content=payload.content)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def update_note(
    db: AsyncSession,
    note_id: int,
    payload: NoteUpdate,
) -> NoteDB | None:
    note = await db.get(NoteDB, note_id)
    if note is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return note

    for field, value in updates.items():
        setattr(note, field, value)
    note.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note_id: int) -> bool:
    note = await db.get(NoteDB, note_id)
    if note is None:
        return False

    await db.delete(note)
    await db.commit()
    return True
