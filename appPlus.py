from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/danew"
app.config['JSON_AS_ASCII'] = False #设置编码
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    _tablename= 'Users'
    UserName = db.Column(db.String,primary_key=True,nullable=False)
    Password = db.Column(db.String,nullable=False)
    Email = db.Column(db.String,nullable=False)
    Address = db.Column(db.String,nullable=False)
    AuthorityLevel = db.Column(db.Enum("Admin",'Customer','Expressmen',
                                       'CustomerService','Finance','Humanresource'),unique=False)

    def __init__(self,name,passwd,email,address,authRank,):
        self.UserName = name
        self.Password = passwd
        self.Email = email
        self.Address = address
        self.AuthorityLevel = authRank

    def __repr__(self):
        return '<User %r>' % self.UserName

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
    #     return dict
    #
    # def jsondata(self):
    #     data = {
    #         'ID' : self.ID,
    #         'Password' : self.Password,
    #         'AuthorityLevel' : self.AuthorityLevel,
    #         'UserName' : self.UserName,
    #     }
    #     return jsonify(data)

class UserModelSchema(ma.ModelSchema):
    class Meta:
        model = Users

@app.route('/user/list')
def list_all_users():
    users_schema = UserModelSchema(many=True)
    all_users = db.session.query(Users).all()
    result = users_schema.dumps(all_users,ensure_ascii=False)
    return result.data

@app.route('/user/insert',methods=['GET','POST'])
def insert_user():
    '''add a user through POST from android'''
    userDic = request.form
    user = Users(userDic['UserName'],userDic['Password'],userDic['Email'],
                 userDic['Address'],userDic['AuthorityLevel'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '插入成功！'})

@app.route('/user/delete/<username>')
def delete_user(username):
    '''delete a user '''
    user = db.session.query(Users).filter_by(UserName=username).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '删除成功！'})

@app.route('/user/update',methods=['GET','POST'])
def update_user():
    '''update info of user'''
    userDic = request.form
    name,passwd,email,address, = userDic['UserName'],userDic['Password'],userDic['Email'],userDic['Address']
    user = db.session.query(Users).filter_by(UserName=name).first()
    user.UserName,user.Password,user.Email,user.Address = name,passwd,email,address
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '修改成功！'})

# def search_user(id):
#     '''search user from database'''
#     with app.app_context():
#         user = db.session.query(Users).filter_by(ID=id).first()
#         return user
    # with app.app_context():
    #     return jsonify(user.to_json())
# @app.route('/user/login',methods=['GET','POST'])
# def login_user():
#     '''judge when user try to login'''



#测试入口
@app.route('/')
def hello_world():
    return jsonify({'status': '0', 'errmsg': '登录成功！'})

if __name__ == '__main__':
    app.run(debug=True)




















