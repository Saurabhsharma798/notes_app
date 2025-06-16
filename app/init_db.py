from models import Base
from database import engine


Base.metadata.createall(bind=engine)