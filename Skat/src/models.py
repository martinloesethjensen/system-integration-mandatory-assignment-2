from flask_marshmallow import Schema
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP, Text, Float
from app import db


class SkatUsers(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String(200), nullable=False,)
    created_at = Column(TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())
    is_active = Column(Boolean, nullable=False, default=True)

    def __init__(self, user_id, created_at, is_active):
        self.user_id = user_id
        self.created_at = created_at
        self.is_active = is_active

    def __repr__(self):
        return '<SkatUsers %s>' % self.user_id


class SkatUsersSchema(Schema):
    class Meta:
        fields = ("id", "user_id", "created_at", "is_active")
        model = SkatUsers


class SkatYears(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    label = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())
    modified_at = Column(TIMESTAMP(timezone=False),
                         nullable=False, default=datetime.now())
    start_date = Column(Text, nullable=False, default=datetime.now())
    end_date = Column(Text, nullable=False, default=datetime.now())
    is_active = Column(Boolean, nullable=False, default=True)

    def __init__(self, label, created_at, modified_at, start_date, end_date, is_active):
        self.label = label
        self.created_at = created_at
        self.modified_at = modified_at
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active

    def __repr__(self):
        return '<SkatYears %s>' % self.label


class SkatYearsSchema(Schema):
    class Meta:
        fields = ("id", "label", "created_at", "modified_at",
                  "start_date", "end_date", "is_active")
        model = SkatYears


class SkatUsersYears(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    skat_user_id = Column(Integer, ForeignKey('skat_users.id'), nullable=False)
    skat_year_id = Column(Integer, ForeignKey('skat_years.id'), nullable=False)
    user_id = Column(String(200), nullable=False,)
    is_paid = Column(Boolean, nullable=False, default=False)
    amount = Column(Float, nullable=False, default=0.0)

    def __init__(self, skat_user_id, skat_year_id, user_id, is_paid, amount):
        self.skat_user_id = skat_user_id
        self.skat_year_id = skat_year_id
        self.user_id = user_id
        self.is_paid = is_paid
        self.amount = amount

    def __repr__(self):
        return '<SkatUsersYears %s>' % self.id


class SkatUsersYearsSchema(Schema):
    class Meta:
        fields = ("id", "skat_user_id", "skat_year_id",
                  "user_id", "is_paid", "amount")
        model = SkatUsersYears


skat_user_schema = SkatUsersSchema()
skat_users_schema = SkatUsersSchema(many=True)

skat_year_schema = SkatYearsSchema()
skat_years_schema = SkatYearsSchema(many=True)

skat_user_year_schema = SkatUsersYearsSchema()
skat_users_years_schema = SkatUsersYearsSchema(many=True)
