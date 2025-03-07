from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db import schemas
from app import services
from app.logger import logger

router = APIRouter()


@router.post("/password/{service_name}", response_model=schemas.ServicePasswordScheme)
async def create_password(
    service_name: str,
    password_data: schemas.Password,
):
    print(password_data)
    try:
        password_entry = await services.create_or_update_password(service_name, password_data)
        return {
            "service_name": password_entry.service_name,
            "password": password_data.password,
        }
    except Exception as e:
        logger.error(f"Error creating password: {e}")
        raise HTTPException(status_code=400)


@router.get("/password/{service_name}", response_model=schemas.ServicePasswordScheme)
async def get_password(service_name: str):
    try:
        password = await services.get_password(service_name)
        if password is None:
            logger.info(f"Service {service_name} password not found")
            raise HTTPException(status_code=404, detail="Service not found")
        print(password)
        return {"service_name": service_name, "password": str(password)}
    except Exception as e:
        logger.error(f"Error getting password: {e}")
        raise HTTPException(status_code=400)


@router.get("/password/", response_model=list[schemas.ServicePasswordScheme])
async def search_passwords(service_name: str):
    try:
        results = await services.search_passwords(service_name)
        if not results:
            raise HTTPException(status_code=404, detail="No matches found")
        return results
    except Exception as e:
        logger.error(f"Error searching passwords: {e}")
        raise HTTPException(status_code=400)
