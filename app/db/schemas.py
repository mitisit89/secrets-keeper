from pydantic import BaseModel, ConfigDict


class Password(BaseModel):
    password: str


class ServicePasswordScheme(Password):
    service_name: str
    model_config = ConfigDict(from_attributes=True)


class ListServicePasswordResponse(BaseModel):
    service_list: list[ServicePasswordScheme]
