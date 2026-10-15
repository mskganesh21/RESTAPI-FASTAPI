from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.models import Note, NoteCreate, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[Note])
async def list_notes(db: AsyncSession = Depends(get_db)) -> list[Note]:
    """GET /notes - list all notes (Express: router.get('/'))."""
    notes = await crud.list_notes(db)
    return [Note.model_validate(note) for note in notes]


@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """GET /notes/:id - fetch a single note."""
    note = await crud.get_note(db, note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    return Note.model_validate(note)


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """POST /notes - create a new note."""
    note = await crud.create_note(db, payload)
    return Note.model_validate(note)


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: AsyncSession = Depends(get_db),
) -> Note:
    """PUT /notes/:id - update an existing note."""
    note = await crud.update_note(db, note_id, payload)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    return Note.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """DELETE /notes/:id - remove a note."""
    deleted = await crud.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
