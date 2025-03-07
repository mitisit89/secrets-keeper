from sqlmodel import Field, SQLModel


class ServicePassword(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    server_name: str
    secret: str
