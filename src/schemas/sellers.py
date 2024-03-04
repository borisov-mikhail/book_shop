from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from src.schemas.books import ReturnedBook
import re

__all__ = ["IncomingSeller", "ReturnedAllSellers", "ReturnedSeller", "ReturnedSellerWithBooks"]

# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str

    # Валидатор для e_mail 
    @field_validator("e_mail")  
    @staticmethod
    def validate_e_mail(mail: str):
        if not re.match(r"^\S+@\S+\.\S+$", mail):
            raise PydanticCustomError("Validation error", "Invalid e_mail format!")
        return mail
    
    # Валидатор на минимальную длину пароля
    @field_validator("password")  
    @staticmethod
    def validate_pass(password: str):
        if len(password) < 8:
            raise PydanticCustomError("Validation error", "Password is too short!")
        return password


# Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата массива объектов "Продавец"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]

class ReturnedSellerWithBooks(ReturnedSeller):
    books: list[ReturnedBook]