from api.db import db


class MessageModel(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140))

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    recipient = db.relationship("UserModel", foreign_keys=[recipient_id])
    sender = db.relationship("UserModel", foreign_keys=[sender_id])

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "message": self.message,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
        }

    @classmethod
    def find_recent_from(cls, recipient_id, sender_id):
        return (
            cls.query.filter_by(sender_id=sender_id, recipient_id=recipient_id)
            .limit(100)
            .all()
        )

    @classmethod
    def find_recent(cls, recipient_id):
        return cls.query.filter_by(recipient_id=recipient_id).limit(100).all()
