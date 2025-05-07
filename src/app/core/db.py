from sqlmodel import Session, create_engine

from app.core.settings import settings


from app.models import Device, SensorValues

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(_session: Session) -> None:
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
    pass
