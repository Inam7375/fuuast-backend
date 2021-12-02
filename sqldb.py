from pymongo.cursor import CursorType
import pyodbc 
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from bson import json_util
from flask import jsonify
import json
from datetime import datetime

# df = pd.read_csv('creds.csv')
def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                      f'Server={"FAISAL-COMPUTER"};'
                      f'Database={"FUUAST"};'
                      'Trusted_Connection=yes;')
    # conn = sqlite3.connect('Users.sqlite')

    return conn



################################## USER END POINTS ##########################################

def get_users():
    try:
        results = []
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users")
        result = list(cursor)
        conn.close()
        for i in result:
            results.append(
                {
                    '_id' : i[0],
                    'status': i[1],
                    'name' : i[2],
                    'email' : i[3],
                    'password' : i[4],
                    'department' : i[5],
                    'designation' : i[6],
                    'role' : i[7],
                    'date_created' : i[8]        
                }   
            )
        return results
    except Exception:
        return False
    else:
         if conn.connected == 1:
            conn.closed()
    


def get_user(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users where id = '{uname}'")
        result = list(cursor)
        conn.close()
        return {
            '_id' : result[0][0],
            'name' : result[0][2],
            'email' : result[0][3],
            'password' : result[0][4],
            'department' : result[0][5],
            'designation' : result[0][6],
            'role' : result[0][7]        
            }   
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()
    


def save_user(uname, name, email, password, dpt, desig, role):
    hash_pass = generate_password_hash(password)
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"insert into Users ([id], [status], [name], [email], [password], [department], [designation], [role], [date_created]) values ('{uname}', '{1}', '{name}', '{email}', '{hash_pass}', '{dpt}', '{desig}', '{role}', '{datetime.now()}')"
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
    else:
        if conn.connected == 1:
            conn.closed()


def update_user(uname, name, email, password, dpt, desig, role):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"update users set id='{uname}', name='{name}', email='{email}', password='{password}', dpt='{dpt}', desig='{desig}', role='{role}' where id = '{uname}'"
        )
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.closed()

def update_user_status(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
                f"select status from users where id = '{uname}'"
            )

        if len(list(cursor)) == 0:
            return False

        status = tuple(cursor)
        status = not status[0][0]
        cursor.execute(
            f"""update users set status='{"1" if status == True else "0"}' where id = '{uname}'"""
        )
        conn.commit()
        conn.close()
        return True

    except Exception:
        return False
    else:
        if conn.connected == 1:
            conn.closed()


def del_user(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from users where id = '{uname}'"
        )
        if len(list(cursor)) == 0:
            return False
        else:
            cursor.execute(
                f"delete from users where id = '{uname}'"
            )
        conn.commit()
        conn.close()
        return True

    except Exception:
        return False
    else:
        if conn.conncected == 1:
            conn.close()

##################### USER NOTIFICATION END POINTS ################################

def save_user_notify(
    docID,
    created=False,
):
    try:
        conn = connect()
        cursor = conn.cursor()
        docID = docID.split('-')
        cursor.execute(
            f"select target_user, created_by_user from document where id = '{docID[1]}' and department = '{docID[0]}'"
        )
        uname = list(cursor)
        if len(uname) == 0:
            return False
        else:
            cursor.execute(
                f"""insert into user_notifications (uname, title, docID, docDep, msg, icon, time,category) values ('{uname[0][0]}', 'New document in pending', '{docID[1]}', '{docID[0]}', '{'-'.join(docID)} is pending...', 'AlertOctagonIcon', '{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}','success')"""
            )
            print('Done')
            conn.commit()
            if created != True:
                cursor.execute(
                    f"""insert into user_notifications (uname, title, docID, docDep, msg, icon, time,category) values ('{uname[0][1]}', 'New update in your document', '{docID[1]}', '{docID[0]}', '{'-'.join(docID)} + " recieved a new update."', 'MailIcon', '{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 'primary')"""
                )
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connect == 1:
            conn.close()

