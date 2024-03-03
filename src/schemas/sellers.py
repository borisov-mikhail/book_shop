from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from src.schemas.books import ReturnedBook


__all__ = ["IncomingSeller", "ReturnedAllSellers", "ReturnedSeller", "ReturnedSellerWithBooks"]

# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str

    @field_validator("password")  # Валидатор, проверяет что пароль подходит по длине
    @staticmethod
    def validate_pass(password: str):
        if len(password) < 10:
            raise PydanticCustomError("Validation error", "Password is too short!")
        return password



# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата массива объектов "Книга"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]

class ReturnedSellerWithBooks(ReturnedSeller):
    books: list[ReturnedBook]