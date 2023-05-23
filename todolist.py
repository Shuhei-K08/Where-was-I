from flask import render_template,request,redirect,url_for,flash
from flask import Flask
import mysql.connector
import os
import importlib
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv()
application = Flask(__name__)
application.config["SECRET_KEY"] = "sample1203"
from flaskext.mysql import MySQL

mysql = MySQL()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

application.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER")
application.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASSWORD")
application.config['MYSQL_DATABASE_DB'] = os.getenv("DB_DATABASE")
application.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST")

mysql.init_app(application)

cnx = mysql.connect()
cursor = cnx.cursor()

def listTodo():
    sql = "SELECT id,task,date FROM todolist ORDER BY date ASC "
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return result
def createTodo():
    
        tasks = {
            'task':request.form.get('task'),
            'date':request.form.get('date'),
        }
        if not tasks['task']:
            return
        if not tasks['date']:
            return
        else:
            sql = '''
                    INSERT INTO todolist
                    (task,date)
                    VALUES
                    (%s, %s)
                    '''
            data = (tasks['task'],
                    tasks['date'],
                    )
            cursor.execute(sql, data)
            cnx.commit()
            
            
def search1():
    sql = "SELECT id,title,date FROM report LIKE %s "
    data=request.form.get('todo')
    cursor.execute(sql,data)
    result = cursor.fetchall()
    
    return result


def listReport():
    
    sql = "SELECT id,title,date FROM report ORDER BY date ASC "
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

@application.route("/top", methods=['GET', 'POST'])
def hoge():
    tasks = listTodo()
    lists = listReport()
    if request.method == "POST":
        if request.form['send']=="追加":
            createTodo()
            return redirect("/todolist.py/top")
    return render_template('todolist.html',lists=lists, tasks=tasks)


@application.route("/delieteTodo/<int:todolist_id>",methods=['GET'])
def deleteTodo(todolist_id):
    todolist_id=todolist_id
    sql="DELETE FROM todolist WHERE id = %s"
    data=todolist_id
    cursor.execute(sql, data)
    cnx.commit()
    return redirect("/todolist.py/top")



def createReport():
        
        report= {
            'title':request.form.get("title"),
            'company':request.form.get("company"),
            'name':request.form.get("name"),
            'content':request.form.get("content"),
            'date':request.form.get("reportDate"),
        }
        if not report['title']:
            flash("題名を入力してください。")
            return
        if not report['name']:
            flash("担当者名を選択してください。")
            return
        if not report['content']:
            flash("商談内容を記入してください。")
            return
        if not report['company']:
            flash("企業名を選択してください。")
            return
        else:
            
            sql = '''
                    INSERT INTO report
                    (title,company,name,content,date)
                    VALUES
                    (%s,%s,%s,%s,%s)
                    '''
            data = (report['title'],
                    report['company'],
                    report['name'],
                    report['content'],
                    report['date']
                    )
            
            cursor.execute(sql, data)

        tasks = {
            'task':request.form.get("task"),
            'date':request.form.get("todoDate"),
        }
        if tasks['task']:
            table= '''
                    INSERT INTO todolist
                    (task,date)
                    VALUES
                    (%s, %s)
                    '''
            dates = (tasks['task'],
                    tasks['date'],
                    )
            cursor.execute(table, dates)
        cnx.commit()
        flash('商談メモを登録したしました。')

def getInfo():
    sql = "SELECT company,name FROM companyInfo "
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def companyInfo():
    sql = "SELECT company FROM company "
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

@application.route("/createReport",methods=['GET', 'POST'])
def hoge1():
    gets=getInfo()
    companies=companyInfo()
    if request.method == "POST":
        createReport()
    
    return render_template("createReport.html",gets=gets,companies=companies)

@application.route("/delieteReport/<int:listreport_id>",methods=['GET'])
def deleteReport(listreport_id):
    listreport_id=listreport_id
    sql="DELETE FROM report WHERE id = %s"
    data=listreport_id
    cursor.execute(sql, data)
    cnx.commit()
    return redirect("/todolist.py/top")
    
def createInfo():
        info = {
            'company':request.form.get('company'),
            'name':request.form.get('name'),
            'email':request.form.get('email'),
            'tel':request.form.get('tel'),
        }
        if not info['company']:
            flash('企業名を記入してください。')
        if not info['name']:
            flash('担当者名を記入してくだい。')
        else:
            sql = '''
                    INSERT INTO companyInfo
                    (company,name,email,tel)
                    VALUES
                    (%s,%s,%s,%s)
                            '''
            data = (info['company'],
                    info['name'],
                    info['email'],
                    info['tel']
                    )
            cursor.execute(sql, data)
            cnx.commit()
            flash('担当者情報を登録しました。')
            return redirect("/todolist.py/createReport")
def companyName():
    sql = "SELECT company FROM company "
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


@application.route('/createInfo',methods=['GET','POST'])
def hoge3():
    companies=companyName()
    if request.method == "POST":
        createInfo()
        
    return render_template("createInfo.html",companies=companies)


