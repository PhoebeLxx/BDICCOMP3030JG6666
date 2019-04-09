from db_operatoin.database_basic.whats_your_name import Employee,db


def search_id(id):
    return Employee.query.filter_by(id = id).first()

def login(id, password):
    emp = search_id(id)
    assert(emp is not None),'No such id'
    assert(emp.check_password_hash(password)),'Wrong password'
    return "Login successfully"


def create(id, password):
    emp = search_id(id)
    assert(emp is not None),'Already exist'
    db.session.add(Employee(id = id, password = password))
    db.session.commit()
    return 'Create employee Successfully'


def update_password(id, new_password):
    emp = Employee.query.filter_by(id=id).first()
    assert (emp is not None), "No such employee"
    assert (not emp.check_password_hash(new_password)),"New password is same as old Password"
    emp.password = new_password
    return 'Update password successfully'



def delete(id):
    emp = Employee.query.filter_by(id=id).first()
    assert (emp is not None), "No such employee"
    db.session.delete(emp)
    db.session.commit()
    return 'successful'