def get_user_notifications(
    uname
):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from user_notifications where uname = '{uname}'"
        )
        columns = [column[0] for column in cursor.description]
        notifications = []
        for row in cursor.fetchall():
            notifications.append(dict(zip(columns, row)))
        conn.close()
        notifications = sorted(
            notifications, key=lambda k: k['time'], reverse=True)
        notification = []
        for i in notifications:
            i['time'] = i['time'].strftime("%d/%m/%Y %H:%M:%S")
            notification.append(i)
        return notification
    except Exception as e:
        print(e)
        return False


################################### DEPARTMENT END POINTS ################################

def save_department(
    depName,
    depHOD,
    about
):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"""
                insert into department 
                (
                    id,
                    depHOD,
                    about
                )
                values(
                    '{depName}',
                    '{depHOD}',
                    '{about}'
                )
            """
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
    else:
        if conn.connected == 1:
            conn.close()


def get_departments():
    try:
        
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from department"
        )
        columns = [column[0] for column in cursor.description]
        departments = []
        for row in cursor.fetchall():
            departments.append(dict(zip(columns, row)))
        conn.close()
        department = []
        for i in departments:
            id = i.pop('id')
            i['_id'] = str(id)
            department.append(i)        
        return department
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def update_department(depName, depHOD, about):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"update department set depHOD = '{depHOD}', about = '{about}' where id = '{depName}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def del_department(id):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"delete from department where id = '{id}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()




################################### DOCUMENT END POINTS ################################

def get_documents():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from document"
        )
        columns = [column[0] for column in cursor.description]
        documents = []
        for row in cursor.fetchall():
            documents.append(dict(zip(columns, row)))
        conn.close()
        document = []
        for i in documents:
            id = i.pop('id')
            department = i.pop('department')
            i['_id'] = department + '-' + str(id)
            document.append(i)
        return document
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def get_user_created_document(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from document where created_by_user = '{uname}' and isCompleted = {0}"
        )
        columns = [column[0] for column in cursor.description]
        documents = []
        for row in cursor.fetchall():
            documents.append(dict(zip(columns, row)))
        conn.close()
        document = []
        for i in documents:
            id = i.pop('id')
            department = i.pop('department')
            i['_id'] = department + '-' + str(id)
            document.append(i)
        return document
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def get_user_completed_document(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from document where created_by_user = '{uname}' and isCompleted = {1} and archived = {0}"
        )
        if len(list(cursor)) < 1:
            return False
        cursor.execute(
            f"select * from document where created_by_user = '{uname}' and isCompleted = {1} and archived = {0}"
        )
        columns = [column[0] for column in cursor.description]
        documents = []
        for row in cursor.fetchall():
            documents.append(dict(zip(columns, row)))
        conn.close()
        document = []
        for i in documents:
            id = i.pop('id')
            department = i.pop('department')
            i['_id'] = department + '-' + str(id)
            document.append(i)
        return document
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()

def get_user_pending_document(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select * from document where target_user = '{uname}'"
        )
        columns = [column[0] for column in cursor.description]
        documents = []
        for row in cursor.fetchall():
            documents.append(dict(zip(columns, row)))
        conn.close()
        document = []
        for i in documents:
            id = i.pop('id')
            department = i.pop('department')
            i['_id'] = department + '-' + str(id)
            document.append(i)
        return document
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()

            
def save_user_approved_documents(uname, docID):
    try:
        docID = docID.split('-')
        
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"select id from users where id = '{uname}'"
        )
        res = list(cursor)
        if len(res) < 1:
            return False
        cursor.execute(
        f"""insert into approved_document_sequence
            (
                uname,
                docID,
                docDep
            )
            values
            (
                '{uname}',
                '{docID[1]}',
                '{docID[0]}'
            )
        """ 
        ) 
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()
      

# def get_user_approved_document(uname):
#     try:
#         conn = connect()
#         cursor = conn.cursor()
#         cursor.execute(
#             f"update document set isCompleted = 1 where id = '{docID[0]}' and department = '{docID[1]}'"
#         )
#         conn.commit()
#         conn.close()
#     ids = doc_approval_collection.find({'uname': uname})
#     if ids:
#         ids = list(ids)
#         ids = ids[0]['documents']
#         ids = list(dict.fromkeys(ids))
#         documents = doc_collection.find()
#         print(list(documents))


