from flask_login import UserMixin
from flask import current_app
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from psycopg2.extensions import AsIs


class Class():
    def __init__(self,className,classCode,tutor,videoList,department,review_point):
        self.className = className
        self.classCode = classCode
        self.tutor = tutor
        self.videoList = videoList
        self.department = department
        self.review_point = review_point

class Department():
    def __init__(self,department_code,department_name):
        self.department_code = department_code
        self.department_name = department_name

class Person(UserMixin):
    def __init__(self, id_number, username, password, department, account_type, gender, mail, profileimage=None):
        self.id = id_number
        self.active = True
        self.set_user(username, id_number, mail, account_type, gender, department, password)
        self.profileimage = profileimage

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return self.username

    def convert_image_path(self):
        image_path = self.profileimage
        self.profileimage = image_path.replace("./itu-be","../..")

    def set_user(self, username=None,id_number=None,mail=None,account_type=None,gender=None,department=None,password=None):
        if username is not None:
            self.username = username

        if id_number is not None:
            self.id_number = id_number
        
        if mail is not None:
            self.mail = mail

        if password is not None:
            self.password = password
        
        if account_type is not None:
            self.account_type = account_type

        if gender is not None:
            self.gender = gender
            if self.gender == "Male":
                self.profileimage = "../static/profile_images/boy.png"
            else:
                self.profileimage = "../static/profile_images/girl.png"

        if department is not None:
            self.department = department
    
    

class Video():
    def __init__(self, video_name, video_code, tutor, department, review_point, thumbnail, path):
        self.video_name = video_name
        self.video_code = video_code
        self.tutor = tutor
        self.department = department
        self.review_point = review_point
        self.thumbnail = thumbnail
        self.path = path
    
    def getVideoName(self):
        return self.video_name

    
class DataBase():

    def __init__(self, url):
        self.url = url

    def CheckIfDataExists(self,data,check):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE ({check} = '{data}' )"""
            cursor.execute(query)
            try:
                User = cursor.fetchone()
                if data == User[6] or data == User[0] or data == User[1]:
                    return True
                else:
                    return False
            except:
                return False

    def update_user_info(self, id_number, user_data):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """"""
            user = self.get_user_with_id(id_number)

            if user_data.id_number != user.id_number:
                query = """UPDATE USERS SET user_id = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.id_number, id_number))

            if user_data.username != user.username:
                query = """UPDATE USERS SET user_name = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.username, id_number))

            if user_data.password != user.password:
                query = """UPDATE USERS SET password = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.password, id_number))

            if user_data.department != user.department:
                query = """UPDATE USERS SET department = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.password, id_number))

            if user_data.profileimage != user.profileimage:
                query = """UPDATE USERS SET profile_image_path = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.profileimage, id_number))

            if user_data.account_type != user.account_type:
                query = """UPDATE USERS SET account_type = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.account_type, id_number))

            if user_data.gender != user.gender:
                query = """UPDATE USERS SET gender = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.gender, id_number))

            if user_data.mail != user.mail:
                query = f"""UPDATE USERS SET mail = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.mail, id_number))

            try:
                connection.commit()
                return True
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_user_with_id(self,id_number):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_id = '{id_number}' )"""
            cursor.execute(query)
            try:
                User = cursor.fetchone()
                User = Person(User[0],User[1],User[2],User[3],User[4],User[5],User[6],User[7])
                connection.commit()
                return User
            except:
                return None

    def get_user(self,user_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_name = '{user_name}' )"""
            cursor.execute(query)
            try:
                User = cursor.fetchone()
                User = Person(User[0],User[1],User[2],User[3],User[4],User[5],User[6],User[7])
                connection.commit()
                return User
            except:
                return None

    def get_departments(self,where=None):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            if where is not None:
                query = f"""SELECT * FROM DEPARTMENT WHERE (department_code = '{where}')"""
            else:
                query = f"""SELECT * FROM DEPARTMENT"""

            cursor.execute(query)
            if where is None:
                try:
                    departments_list = []
                    departments = cursor.fetchall()

                    for department in departments:
                        departments_list.append(Department(department[0],department[1]))
                    
                    return departments_list
                except:
                    return None
            else:
                try:
                    department = cursor.fetchone()
                    department = Department(department[0],department[1])
                    
                    return department
                except:
                    return None

    def create_user(self, User):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor() 
            try:
                cursor.execute("""INSERT INTO USERS (user_id, user_name, password, profile_image_path, department, account_type, gender, mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (int(User.id_number), User.username, User.password, User.profileimage ,User.department, User.account_type, User.gender, User.mail))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode)
                
                

def get_User(user_name):
    user = current_app.config["db"].get_user(user_name)
    return user