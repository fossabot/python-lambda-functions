from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func, Float, Boolean, Text
from sqlalchemy.orm import relationship
from .model_base import Base


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String(36), primary_key=True)
    is_peer_review = Column(Boolean)
    belongs_to_good_pair = Column(Boolean)
    user_id = Column(String(36), ForeignKey('users.id'))
    item_id = Column(String(36), ForeignKey('items.id',
                                            ondelete='CASCADE', onupdate='CASCADE'))
    start_timestamp = Column(DateTime)
    finish_timestamp = Column(DateTime)
    status = Column(String(100))

    review_answers = relationship(
        "ReviewAnswer", back_populates="review")
    item = relationship("Item", back_populates="reviews")

    def to_dict(self):
        return {"id": self.id, "is_peer_review": self.is_peer_review,
                "belongs_to_good_pair": self.belongs_to_good_pair, "user_id": self.user_id,
                "start_timestamp": str(self.start_timestamp), "finish_timestamp": str(self.finish_timestamp)}
