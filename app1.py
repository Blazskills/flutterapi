from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] = 'JIHDGJIDHFHJDFJ'

#Init db

db = SQLAlchemy(app)

#init ma

ma = Marshmallow(app)


#product

class product (db.Model):
    id = db.Column (db.Integer, primary_key =True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)


    def __init__(self, name, description,price, qty ):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

    # !product schema
class ProductSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


#Init schema
# product_schema = ProductSchema(strict=True)
#  !products_schema = ProductSchema( many =True)
    


# !create product
@app.route('/product',methods=['POST'])
def add_product():
    user_schema =ProductSchema(many=True)
    name =request.json['name']
    description =request.json['description']
    price =request.json['price']
    qty =request.json['qty']
    new_product = product(name, description,price,qty)
    db.session.add(new_product)
    db.session.commit()
    return user_schema.jsonify({new_product})
    #! result = {
    #!     'name' : new_product.name,
    #!     'description' : new_product.description,
    #!     'price' : new_product.price,
    #!     'qty' : new_product.qty
    #! }
    #! return jsonify({'state': result})
    
    
# !Get all products
@app.route('/products', methods=['GET'])
def products():
    jsonposts = product.query.all()
    user_schema = ProductSchema(many=True)
    _jsonposts = user_schema.dump(jsonposts)
    return jsonify({'products': _jsonposts})


# ! API FOR Product BY ID DATABASE
@app.route("/productid/<id>/api/v2", methods=['GET'])
def productid(id):
    user = product.query.filter_by(id=id)
    user_schema = ProductSchema(many=True)
    output = user_schema.dump(user)
    if (len(output) > 0):
        return jsonify({'user': output}), 200
    return jsonify({'Message': "Id not Found"}), 400

# !update product in database
@app.route('/productupdate/<id>', methods=['PUT'])
def productupdate(id):
        user_schema =ProductSchema(many=True)
        Productss= product.query.filter_by(id=id).first()
        if Productss:
            name = request.json['name']
            description = request.json['description']
            price = request.json['price']
            qty = request.json['qty']
            Productss.name=name
            Productss.description=description
            Productss.price=price
            Productss.qty=qty
            db.session.commit()
            return user_schema.jsonify({Productss})
        return jsonify({'Message' : "Wrong update"})

# !delete user from the database
@app.route("/productdel/<id>",methods=['DELETE'])
def userdelete(id):
    user = product.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Message' : "deleted"})
    return jsonify({'Message' : "Id does not exist to be deleted"})



@app.route('/',methods=['GET'])
def hello_world():
    return  jsonify({'msg':'Hello, World!'})

if __name__ =='__main__':
    app.run(debug=True, port=4000)