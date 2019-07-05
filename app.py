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

# class AuthRank(enum.Enum):
#     Admin = "Admin"
#     Customer = 'Customer'
#     Expressmen = 'Expressmen'
#     CustomerService = 'CustomerService'
#     Finance = 'Finance'
#     Humanresource = 'Humanresource'




class Users(db.Model):
    _tablename= 'Users'
    UserName = db.Column(db.String)
    ID = db.Column(db.String,primary_key=True,nullable=False)
    Password = db.Column(db.String,nullable=False)
    AuthorityLevel = db.Column(db.Enum("Admin",'Customer','Expressmen','CustomerService','Finance','Humanresource'),unique=False)

    def __init__(self,userid,passwd,authRank,name):
        self.ID = userid
        self.Password = passwd
        self.AuthorityLevel = authRank
        self.UserName = name

    def __repr__(self):
        return '<User %r>' % self.ID

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def jsondata(self):
        data = {
            'ID' : self.ID,
            'Password' : self.Password,
            'AuthorityLevel' : self.AuthorityLevel,
            'UserName' : self.UserName,
        }
        return jsonify(data)

class UserModelSchema(ma.ModelSchema):
    # type = EnumField(AuthRank,by_value=True)
    class Meta:
        model = Users

def search_user(id):
    '''search user from database'''
    with app.app_context():
        user = db.session.query(Users).filter_by(ID=id).first()
        return user
    # with app.app_context():
    #     return jsonify(user.to_json())


@app.route('/user/login',methods=['GET','POST'])
def login_user():
    '''judge when user try to login'''

@app.route('/user/list')
def list_all_users():
    # users = db.session.query(Users).all()
    # # print(user[0].jsondata())
    # # print(user[0].jsondata())
    # with app.app_context():
    #     List = [user.jsondata() for user in users]
    # # return List

    users_schema = UserModelSchema(many=True)
    all_users = db.session.query(Users).all()
    result = users_schema.dumps(all_users,ensure_ascii=False)
    return result.data


@app.route('/user/insert',methods=['GET','POST'])
def insert_user():
    '''add a user through POST from android'''
    userDic = request.form
    user = Users(userDic['ID'],userDic['Password'],userDic['AuthorityLevel'],userDic['UserName'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '插入成功！'})

@app.route('/user/delete/<userid>')
def delete_user(userid):
    '''delete a user '''
    user = db.session.query(Users).filter_by(ID=userid).first()
    # user = db.session.query(Users).filter_by(userid=userid).all()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '删除成功！'})

@app.route('/user/update',methods=['GET','POST'])
def update_user():
    '''update info of user'''
    userDic = request.form
    id,passwd,authRank,name = userDic['ID'],userDic['Password'],userDic['AuthorityLevel'],userDic['UserName']
    user = db.session.query(Users).filter_by(ID=id).first()
    user.Password,user.AuthorityLevel,user.UserName = passwd,authRank,name
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '修改成功！'})




#测试入口
@app.route('/')
def hello_world():
    return jsonify({'status': '0', 'errmsg': '登录成功！'})


if __name__ == '__main__':
    app.run(debug=True)




















