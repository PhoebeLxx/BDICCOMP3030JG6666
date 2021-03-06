from www.model.component.database_basic.whats_your_name import *

def search_username(username):
    '参数:username， 用户对象，否则None'
    return Users.query.filter_by(username=username).first()

def password_is_right(username, password):
    '参数:username, password'
    user = search_username(username)
    return user.check_password_hash(password)

def insert_user(dict):
    '参数:dict username,password,phone_num,email'
    user = search_username(dict['username'])
    assert (user is None), "Username already exist"
    db.session.add(Users(username=dict['username'],password=dict['password'],phone_num=dict['phone_num'],email=dict['email']))
    db.session.commit()
    return 'Create successfully'

def get_insurance(username):
    user = search_username(username)
    assert (user is not None), "Username already exist"
    return user.insurance_id.all()

def get_claim(username):
    user = search_username(username)
    assert (user is not None), "Username already exist"
    return user.claim_id.all()


def update_profile(username, new_profile):
    user = search_username(username)
    assert user is not None, 'No such user'
    user.profile = new_profile
    db.session.commit()
    return "Update successfully"

def update_username(username, new_name):
    user = search_username(username)
    assert (user is not None), "No such user"
    assert (not search_username(new_name)), 'This name already exist'
    user.username = new_name
    db.session.commit()
    return "Update successfully"

def update_password(username, new_password):
    user = search_username(username)
    assert (user is not None), "No such user"
    assert (not user.check_password_hash(new_password)),'Same password'
    user.password = new_password
    return "Update successfully"

def update_phone_num(username,new_phone_num):
    user = search_username(username)
    assert (user is not None), "No such user"
    assert (user.phone_num is not new_phone_num), 'Same phone num'
    user.phone_num = new_phone_num
    return "Update successfully"

def update_passport_num(username,new_passport_num):
    user = search_username(username)
    assert (user is not None), "No such user"
    assert (user.passport_num is not new_passport_num), 'Same passport_num'
    user.password = new_passport_num
    return "Update successfully"

def update_email(username, new_email):
    user = search_username(username)
    assert (user is not None), "No such user"
    assert (user.email is not new_email), 'Same email'
    user.password = new_email
    return 'Update email successfully'

def delete_user(username):
    user = search_username(username)
    assert (user is not None), "No such user"
    db.session.delete(user)
    db.session.commit()
    return 'Delete successfully'

if __name__ == '__main__':
    '参数:dict name,password,phone_num,passport_num,email, return boolean'
    # Users.insert_user({'username': '1cfabds', 'password': '1afsdfff', 'phone_num': 1213334,
    #                    'email': '133f23@1163.com'})

    user = Users.search_username('teds')
    print(user.insurance_id.all())