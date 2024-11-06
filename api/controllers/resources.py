from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, resource):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount,
    )

    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, item):
    return db.query(models.Resource).filter(models.Resource.item == item).first()

def update(db: Session, item, resource):
    # Query the database for the specific order to update
    db_resource = db.query(models.Resource).filter(models.Resource.item == item)
    # Extract the update data from the provided 'order' object
    update_data = resource.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resource.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_resource.first()

def delete(db: Session, item):
    # Query the database for the specific order to delete
    db_resource = db.query(models.Resource).filter(models.Resource.item == item)
    # Delete the database record without synchronizing the session
    db_resource.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
