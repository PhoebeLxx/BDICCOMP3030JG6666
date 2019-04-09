from flask import Flask,render_template,request,redirect,session,jsonify,make_response
from werkzeug.utils import secure_filename
import os
import json
import cv2
import time
from datetime import timedelta
from email_verificatoin import email_verify
from flask_cors import CORS
from re_verification import *
import user
import employee
import administrator

app = Flask(__name__)
CORS(app,support_credentials=True)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=7)
app.send_file_max_age_default = timedelta(seconds=10)


# @app.route('/')
# def home():
#     user = session.get('username')
#     if user:
#         return redirect('/1/')
#     else:
#         return redirect('/0/')
#
# @app.route('/<is_login>/')
# def home_page(is_login):
#     if is_login == '1':
#         return render_template('homepage.html',user=session['username'])
#     else:
#         return render_template('homepage.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login_info = json.load(request.get_data())
        name = login_info['name']
        return_value = {}
        if verify_username(name):
            return_value = user.user_all_info(name)
            return jsonify(return_value)
        elif verify_employeename(name):
            return_value['state'] = "2"
            return jsonify(return_value)
        elif verify_administrator_name(name):
            return_value['state'] = "3"
            return jsonify(return_value)
        else:
            return_value['state'] = "-1"
            return jsonify(return_value)

