from flask import Flask,request,render_template,json,jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields

import enum
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = Flask(__name__)

# 此处是配置SQLALCHEMY_DATABASE_URI, 前面的mysql+mysqlconnetor指的是数据库的类型以及驱动类型
# 后面的username,pwd,addr,port,dbname分别代表用户名、密码、地址、端口以及库名
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:zhutoukj97@127.0.0.1:3306/danew"

#设置编码
app.config['JSON_AS_ASCII'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

class

class AuthRank(enum.Enum):
    Admin = "Admin"
    Customer = 'Customer'
    Expressmen = 'Expressmen'
    CustomerService = 'CustomerService'
    Finance = 'Finance'
    Humanresource = 'Humanresource'


class Users(db.Model):
    _table = 'Users'
    userid = db.Column(db.String(20),primary_key=True)
    passwd = db.Column(db.String(20))
    authRank = db.Column(db.Enum(AuthRank),unique=False)

    def __init__(self,userid,passwd,authRank):
        self.userid = userid
        self.passwd = passwd
        self.authRank = authRank

    def __str__(self):
        return '<User %r>' % self.userid

@app.route('/insert_user',methods=['GET','POST'])
def insert_user():
    '''add a user through POST from android'''
    userDic = request.form
    user = Users(userDic['name'],userDic['password'],userDic['authRank'])
    print('23333333')
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': '200', 'message': '插入成功！'})

@app.route('/delete')


#测试入口
@app.route('/')
def hello_world():
    return jsonify({'status': '0', 'errmsg': '登录成功！'})


if __name__ == '__main__':
    #
    app.run()




















