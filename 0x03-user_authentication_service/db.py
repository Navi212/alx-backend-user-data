"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Dict
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar("User"):
        """Adds a user to the db using the email and hashed_password params"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict) -> TypeVar("User"):
        """Finds first user in the db by **kwargs"""
        if not kwargs:
            raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound

    def update_user(self, user_id: str, **kwargs: Dict) -> None:
        """Updates a user by user id"""
        if not kwargs:
            raise InvalidRequestError
        try:
            user = self.find_user_by(id=user_id)
            for key, val in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, val)
                else:
                    raise ValueError
        except NoResultFound:
            pass
