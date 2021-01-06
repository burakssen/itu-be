from flask import current_app
import psycopg2 as dbapi2
import os
import sys


from entities.Department import Department
from entities.Person import Person
from entities.Class import Class
from entities.Video import Video
from entities.Comment import Comment

class DataBase():

    def __init__(self):
        self.url = os.getenv("DATABASE_URL")



    def CheckIfDataExists(self, data, check):
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
                cursor.execute(query, (user_data.department, id_number))

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

            if user_data.title != user.title:
                query = f"""UPDATE USERS SET title = %s WHERE user_id = %s;"""
                cursor.execute(query, (user_data.title, id_number))

            try:
                connection.commit()
                return True
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_user_with_id(self, id_number):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_id = '{id_number}' )"""
            cursor.execute(query)
            try:
                User = cursor.fetchone()
                User = Person(User[0], User[1], User[2], User[3], User[4], User[5], User[6], User[8], User[7])
                connection.commit()
                return User
            except:
                return None

    def get_user(self, user_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_name = '{user_name}' )"""
            cursor.execute(query)
            try:
                User = cursor.fetchone()
                User = Person(User[0], User[1], User[2], User[3], User[4], User[5], User[6], User[8], User[7])
                connection.commit()
                return User
            except:
                return None


    def get_all_users(self):
        user_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (account_type != 'admin' )"""
            cursor.execute(query)
            try:
                users = cursor.fetchall()
                for User in users:
                    User = Person(User[0], User[1], User[2], User[3], User[4], User[5], User[6], User[8], User[7])
                    user_list.append(User)
                connection.commit()
                return user_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_departments(self, where=None):
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
                        departments_list.append(Department(department[0], department[1]))

                    return departments_list
                except:
                    return None
            else:
                try:
                    department = cursor.fetchone()
                    department = Department(department[0], department[1])

                    return department
                except:
                    return None

    def create_user(self, User):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO USERS (user_id, user_name, password, profile_image_path, department, account_type, gender, mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (int(User.id_number), User.username, User.password, User.profileimage, User.department,
                     User.account_type, User.gender, User.mail))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def delete_user(self, user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""DELETE FROM USERS WHERE user_id = %s""", (user_id,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def create_class(self, nclass):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO Class (class_code, class_name, tutor, review_points, class_context) VALUES (%s, %s, %s, %s, %s)""",
                    (nclass.class_code, nclass.class_name, nclass.tutor, nclass.review_points, nclass.class_context))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Class code exists"

    def get_tutors_classes(self, id_number):
        class_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM Class WHERE (tutor = %s)"""
            try:
                cursor.execute(query, (id_number,))
                classes = cursor.fetchall()

                for nclass in classes:
                    nclass = Class(nclass[1], nclass[0], nclass[2], nclass[3], nclass[4])
                    class_list.append(nclass)

                connection.commit()
                return class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_all_classes(self):
        class_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM Class"""
            try:
                cursor.execute(query)
                classes = cursor.fetchall()

                for nclass in classes:
                    nclass = Class(nclass[1], nclass[0], nclass[2], nclass[3], nclass[4])
                    class_list.append(nclass)

                connection.commit()
                return class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_class_with_class_code(self,class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM Class WHERE class_code = %s"""
            try:
                cursor.execute(query,(class_code,))
                classes = cursor.fetchone()
                nclass = Class(classes[1], classes[0], classes[2], classes[3], classes[4])
                connection.commit()
                return nclass
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)


    def create_video(self, video):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO Video (video_code, video_name, class_code, tutor, comments_available, thumbnail_path, 
                    video_path, video_descriptions, review_points) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (video.video_code, video.video_name, video.class_code, video.tutor, video.comments_available,
                     video.thumbnail_path, video.video_path, video.video_descriptions, video.review_points))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Video code exists"

    def get_videos(self,class_code):
        video_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM Video WHERE (class_code = %s)"""
            try:
                cursor.execute(query, (class_code,))
                videos = cursor.fetchall()

                for video in videos:
                    video = Video(video[2],video[1],video[4],video[3],video[9],video[6],video[7],video[8],video[5])
                    video_list.append(video)

                connection.commit()
                return video_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_video_with_video_code(self,video_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM Video WHERE (video_code = %s)"""
            try:
                cursor.execute(query, (video_code,))
                video = cursor.fetchone()
                video = Video(video[2],video[1],video[4],video[3],video[9],video[6],video[7],video[8],video[5])
                connection.commit()
                return video
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def create_comment(self,comment):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO comments (comment_id, user_id, video_code, comment_context) VALUES (%s, %s, %s, %s)""",
                    (comment.comment_id, comment.user_id, comment.video_code, comment.comment_context))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Comment code exists"

    def get_comments(self, video_code):
        comment_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """SELECT * FROM comments WHERE video_code = %s""", (video_code,)
                )
                comments = cursor.fetchall()
                for comment in comments:
                    comment = Comment(comment[0],comment[1],comment[2],comment[3])
                    comment_list.append(comment)
                connection.commit()

                return comment_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Comment code exists"

def get_User(user_name):
    user = current_app.config["db"].get_user(user_name)
    return user