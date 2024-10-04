from pydantic import BaseModel


class BreedBase(BaseModel):
    name: str


class BreedCreate(BreedBase):
    pass


class Breed(BreedBase):
    id: int

    class Config:
        orm_mode = True


class KittenBase(BaseModel):
    name: str
    age: int


class KittenCreate(KittenBase):
    breed_name: str


class KittenDeleteResponse(KittenBase):
    id: int

    class Config:
        orm_mode = True


class Kitten(KittenBase):
    id: int
    breed: Breed

    class Config:
        orm_mode = True
