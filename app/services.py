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


async def create_or_update_password(service_name: str, password_data: PasswordCreate) -> str | NoReturn:
    encrypted = encrypt_password(password_data.password)
    try:
        async with async_session() as session:
            db_password = await session.query(ServicePassword).filter(Password.service_name == service_name).first()
            if db_password:
                db_password.encrypted_password = encrypted
                logger.info(f"Updating password for service {service_name}")
            else:
                db_password = Password(service_name=service_name, encrypted_password=encrypted)
                session.add(db_password)
                logger.info(f"Creating password for service {service_name}")
            await session.commit()
            await session.refresh(db_password)
            return db_password
    except Exception as e:
        logger.error(f"Error getting in function create_or_update_password: {e}")
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
