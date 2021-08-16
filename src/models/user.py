from src import db, bcrypt, login_manager
from flask_login import UserMixin

#login_manager for flask load user protects routes
@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
       id = db.Column(db.Integer(), primary_key=True)
       username = db.Column(db.String(length=30), nullable=False, unique=True)
       email = db.Column(db.String(length=50), nullable=False, unique=True)
       password_hash = db.Column(db.String(length=60), nullable=False)
       budget = db.Column(db.Integer(), nullable=False, default=1000)
       #not a column not but relationship with Item model
       items = db.relationship('Item', backref='owned_user', lazy=True)

       def __repr__(self):
            return f'User {self.username}'


       @property
       def prettier_budget(self):
            if len(str(self.budget)) >= 4:
                 return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
            else:
                 return f"{self.budget}"


       @property
       #getter property password
       def password(self): #property password returns password Class has propert password # getter
            return self.password

       @password.setter
       #setter for property password
       def password(self, plain_text_password): #password setter turns password to password hash
            self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
     
       def check_password_correction(self, attempted_password):
            return bcrypt.check_password_hash(self.password_hash, attempted_password)

       def can_purchase(self, item):
            return self.budget >= item.price