from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, order_detail):
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id,
    )

    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()

def update(db: Session, order_id, order_detail):
    # Query the database for the specific order to update
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id)
    # Extract the update data from the provided 'order' object
    update_data = order_detail.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_order_detail.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_order_detail.first()

def delete(db: Session, order_id):
    # Query the database for the specific order to delete
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id)
    # Delete the database record without synchronizing the session
    db_order_detail.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
