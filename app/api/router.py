from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import schemas
from app.db.connection import get_session
from app import services
from app.logger import logger

router = APIRouter()


@router.post("/password/{service_name}", response_model=schemas.ServicePasswordScheme)
async def create_password(
    service_name: str,
    password_data: schemas.Password,
    session: AsyncSession = Depends(get_session),
):
    """
    Create or update a password for a given service.

    This endpoint allows the user to create a new password entry or update an existing one for a specified service name.

    Args:
        service_name (str): The name of the service for which the password is being created or updated.
        password_data (schemas.Password): An object containing the password details.

    Returns:
        dict: A dictionary containing the service name and the newly created or updated password.

    Raises:
        HTTPException: If an error occurs while creating or updating the password, a 400 status code is returned.
    """
    try:
        password_entry = await services.create_or_update_password(session, service_name, password_data)
        return {
            "service_name": password_entry.service_name,
            "password": password_data.password,
        }
    except Exception as e:
        logger.error(f"Error creating password: {e}")
        raise HTTPException(status_code=400)


@router.get("/password/{service_name}", response_model=schemas.ServicePasswordScheme)
async def get_password(service_name: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a password for a given service.

    This endpoint returns the password for the given service name.

    Args:
        service_name (str): The name of the service for which the password is being retrieved.

    Returns:
        dict: A dictionary containing the service name and the password.

    Raises:
        HTTPException: If an error occurs while retrieving the password, a 400 status code is returned.
        HTTPException: If the service is not found, a 404 status code is returned.
    """
    try:
        password = await services.get_password(session, service_name)
        if password is None:
            logger.info(f"Service {service_name} password not found")
            raise HTTPException(status_code=404, detail="Service not found")
        print(password)
        return {"service_name": service_name, "password": str(password)}
    except Exception as e:
        logger.error(f"Error getting password: {e}")
        raise HTTPException(status_code=400)


@router.get("/password/", response_model=list[schemas.ServicePasswordScheme])
async def search_passwords(service_name: str, session: AsyncSession = Depends(get_session)):
    """
    Search for passwords by service name.

    This endpoint takes a service name and returns a list of matching password entries.

    Args:
        service_name (str): The service name to search for.

    Returns:
        list[schemas.ServicePasswordScheme]: A list of matching password entries.

    Raises:
        HTTPException: If an error occurs while searching, a 400 status code is returned.
        HTTPException: If no matches are found, a 404 status code is returned.
    """
    try:
        results = await services.search_passwords(session, service_name)
        if not results:
            raise HTTPException(status_code=404, detail="No matches found")
        return results
    except Exception as e:
        logger.error(f"Error searching passwords: {e}")
        raise HTTPException(status_code=400)