@app.route('/user_login/',methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_data()
        login_info = json.load(data)
        return user.login(login_info['username'],login_info['password'])
    # test
    # return render_template('loginpage.html')

#TODO 改
@app.route('/employee_login/',methods=['GET','POST'])
def employee_login():
    if request.method == 'POST':
        data = request.get_data()
        login_info = json.load(data)
        return user.login(login_info['username'],login_info['password'])

@app.route('/administrator_login/',methods=['GET','POST'])
def administrator_login():
    if request.method == 'POST':
        data = request.get_data()
        login_info = json.load(data)
        return user.login(login_info['username'],login_info['password'])

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_data()
        register_info = json.load(data)
        # register_info = {}
        if register_info['verify'] == 0:

            register_info['email'] = request.form['email']
            verification_code = email_verify(register_info['email'])
            return verification_code
        else:
            register_info['username'] = request.form['username']
            register_info['password'] = request.form['password']
            register_info['confirm_password'] = request.form['confirm_password']
            # register_info['passport_num'] = request.form['passport']
            register_info['phone_num'] = request.form['phone_number']
            # register_info['email'] = request.form['email']
            return user.register(register_info)


@app.route('/customer_info/',methods=['GET','POST'])
def customer_info():
    if request.method == 'POST':
        update_info = {}
        update_info['old_username'] = request.form['old_name']
        update_info['first_name'] = request.form['first_name']
        update_info['last_name'] = request.form['last_name']
        update_info['user_name'] = request.form['user_name']
        update_info['password'] = request.form['password']
        update_info['confirm_password'] = request.form['confirm_password']
        update_info['passport_id'] = request.form['passport_id']
        update_info['mobile_cn'] = request.form['mobile_cn']
        update_info['email'] = request.form['email']
        update_info['birthday'] = request.form['birthday']
        update_info['address'] = request.form['address']

        user_image = request.files['user_image']

        # TODO 所有信息同时更新还是可以分开更新？
        # user.update_name(update_info['old_name'],update_info['new_name'])
        # user.update_password(update_info['old_name'],update_info['password'],update_info['confirm_password'])
        # user.update_passport(update_info['old_name'],update_info['passport_num'])
        # user.update_email(update_info['old_name'],update_info['email'])
        # user.update_phone(update_info['old_name'],update_info['phone_num'])
        # user.update_user_image(update_info['old_name'],user_image)
        return None

@app.route('/luggage/order/create',methods=['GET','POST'])
def luggage_order_create():
    if request.method == 'POST':
        insurance_info = {}
        insurance_info['first_name'] = request.form['first_name']
        insurance_info['last_name'] = request.form['last_name']
        insurance_info['user_name'] = request.form['user_name']
        insurance_info['passport_id'] = request.form['passport_id']
        insurance_info['mobile_cn'] = request.form['mobile_cn']
        insurance_info['email'] = request.form['email']
        insurance_info['birthday'] = request.form['birthday']
        insurance_info['address'] = request.form['address']

        insurance_info['product_id'] = request.form['product_id']
        insurance_info['project_id'] = request.form['project_id']
        insurance_info['flight_number'] = request.form['flight_number']

        insurance_info['status'] = 0    # 0-未处理

        insurance_info['luggage_image_outside'] = request.files['luggage_image_outside']
        insurance_info['luggage_image_inside'] = request.files['luggage_image_inside']
        insurance_info['luggage_height'] = request.files['luggage_height']
        insurance_info['luggage_width'] = request.files['luggage_width']

        insurance_info['remark'] = request.files['remark']

        return user.buy_insurance(insurance_info)

@app.route('/luggage/order/list',methods=['GET','POST'])
def luggage_order_list():
    if request.method == 'POST':
        claim_info = {}
        claim_info['order_id'] = request.form['order_id']
        claim_info['user_name'] = request.form['user_name']
        claim_info['lost_time'] = request.form['lost_time']
        claim_info['lost_place'] = request.form['lost_place']
        claim_info['flight_number'] = request.form['flight_number']
        claim_info['lost_reason'] = request.form['lost_reason']
        claim_info['remark'] = request.form['remark']
        claim_info['employee_id'] = -1  # 表示新的订单，没有员工处理
        claim_info['status'] = -1

        return user.apply_claim(claim_info)

@app.route('/apply_claim/',methods=['GET','POST'])
def apply_claim_page():
    if request.method == 'POST':
        claim_info = {}
        claim_info['insurance_id'] = request.form['insurance_id']
        claim_info['employee_id'] = -1 # 表示新的订单，没有员工处理
        claim_info['reason'] = request.form['reason']
        claim_info['status'] = -1

        return user.apply_claim(claim_info)

@app.route('/logout/')
def logout_page():
    session.clear() # TODO 用户登出要清cookie和session
    return None

@app.route('/employee_login/',methods=['GET','POST'])
def employee_lonin_page():
    employeeid = request.form['employeeid']
    password = request.form['password']
    return employee.login(employeeid, password)

@app.route('/employee_update_password/',methods=['GET','POST'])
def employee_update_password_page():
    employeeid = request.form['employeeid']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    return employee.update_password(employeeid,new_password,confirm_password)

# TODO 员工是否应该看到所有的保险和理赔申请？
@app.route('/check_all_insurance/',methods=['GET','POST'])
def list_all_insurance_page():
    return employee.list_all_insurance()

@app.route('/list_all_claim/',methods=['GET','POST'])
def list_all_claim_page():
    return employee.list_all_claim()

@app.route('/address_claim/',methods=['GET','POST'])
def address_claim_page():
    claim_id = request.form['claim_id']
    # state = request.form['state']
    audit_result = request.form['audit_result']
    return employee.address_claim(claim_id,audit_result)

@app.route('/administrator_login/',methods=['GET','POST'])
def administrator_login_page():
    administratorid = request.form['administratorid']
    password = request.form['password']
    return administrator.login(administratorid, password)

@app.route('/administrator_update_password/',methods=['GET','POST'])
def administrator_update_password():
    administratorid = request.form['administratorid']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    return administrator.update_password(administratorid, new_password, confirm_password)


@app.route('/create_new_administrator/',methods=['GET','POST'])
def create_new_administrator():
    new_id = request.form['new_id']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    return administrator.create_new_administrator(new_id,password,confirm_password)

@app.route('/delete_administrator/',methods=['GET','POST'])
def delete_administrator():
    current_id = request.form['current_id']
    delete_id = request.form['delete_id']
    return administrator.delete_administrator(current_id,delete_id)

@app.route('/create_employee/',methods=['GET','POST'])
def create_employee():
    employee_id = request.form['employee_id']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    return administrator.create_employee(employee_id, password, confirm_password)

@app.route('/delete_employee/',methods=['GET','POST'])
def delete_employee():
    delete_employee_id = request.form['delete_employee_id']
    return administrator.delete_employee(delete_employee_id)

@app.route('/update_employee_password/',methods=['GET','POST'])
def update_employee_password():
    update_employee_id = request.form['update_employee_id']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    return administrator.update_employee_password(update_employee_id,password,confirm_password)

@app.route('/delete_user/',methods=['GET','POST'])
def delete_user():
    delete_username = request.form['delete_username']
    return administrator.delete_user(delete_username)

# TODO list
"""
1. administrator 是否看到所有的claim和insurance，是否可以和员工共用一个方法？(再一个py文件)
2. administrator 的名字问题，a@开头
3. 员工和管理员的名字前缀(e@,a@),应不应该手动输入
4. 其他信息的正则验证
5. 状态位的确定
"""

if __name__ == '__main__':
    app.run()
