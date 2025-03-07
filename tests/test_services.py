from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from cryptography.fernet import InvalidToken
from sqlalchemy.exc import NoResultFound

from app.services import create_or_update_password, decrypt_password, encrypt_password, get_password, search_passwords


@pytest.fixture
def mock_cipher():
    with patch("app.services.cipher") as mock_cipher:
        yield mock_cipher


@pytest.fixture
async def mock_async_session():
    with patch("app.services.async_session") as mock_async_session:
        mock_session_instance = mock_async_session.return_value
        mock_session_instance.__aenter__.return_value = mock_session_instance
        yield mock_async_session


@pytest.fixture
def mock_logger():
    with patch("app.services.logger") as mock_logger:
        yield mock_logger


def test_decrypt_valid_password(mock_cipher, mock_logger):
    encrypted_password = "valid_encrypted_password"
    mock_cipher.decrypt.return_value.decode.return_value = "decrypted_password"
    decrypted_password = decrypt_password(encrypted_password)
    assert decrypted_password == "decrypted_password"
    mock_logger.info.assert_called_once_with("Decrypting password")


def test_decrypt_invalid_password(mock_cipher):
    encrypted_password = "invalid_encrypted_password"
    mock_cipher.decrypt.side_effect = InvalidToken
    with pytest.raises(InvalidToken):
        decrypt_password(encrypted_password)


def test_decrypt_none(mock_cipher):
    encrypted_password = None
    decrypted_password = decrypt_password(encrypted_password)
    assert decrypted_password is None


def test_encrypt_password(mock_cipher, mock_logger):
    password = "password"
    mock_cipher.encrypt.return_value.decode.return_value = "encrypted_password"
    encrypted_password = encrypt_password(password)
    assert encrypted_password == "encrypted_password"
    mock_logger.info.assert_called_once_with("Encrypting password")


@pytest_asyncio.fixture(scope="session")
async def test_get_password(mock_async_session, mock_cipher):
    service_name = "service_name"
    mock_async_session.return_value.execute.return_value.scalar_one_or_none.return_value = "encrypted_password"
    mock_cipher.decrypt.return_value.decode.return_value = "decrypted_password"
    password = await get_password(mock_async_session, service_name)
    assert password == "decrypted_password"


@pytest_asyncio.fixture(scope="session")
async def test_get_password_none(mock_async_session, mock_cipher):
    service_name = "service_name"
    mock_async_session.return_value.execute.return_value.scalar_one_or_none.return_value = None
    password = await get_password(mock_async_session, service_name)
    assert password is None


@pytest_asyncio.fixture(scope="session")
async def test_search_passwords(mock_async_session, mock_cipher):
    query = "query"
    mock_async_session.return_value.scalars.return_value.all.return_value = [
        MagicMock(service_name="service_name", password="encrypted_password")
    ]
    mock_cipher.decrypt.return_value.decode.return_value = "decrypted_password"
    passwords = await search_passwords(mock_async_session, query)
    assert len(passwords) == 1
    assert passwords[0].service_name == "service_name"
    assert passwords[0].password == "decrypted_password"


@pytest_asyncio.fixture(scope="session")
async def test_create_or_update_password(mock_async_session, mock_cipher):
    service_name = "service_name"
    password_data = AsyncMock(password="password")
    mock_cipher.encrypt.return_value.decode.return_value = "encrypted_password"
    mock_async_session.return_value.execute.return_value.scalar_one_or_none.return_value = None
    password = await create_or_update_password(mock_async_session, service_name, password_data)
    assert password.service_name == service_name
    assert password.password == "encrypted_password"
