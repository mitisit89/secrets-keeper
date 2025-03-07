from sqlmodel import Field, SQLModel


class ServicePassword(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_name: str = Field(unique=True)
    password: str = Field(max_length=255)
