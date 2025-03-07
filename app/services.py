from typing import NoReturn
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import text
from app.settings import settings
from app.logger import logger
from app.db.connection import async_session
from app.db.models import ServicePassword
from app.db.schemas import Password, ServicePasswordScheme
from sqlmodel import select, insert, update

cipher = Fernet(settings.SECRET_KEY)


def encrypt_password(password: str) -> str:
    logger.info("Encrypting password")
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password: str) -> str:
    try:
        if encrypted_password is None:
            return
        logger.info("Decrypting password")
        decrypted = cipher.decrypt(encrypted_password.encode()).decode()
        return decrypted
    except InvalidToken as e:
        raise e


async def create_or_update_password(service_name: str, password_data: Password) -> ServicePasswordScheme | NoReturn:
    encrypted = encrypt_password(password_data.password)
    try:
        async with async_session() as session:
            q = select(ServicePassword.id).where(ServicePassword.service_name == service_name)
            result = await session.execute(q)
            check_if_exist = result.scalar_one_or_none()
            if check_if_exist:
                serivice = ServicePassword(id=check_if_exist, service_name=service_name, password=encrypted)
            else:
                serivice = ServicePassword(service_name=service_name, password=encrypted)
            new_service: ServicePasswordScheme = await session.merge(serivice)
            await session.commit()
            await session.refresh(new_service)
            return new_service
    except Exception as e:
        raise e


async def get_password(service_name: str) -> Password | None | NoReturn:
    try:
        async with async_session() as session:
            q = select(ServicePassword.password).where(ServicePassword.service_name == service_name)
            result = await session.execute(q)
            decrypted = decrypt_password(result.scalar_one_or_none())
            if decrypted is None:
                return None
            return Password(password=decrypted)

    except Exception as e:
        raise e


async def search_passwords(query: str) -> list[ServicePasswordScheme] | NoReturn:
    try:
        async with async_session() as session:
            q = await session.scalars(select(ServicePassword).where(ServicePassword.service_name.contains(query)))
            return [
                ServicePasswordScheme(service_name=r.service_name, password=decrypt_password(r.password))
                for r in q.all()
            ]

    except Exception as e:
        raise e
