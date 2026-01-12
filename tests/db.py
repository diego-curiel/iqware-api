from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_engine = create_engine("sqlite:///:memory:")
SessionTesting = sessionmaker(bind=test_engine)
