from typing import NoReturn
from cryptography.fernet import Fernet
from app.settings import settings
from app.logger import logger
from app.db.connection import async_session
from app.db.models import ServicePassword
from app.db.schemas import PasswordResponse
import functools

cipher = Fernet(settings.SECRET_KEY.encode())


async def encrypt_password(password: str) -> str:
    logger.info("Encrypting password")
    return cipher.encrypt(password.encode()).decode()


async def decrypt_password(encrypted_password: str) -> str:
    logger.info("Decrypting password")
    return cipher.decrypt(encrypted_password.encode()).decode()


async def create_or_update_password(service_name: str, password_data: Password) -> dict | NoReturn:
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
            new_service = await session.merge(serivice)
            await session.commit()
            await session.refresh(new_service)
            return new_service
    except Exception as e:
        raise e


async def get_password(service_name: str) -> str | NoReturn:
    try:
        async with async_session() as session:
            db_password = (
                await session.query(ServicePassword).filter(ServicePassword.service_name == service_name).first()
            )
            if db_password:
                logger.info(f"Retrieving password for service {service_name} ")
                return decrypt_password(db_password.encrypted_password)
            logger.info(f"Password not found for service {service_name}")
            return None
    except Exception as e:
        logger.error(f"Error getting in function get_password: {e}")
        raise e


async def search_passwords(query: str) -> PasswordResponse | NoReturn:
    try:
        async with async_session() as session:
            results = (
                await session.query(ServicePassword).filter(ServicePassword.service_name.ilike(f"%{query}%")).all()
            )
            logger.info(f"Finding passwords for services {query} ,for query {len(results)}")
            return {r.service_name: decrypt_password(r.encrypted_password) for r in results}
    except Exception as e:
        logger.error(f"Error getting in function search_passwords: {e}")
        raise e
