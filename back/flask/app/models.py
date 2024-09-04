from . import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    uid = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50))
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(50))

class Cave(db.Model):
    __tablename__ = 'caves'
    id = db.Column(db.Integer, primary_key=True)
    proprietaire_uid = db.Column(db.Integer, db.ForeignKey('utilisateurs.uid'), nullable=False)
    nom = db.Column(db.String(50), nullable=False, unique=True)

class Bouteille(db.Model):
    __tablename__ = 'bouteilles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    cepage = db.Column(db.String(50), nullable=False)
    millesime = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    cave_id = db.Column(db.Integer, db.ForeignKey('caves.id'), nullable=False)

class Ami(db.Model):
    __tablename__ = 'amis'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.uid'), nullable=False)
    ami_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.uid'), nullable=False)