def save_document(
    title,
    createdByName,
    createdByUName,
    createdByDep,
    targetUName,
    targetUDep,
    description,
    final_user
):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = f"""exec dbo.get_process_id  
                    '{title}',
                    '{createdByDep}',
                    '{createdByUName}',
                    '{createdByName}',
                    '{createdByDep}',
                    '{targetUName}',
                    '{targetUDep}',
                    '{description}',
                    '{final_user}',
                     0"""
        cursor.execute(query)
        id = cursor.fetchone()[0]  # although cursor.fetchval() would be preferred
        conn.commit()
        conn.close()
        save_user_notify(createdByDep + "-" + str(id), True)
        return True
    except Exception as e:
        print(e)
        return False

def update_completion(docID):
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"select id from document where id = '{docID[1]}'")
        res = list(cursor)
        if len(res) < 1:
            return False
        cursor.execute(
            f"update document set isCompleted = 1 where id = '{docID[1]}' and department = '{docID[0]}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def document_archived(docID):
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"update document set archived = 1 where id =  '{docID[0]}' and department = '{docID[1]}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()


def archive_document(id):
    try:
        docID = id.split('-')
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"update document set archived = 1 where id =  '{docID[0]}' and department = '{docID[1]}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()



##################### LOG & LOG SEQUENCE END POINTS ################################

def get_log(docID):
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor() 
        cursor.execute(
            f"select * from logs where docID={docID[1]} and docDep = '{docID[0]}'"
        
        )
        res = list(cursor)
        if len(res) < 1:
            return False
        cursor.execute(
            f"select * from logs where docID={docID[1]} and docDep = '{docID[0]}'"
        
        )
        columns = [column[0] for column in cursor.description]
        logs = []
        for row in cursor.fetchall():
            logs.append(dict(zip(columns, row)))
        conn.close()
        log = []
        for i in logs:
            id = i.pop('docID')
            department = i.pop('docDep')
            i['_id'] = department + '-' + str(id)
            log.append(i)
        return log
    except Exception as e:
        print(e)
        return False


def save_log_sequence(
    docID
):
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor() 
        cursor.execute(
            f"select * from log_sequences where docID='{docID[1]}' and docDep = '{docID[0]}'"
       
        )
        if len(list(cursor)) > 0:
            cursor.execute(
            f"insert into log_sequences (docID,docDep,sequence) values ('{docID[1]}', ''{docID[0]}', 'Recieved')"
       
        )
        else:
            cursor.execute(
            f"insert into log_sequences (docID,docDep,sequence) values ('{docID[1]}', ''{docID[0]}', 'Recieved')"
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False
    else:
        if conn.connected == 1:
            conn.close()


def get_log_sequence(docID):
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor() 
        cursor.execute(
            f"select * from log_sequences where docID='{docID[1]}' and docDep = '{docID[0]}'"
        )
        resp = list(cursor)
        conn.close()
        if len(resp) > 0:
            return resp
        else:
            return False
    except Exception:
        return False
    else:
        if conn.connected == 1:
            conn.close()


def save_log(
    docID,
    forwardedToUname,
    forwardedDep,
    objection,
    comments,
    date
):

    # create log db
    try:
        docID = docID.split('-')
        conn = connect()
        cursor = conn.cursor() 
        cursor.execute(
            f"insert into logs (docID, docDep, forwardedToUname, forwardedDep, objection, comments, date) values('{docID[1]}', '{docID[0]}', '{forwardedToUname}', '{forwardedDep}', '{objection}', '{comments}', '{date}')"
       
        )

        log = get_log(docID)
        if log:
            save_log_sequence(docID)
        conn.commit()
        cursor.execute(
            f"update document set target_user = '{forwardedToUname}' where id='{docID[1]}' and department='{docID[0]}'"
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
    else:
        if conn.connected == 1:
            conn.close()





if __name__ == "__main__":
    save_document(
        'Bill Approval',
        'Sajid Khokar',
        'sajidkhokar',
        'HR',
        'Mateen',
        'CS',
        'This is a bill document',
        'Mateen'
    )
    # print(save_log(
    #     'CS-6',
    #     'Mateen',
    #     'CS',
    #     'None',
    #     'None',
    #     datetime.now()
    # ))
