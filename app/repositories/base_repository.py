from typing import Generic
from typing import Type
from typing import TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: Session,
        model: Type[ModelType],
    ):

        self.db = db
        self.model = model

    def create(
        self,
        obj: ModelType,
    ) -> ModelType:

        self.db.add(obj)

        self.db.commit()

        self.db.refresh(obj)

        return obj

    def update(
        self,
        obj: ModelType,
    ) -> ModelType:

        self.db.commit()

        self.db.refresh(obj)

        return obj

    def delete(
        self,
        obj: ModelType,
    ) -> None:

        self.db.delete(obj)

        self.db.commit()

    def get_by_id(
        self,
        obj_id: int,
    ) -> ModelType | None:

        return (
            self.db.query(self.model)
            .filter(
                self.model.id == obj_id
            )
            .first()
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:

        return (
            self.db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def refresh(
        self,
        obj: ModelType,
    ) -> ModelType:

        self.db.refresh(obj)

        return obj

    def get_first(
        self,
        **filters,
    ) -> ModelType | None:

        return (
            self.db.query(self.model)
            .filter_by(**filters)
            .first()
        )

    def get_all(
        self,
        **filters,
    ) -> list[ModelType]:

        return (
            self.db.query(self.model)
            .filter_by(**filters)
            .all()
        )

    def get_by(
        self,
        **filters,
    ) -> ModelType | None:

        return (
            self.db.query(self.model)
            .filter_by(**filters)
            .first()
        )

    def list_by(
        self,
        **filters,
    ) -> list[ModelType]:

        return (
            self.db.query(self.model)
            .filter_by(**filters)
            .all()
        )

    def count(self) -> int:
    
        return (
            self.db.query(self.model)
            .count()
        )

    def exists(
        self,
        **filters,
    ) -> bool:
    
        return (
            self.get_by(**filters)
            is not None
        )    