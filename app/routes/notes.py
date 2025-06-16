from fastapi import APIRouter,Depends,HTTPException
from schemas import UserCreate,UserLogin,UserOut,NotesCreate,NotesOut,NotesUpdate
from sqlalchemy.orm import Session
from models import NOTE,USER
from database import get_db
from auth import get_current_user

router=APIRouter(
    prefix='/notes',
    tags=["Notes"]
)


@router.post('/',response_model=NotesOut)
def notes(note:NotesCreate , db:Session=Depends(get_db),current_user:USER=Depends(get_current_user)):
    new_note=NOTE(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get('/',response_model=list[NotesOut])
def get_notes(db:Session=Depends(get_db),current_user:USER=Depends(get_current_user)):
    notes=db.query(NOTE).filter(NOTE.owner_id == current_user.id).all()
    return notes


@router.put('/{id}',response_model=NotesOut)
def update_note(id:int,update_note:NotesUpdate,db:Session=Depends(get_db),current_user:USER=Depends(get_current_user)):
    note=db.query(NOTE).filter(NOTE.id == id).first()

    if note is None:
        raise HTTPException(status_code=404,detail="note not found")
    if note.owner_id!=current_user.id:
        raise HTTPException(status_code=403,detail="not authorized to change")
    
    if update_note.title is not None:
        note.title=update_note.title
    if update_note.content is not None:
        note.content=update_note.content

        
    db.commit()
    db.refresh(note)
    return note


@router.delete('/{id}')
def delete_note(id:int,db:Session=Depends(get_db),current_user:USER=Depends(get_current_user)):
    note=db.query(NOTE).filter(NOTE.id==id).first()

    if note is None:
        raise HTTPException(status_code=404,detail='note not found')
    
    if note.owner_id!=current_user.id:
        raise HTTPException(status_code=403,detail="not authorized")
    
    db.delete(note)
    db.commit()
    return {"message":"note deleted successfully"}

