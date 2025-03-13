from market import database, bcrypt, login_manager

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(length=30), nullable=False, unique=True)
    email_address = database.Column(database.String(length=50), nullable=False, unique=True)
    password_hash = database.Column(database.String(length=60), nullable=False)
    budget = database.Column(database.Integer, nullable=False, default=1000)
    items = database.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(30), nullable=False, unique=True)
    price = database.Column(database.Float, nullable=False)
    barcode = database.Column(database.String(12), nullable=False, unique=True)
    description = database.Column(database.String(1024), nullable=False, unique=True)
    owner = database.Column(database.Integer, database.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        database.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        database.session.commit()