from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class ProcReport(db.Model):
    __tablename__ = 'proc_report'
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.String)
    assessmentId = db.Column(db.Integer)
    countZero = db.Column(db.Integer)
    countOne = db.Column(db.Integer)
    countMany = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.userId}>'


class ProcReportSchema(ma.Schema):
    class Meta:
        model = ProcReport

    id = fields.Integer()
    userId = fields.String()
    assessmentId = fields.Integer()
    countZero = fields.Integer()
    countOne = fields.Integer()
    countMany = fields.Integer()
