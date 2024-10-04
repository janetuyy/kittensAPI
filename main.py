from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/breeds/", response_model=list[schemas.Breed])
def read_breeds(db: Session = Depends(get_db)):
    breeds = crud.get_breeds(db)
    return breeds


@app.get("/kittens/", response_model=list[schemas.Kitten])
def read_kittens(db: Session = Depends(get_db)):
    kittens = crud.get_kittens(db)
    return kittens


@app.get("/kittens/breed/{breed_name}", response_model=list[schemas.Kitten])
def read_kittens_by_breed(breed_name: str, db: Session = Depends(get_db)):
    kittens = crud.get_kittens_by_breed(db, breed_name=breed_name)
    return kittens


@app.get("/kittens/{kitten_id}", response_model=schemas.Kitten)
def read_kitten(kitten_id: int, db: Session = Depends(get_db)):
    kitten = crud.get_kitten(db, kitten_id=kitten_id)
    if kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return kitten


@app.post("/kittens/", response_model=schemas.Kitten)
def create_kitten(kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_kitten(db=db, kitten=kitten)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/kittens/{kitten_id}", response_model=schemas.Kitten)
def update_kitten(
    kitten_id: int, kitten: schemas.KittenCreate, db: Session = Depends(get_db)
):
    return crud.update_kitten(db=db, kitten_id=kitten_id, kitten=kitten)


@app.delete("/kittens/{kitten_id}", response_model=schemas.KittenDeleteResponse)
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    return crud.delete_kitten(db=db, kitten_id=kitten_id)
