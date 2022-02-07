from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Employee(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    dept=db.Column(db.String(20))
    dept_name=db.Column(db.String(20))
    manager_name=db.Column(db.String(20))


class Department(db.Model):
    id=db.Column(db.Integer)
    dept=db.Column(db.String(20), db.ForeignKey(Employee.dept), primary_key=True)
    dept_name=db.Column(db.String(20))
    manager_name=db.Column(db.String(20))


@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        dept=request.form['dept']
        dept_name=request.form['dept_name']
        manager_name=request.form['manager_name']
        employee=Employee(id=id, name=name, dept=dept, dept_name=dept_name, manager_name=manager_name)
        department=Department(dept=dept, dept_name=dept_name, manager_name=manager_name)

        try:
            db.session.add(employee)
            db.session.add(department)
            db.session.commit()
            return redirect('/')
        except:
            return "Problem adding employee !"

    else:
        employee=Employee.query.order_by(Employee.id).all()
        department=Department.query.order_by(Department.dept).distinct()
        return render_template('index.html', employee=employee, department=department)


@app.route('/update/<int:id>', methods = ["POST", "GET"])
def update(id):
    emp = Employee.query.get_or_404(id)

    if request.method == 'POST':
        emp.name = request.form["name"]
        emp.dept = request.form["dept"]
        emp.dept_name = request.form["dept_name"]
        emp.manageer_name = request.form["manager_name"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Cannot update employee Info!!!"

    else:
        return render_template("update.html", emp = emp)


@app.route('/delete/<int:id>')  
def delete(id):
    edel=Employee.query.get_or_404(id) 
    emp_left= len(Employee.query.filter(Employee.dept == edel.dept).all())
    if emp_left==1:
        d_del=Department.query.get_or_404(edel.dept)
    try:
        if emp_left>1:
            db.session.delete(edel)
            db.session.commit()
            return redirect('/')
        else:
            db.session.delete(edel)
            db.session.delete(d_del)
            db.session.commit()
            return redirect('/')
    except:
        return "Problem in deleting data!!!"

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)