from flask_login import UserMixin
from flask import current_app
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher

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
    def __init__(self, id_number, username, password, profile_image_path, department, account_type, gender, mail):
        self.id = id_number
        self.active = True
        self.set_user(username,id_number, mail, account_type,gender,department, password)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return self.username

    def set_user(self, username=None,id_number=None,mail=None,account_type=None,gender=None,department=None,password=None):
        if username:
            self.username = username

        if id_number:
            self.id_number = id_number
        
        if mail:
            self.mail = mail

        if password:
            self.password = password
        
        if account_type:
            self.account_type = account_type
        
        if gender:
            self.gender = gender
            if self.gender == "Male":
                self.profileimage = "../static/profile_images/boy.png"
            else:
                self.profileimage = "../static/profile_images/girl.png"
        
        if department:
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

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

    
    def get_user(self,user_name):
        with dbapi2.connect(database=self.database, user=self.user, password=self.password) as connection:
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
        with dbapi2.connect(database=self.database, user=self.user, password=self.password) as connection:
            cursor = connection.cursor()
            if where is not None:
                query = f"""SELECT * FROM DEPARTMENT WHERE (department_code = '{where}')"""
            else:
                query = f"""SELECT * FROM DEPARTMENT"""

            cursor.execute(query)
            print(where)
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
        with dbapi2.connect(database=self.database, user=self.user, password=self.password) as connection:
            cursor = connection.cursor() 
            try:
                cursor.execute("""INSERT INTO USERS (user_id, user_name, password, profile_image_path, department, account_type, gender, mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (int(User.id_number), User.username, User.password, User.profileimage ,User.department, User.account_type, User.gender, User.mail))
                connection.commit()
            except dbapi2.Error as e:
                return "Error"
                
                

def get_User(user_name):
    user = current_app.config["db"].get_user(user_name)
    return user