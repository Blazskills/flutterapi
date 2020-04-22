from flask import Flask, request, jsonify,redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
import uuid


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqliteflutter')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] = 'JIHDGJIDHFHJDFJ'

#Init db

db = SQLAlchemy(app)

#init ma

ma = Marshmallow(app)


#product

class Bible (db.Model):
    id = db.Column (db.Integer, primary_key =True)
    month_name = db.Column(db.String(100))
    month_uid = db.Column(db.Integer)
    month_id = db.Column(db.Integer)
    morning = db.Column(db.String(100))
    afternoon = db.Column(db.String(100))
    night = db.Column(db.String(100))
    today=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self,  morning, afternoon,night):

        self.morning = morning
        self.afternoon = afternoon
        self.night = night

class months (db.Model):
    id = db.Column (db.Integer, primary_key =True)
    month = db.Column(db.String(100), unique=True)
    today=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, month):
        self.month = month
       

    # !product schema
class BibleSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'today' ,'month_name', 'month_uid', 'month_id', 'morning','afternoon','night')
        


# !Init schema
# product_schema = BibleSchema(strict=True)
# products_schema = BibleSchema( many =True)




# !Get all products
@app.route('/apibible', methods=['GET'])
def apibible():
    jsonbible = Bible.query.all()
    allJanuary = Bible.query.filter_by(month_name='January').all()
    allFebruary = Bible.query.filter_by(month_name='February').all()
    allMarch = Bible.query.filter_by(month_name='March').all()
    allApril = Bible.query.filter_by(month_name='April').all()
    allMay = Bible.query.filter_by(month_name='May').all()
    allJune = Bible.query.filter_by(month_name='June').all()
    allJuly = Bible.query.filter_by(month_name='July').all()
    allAugust = Bible.query.filter_by(month_name='August').all()
    allSeptember = Bible.query.filter_by(month_name='September ').all()
    allOctober = Bible.query.filter_by(month_name='October').all()
    allNovember = Bible.query.filter_by(month_name='November').all()
    allDecember = Bible.query.filter_by(month_name='December ').all()
    user_schema = BibleSchema(many=True)
    _jsonbible = user_schema.dump(jsonbible)
    _allJanuary = user_schema.dump(allJanuary)
    _allFebruary = user_schema.dump(allFebruary)
    _allMarch = user_schema.dump(allMarch)
    _allApril = user_schema.dump(allApril)
    _allmay = user_schema.dump(allMay)
    _allJune = user_schema.dump(allJune)
    _allJuly = user_schema.dump(allJuly)
    _allAugust = user_schema.dump(allAugust)
    _allSeptember = user_schema.dump(allSeptember)
    _allOctober = user_schema.dump(allOctober)
    _allNovember = user_schema.dump(allNovember)
    _allDecember = user_schema.dump(allDecember)
    return jsonify({'Bible': _jsonbible}, {'AllJanuary': _allJanuary}, {'AllFebruary': _allFebruary}, {'AllMarch': _allMarch}, {'AllApril': _allApril}, {'Allmay': _allmay}, {'AllJune': _allJune}, {'AllJuly': _allJuly}, {'AllAugust': _allAugust}, {'AllSeptember': _allSeptember}, {'AllOctober': _allOctober}, {'AllNovember': _allNovember}, {'AllDecember': _allDecember})







@app.route('/month',  methods=['GET','POST'])
def month():
    if request.method =='POST':
        month = request.form['month']
        if month == '':
            return render_template('index.html', message='please enter reduired feilds')
        if db.session.query(months).filter(months.month == month).count()== 0:
            new_month = months(month)
            db.session.add(new_month)
            db.session.commit()
            return render_template('index.html',  message= month + ' ' + ' ' "Added Successfully")
        return render_template('index.html',  message= month + ' ' + ' ' "Already Added")
    return render_template('index.html')


# @app.route('/bible',  methods=['GET','POST'])
# def bible():
#     if request.method =='POST':
#         biblemonth = request.form['biblemonth']
#         biblepg = months.query.filter_by(month=biblemonth).first()
#         if biblepg:
#             print(biblepg.id)
#             return "seen"
#         else:
#             return 'invaild'
#     return render_template('biblepg.html')




@app.route('/bible',  methods=['GET','POST'])
def bible():
    if request.method =='POST':
        biblemonth = request.form['biblemonth']
        morning = request.form['morning']
        afternoon = request.form['afternoon']
        night = request.form['night']
        biblepg = months.query.filter_by(month=biblemonth).first()
        if biblepg:
            new_bible = Bible(morning,afternoon,night)
            db.session.add(new_bible)
            new_bible.month_name = biblepg.month
            new_bible.month_id = biblepg.id
            new_bible.month_uid = str(uuid.uuid4())[:8]
            db.session.commit()
            return render_template('biblepg.html', message='Created Successfully')   
        else:
            return render_template('biblepg.html', message='Wrong Month Input')
    return render_template('biblepg.html')




    # !product schema
# class ProductSchema(ma.ModelSchema):
#     class Meta:
#         fields = ('id', 'name', 'description', 'price', 'qty')


#Init schema
# product_schema = ProductSchema(strict=True)
#  !products_schema = ProductSchema( many =True)
    


# !create product
# @app.route('/product',methods=['POST'])
# def add_product():
#     user_schema =ProductSchema(many=True)
#     name =request.json['name']
#     description =request.json['description']
#     price =request.json['price']
#     qty =request.json['qty']
#     new_product = product(name, description,price,qty)
#     db.session.add(new_product)
#     db.session.commit()
#     return user_schema.jsonify({new_product})
    #! result = {
    #!     'name' : new_product.name,
    #!     'description' : new_product.description,
    #!     'price' : new_product.price,
    #!     'qty' : new_product.qty
    #! }
    #! return jsonify({'state': result})
    
    
# !Get all products
# @app.route('/products', methods=['GET'])
# def products():
#     jsonposts = product.query.all()
#     user_schema = ProductSchema(many=True)
#     _jsonposts = user_schema.dump(jsonposts)
#     return jsonify({'products': _jsonposts})


# ! API FOR Product BY ID DATABASE
# @app.route("/productid/<id>/api/v2", methods=['GET'])
# def productid(id):
#     user = product.query.filter_by(id=id)
#     user_schema = ProductSchema(many=True)
#     output = user_schema.dump(user)
#     if (len(output) > 0):
#         return jsonify({'user': output}), 200
#     return jsonify({'Message': "Id not Found"}), 400

# !update product in database
# @app.route('/productupdate/<id>', methods=['PUT'])
# def productupdate(id):
#         user_schema =ProductSchema(many=True)
#         Productss= product.query.filter_by(id=id).first()
#         if Productss:
#             name = request.json['name']
#             description = request.json['description']
#             price = request.json['price']
#             qty = request.json['qty']
#             Productss.name=name
#             Productss.description=description
#             Productss.price=price
#             Productss.qty=qty
#             db.session.commit()
#             return user_schema.jsonify({Productss})
#         return jsonify({'Message' : "Wrong update"})

# !delete user from the database
# @app.route("/productdel/<id>",methods=['DELETE'])
# def userdelete(id):
#     user = product.query.get(id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'Message' : "deleted"})
#     return jsonify({'Message' : "Id does not exist to be deleted"})





if __name__ =='__main__':
    app.run()