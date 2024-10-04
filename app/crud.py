from sqlalchemy.orm import Session
from . import models, schemas


def get_breeds(db: Session):
    # Получение списка всех пород
    return db.query(models.Breed).all()


def get_kittens(db: Session):
    # Получение списка всех котят
    return db.query(models.Kitten).all()


def get_kittens_by_breed(db: Session, breed_name: str):
    # Найти породу по breed_name
    breed = db.query(models.Breed).filter(models.Breed.name == breed_name).first()
    if breed:
        # Найти котят по breed_id
        return db.query(models.Kitten).filter(models.Kitten.breed_id == breed.id).all()
    return []


def get_kitten(db: Session, kitten_id: int):
    # Найти котенка по kitten_id
    return db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()


def create_or_get_breed(db: Session, breed_name: str):
    # Попытка найти существующую запись по имени породы
    breed = db.query(models.Breed).filter(models.Breed.name == breed_name).first()

    if breed is None:
        # Если порода не найдена, создать новую запись в таблице breeds
        breed = models.Breed(name=breed_name)
        db.add(breed)
        db.commit()
        db.refresh(breed)
    return breed


def create_kitten(db: Session, kitten: schemas.KittenCreate):
    # Найти или создать породу по breed_name
    breed = create_or_get_breed(db, kitten.breed_name)

    # Создать новую запись котенка
    db_kitten = models.Kitten(name=kitten.name, age=kitten.age, color=kitten.color, description=kitten.description, breed_id=breed.id)
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)

    return db_kitten


def update_kitten(db: Session, kitten_id: int, kitten: schemas.KittenCreate):
    # Найти котенка по kitten_id
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()

    # Найти или создать породу по breed_name
    breed = create_or_get_breed(db, kitten.breed_name)

    # Обновить данные котенка
    db_kitten.name = kitten.name
    db_kitten.age = kitten.age
    db_kitten.color = kitten.color
    db_kitten.description = kitten.description
    db_kitten.breed_id = breed.id

    db.commit()
    db.refresh(db_kitten)
    return db_kitten


def delete_kitten(db: Session, kitten_id: int):
    # Найти котенка по kitten_id
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()

    # Удалить данные котенка
    db.delete(db_kitten)
    db.commit()
    return {
        "id": db_kitten.id,
        "name": db_kitten.name,
        "age": db_kitten.age,
        "color": db_kitten.color,
        "description": db_kitten.description
    }