def createCompany():
        company = request.form.get('company')
        sql = "SELECT company FROM company "
        cursor.execute(sql)
        selectCompanies=cursor.fetchall()

        for selectCompany in selectCompanies:
            if company==selectCompany[0]:
                flash('企業名が重複してます。')
                return redirect("/todolist.py/company")
        if company=='':
            flash('企業名を記入してください。')
        else:
            sql = '''
                    INSERT INTO company
                    (company)
                    VALUES
                    (%s)
                            '''
            data = company
                    
            cursor.execute(sql, data)
            cnx.commit()
            flash('登録が完了しました。')
            return redirect("/todolist.py/company")
@application.route('/company',methods=['GET','POST'])
def hoge4():
    if request.method == "POST":
        createCompany()
    return render_template("company.html")

@application.route('/report/<int:report_id>',methods=['GET','POST'])
def reportDetail(report_id):
    report_id=report_id
    if request.method == "POST":
        report= {
            'title':request.form.get("title"),
            'company':request.form.get("company"),
            'name':request.form.get("name"),
            'content':request.form.get("content"),
            'date':request.form.get("date"),
        }
        sql = ('''
        UPDATE report
        SET title=%s,company=%s,name=%s,content=%s,date=%s
        WHERE id = %s
        ''')
        data = (report['title'],
                report['company'],
                report['name'],
                report['content'],
                report['date'],
                report_id
                )
        cursor.execute(sql, data)
        cnx.commit()
        return redirect("/todolist.py/top")
    else:
        sql="SELECT * FROM report where id=%s"
        data=report_id
        cursor.execute(sql, data)
        report=cursor.fetchone()
        companies=companyInfo()
        gets=getInfo()
        return render_template("reportDetail.html",report=report,companies=companies,gets=gets)
    
@application.route('/updateReport/<int:report_id>',methods=['GET','POST'])
def updateReport(report_id):
    report_id=report_id
    if request.method == "POST":
        report= {
            'title':request.form.get("title"),
            'company':request.form.get("company"),
            'name':request.form.get("name"),
            'content':request.form.get("content"),
            'date':request.form.get("date"),
        }
        
        sql = ('''
        UPDATE report
        SET title=%s,company=%s,name=%s,content=%s,date=%s
        WHERE id = %s
        ''')
        data = (report['title'],
                report['company'],
                report['name'],
                report['content'],
                report['date'],
                report_id
                )
        cursor.execute(sql, data)
        cnx.commit()
        return redirect("/todolist.py/top")
    else:
        sql="SELECT * FROM report where id=%s"
        data=report_id
        cursor.execute(sql, data)
        report=cursor.fetchone()
        companies=companyInfo()
        gets=getInfo()
        return render_template("updateReport.html",report=report,companies=companies,gets=gets,)
    
@application.route('/create_company', methods=['GET','POST'])
def companyInfo2():
    if request.method == "POST":
        companyName = request.form.get("company")
        sql = "SELECT id FROM company where company = %s"
        cursor.execute(sql,companyName)
        company_id = cursor.fetchone()[0]
        return redirect(url_for('listCompany',company_id=company_id))
    else:
        sql="SELECT * FROM company"
        cursor.execute(sql)
        lists=cursor.fetchall()
        return render_template("create_company.html", lists=lists)

@application.route('/listCompany/<int:company_id>',methods=['GET'])
def listCompany(company_id):
    company_id = company_id
    sql = "SELECT company FROM company where id = %s"
    cursor.execute(sql,company_id)
    companyName =cursor.fetchone()[0]
    sql = "SELECT * FROM companyInfo where company = %s"
    cursor.execute(sql,companyName)
    listsC = cursor.fetchall()
    return render_template("listCompany.html",listsC=listsC,companyName=companyName)

@application.route('/PIC/<int:info_id>',methods=['GET'])
def PIC(info_id):
    sql = "SELECT company FROM companyInfo where id= %s"
    cursor.execute(sql,info_id)
    companyName=cursor.fetchone()[0]
    sql = "SELECT id FROM company where company= %s"
    cursor.execute(sql,companyName)
    company_id=cursor.fetchone()[0]
    
    info_id = info_id
    sql="DELETE FROM companyInfo WHERE id = %s"
    data=info_id
    cursor.execute(sql, data)
    cnx.commit()
    flash('担当者情報を削除いたしました')
    return redirect(url_for('listCompany',company_id=company_id))

@application.route('/companyInfo')
def companyList():
    sql = "SELECT * FROM company"
    cursor.execute(sql)
    lists = cursor.fetchall()
    return render_template('companyInfo.html',lists=lists)


@application.route('/deleteCompany/<int:company_id>',methods=['GET'])
def deleteCompany(company_id):
    company_id=company_id
    sql="SELECT company FROM company WHERE id= %s"
    cursor.execute(sql,company_id)
    companyName=cursor.fetchone()[0]
    sql = "DELETE FROM company WHERE id = %s"
    cursor.execute(sql,company_id)
    sql = "DELETE FROM companyInfo WHERE company = %s"
    cursor.execute(sql,companyName)
    cnx.commit()
    flash('企業情報を削除いたしました')
    return redirect('/todolist.py/companyInfo')
