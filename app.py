from flask import Flask,request,render_template,json,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

# 此处是配置SQLALCHEMY_DATABASE_URI, 前面的mysql+mysqlconnetor指的是数据库的类型以及驱动类型
# 后面的username,pwd,addr,port,dbname分别代表用户名、密码、地址、端口以及库名
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:zhutoukj97@127.0.0.1:3306/danew"

#设置编码
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    # __tablename__= 'Users'
    Phone = db.Column(db.String,nullable=False)
    UserName = db.Column(db.String,primary_key=True,unique=True,nullable=False)
    ID = db.Column(db.String,nullable=False)
    Password = db.Column(db.String,nullable=False)
    Address = db.Column(db.String,nullable=False)
    #,'Expressmen','CustomerService','Finance','Humanresource'
    AuthorityLevel = db.Column(db.Enum("Admin",'Customer'),nullable=False)

    def __init__(self,userid,name,passwd,phone,address,authRank='Customer',):
        self.UserName = name
        self.ID = userid
        self.Password = passwd
        self.Phone = phone
        self.Address = address
        self.AuthorityLevel = authRank

    def __repr__(self):
        return '<User %r>' % self.ID

class UserModelSchema(ma.ModelSchema):
    class Meta:
        # model = Users
        fields = ('UserName','Phone','Address')

user_schema = UserModelSchema()
users_schema = UserModelSchema(many=True)

@app.route('/user/login',methods=['GET','POST'])
def login_user():
    '''judge when user try to login'''
    user_data = request.form
    name = user_data['name']
    passwd = user_data['password']
    print(name,passwd)
    user = Users.query.get(name)
    print(user)
    if user.Password == passwd:
        return jsonify({'status': '200', 'message': '登录成功!'})
    return jsonify({'status': '401','message': '登录失败!'})

@app.route('/user/list')
def list_all_users():
    all_users = db.session.query(Users).all()
    result = users_schema.dumps(all_users)
    return jsonify(result.data)
    # return result.data
    # return json.dumps(result.data)


@app.route('/user/insert',methods=['GET','POST'])
def insert_user():
    '''add a user through POST from android'''
    user_data = request.form
    user = Users(user_data['ID'],user_data['Password'],user_data['AuthorityLevel'],user_data['UserName'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '插入成功！'})

@app.route('/user/delete/<username>')
def delete_user(username):
    '''delete a user '''
    user = db.session.query.get(username)
    # user = db.session.query(Users).filter_by(userid=userid).all()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '删除成功！'})


@app.route(r'/user/query/<username>')
def query_user(username):
    '''query a user'''
    user = Users.query.get(username)
    if user:
        result = user_schema.dumps(user)
        return jsonify(result.data)
    else:
        return jsonify({'status': '401','message': '查询失败!'})


@app.route('/user/update',methods=['GET','POST'])
def update_user():
    '''update info of user'''
    user_data = request.form
    name,passwd,phone,address = user_data['UserName'],user_data['Password'],user_data['phone'],user_data['address']
    user = db.session.query().get(name)
    user.UserName,user.Password,user.Phone,user.Address = name,passwd,phone,address
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '修改成功！'})



#测试入口
@app.route('/')
def hello_world():
    return jsonify({'status': '0', 'errmsg': '登录成功！'})


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")




















