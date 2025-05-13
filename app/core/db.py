from sqlmodel import Session, create_engine
import logging
from app.core.settings import settings
from app.models.customer import Customer
from app.models.address import Address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(_session: Session) -> None:
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)    
    logger.info("Creating models")
