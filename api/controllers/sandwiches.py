from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price,
    )

    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


def read_all(db: Session):
    return db.query(models.Sandwich).all()


def read_one(db: Session, sandwich_name):
    return db.query(models.Sandwich).filter(models.Sandwich.sandwich_name == sandwich_name).first()

def update(db: Session, sandwich_name, sandwich):
    # Query the database for the specific order to update
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.sandwich_name == sandwich_name)
    # Extract the update data from the provided 'order' object
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_sandwich.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_sandwich.first()

def delete(db: Session, sandwich_name):
    # Query the database for the specific order to delete
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.sandwich_name == sandwich_name)
    # Delete the database record without synchronizing the session
    db_sandwich.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
