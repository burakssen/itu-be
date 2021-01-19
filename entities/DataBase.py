from flask import current_app
import psycopg2 as dbapi2
import os

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
            query = f"""SELECT * FROM USERS WHERE ({check} = %s )"""
            cursor.execute(query,(data,))
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
            query = """
                UPDATE USERS
                SET
                user_id = COALESCE(%s, user_id),
                user_name = COALESCE(%s, user_name),
                password = COALESCE(%s, password),
                department = COALESCE(%s, department),
                profile_image_path = COALESCE(%s, profile_image_path),
                account_type = COALESCE(%s, account_type),
                gender = COALESCE(%s, gender),
                mail = COALESCE(%s, mail),
                title = COALESCE(%s, title)
                WHERE user_id = %s
            """
            try:
                cursor.execute(query,(
                    user_data.id_number,
                    user_data.username,
                    user_data.password,
                    user_data.department,
                    user_data.profileimage,
                    user_data.account_type,
                    user_data.gender,
                    user_data.mail,
                    user_data.title,
                    id_number,
                ))
                connection.commit()
                return True
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_user_with_id(self, id_number):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_id = %s )"""
            cursor.execute(query,(id_number,))
            try:
                User = cursor.fetchone()
                User = Person(User[0], User[1], User[2], User[3], User[4], User[5], User[6], User[8], User[7],activated=User[9])
                connection.commit()
                return User
            except:
                return None

    def get_user(self, user_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT * FROM USERS WHERE (user_name = %s )"""
            cursor.execute(query,(user_name,))
            try:
                User = cursor.fetchone()
                User = Person(User[0], User[1], User[2], User[3], User[4], User[5], User[6], User[8], User[7], activated=User[9], most_viewed_video=User[10])
                connection.commit()
                return User
            except:
                return None


    def get_all_users(self):
        user_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""SELECT 
                users.user_id, 
                users.user_name, 
                department.department_name,
                users.account_type,
                users.gender,
                users.mail,
                users.title,
                users.profile_image_path,
                users.activated
            FROM USERS 
            INNER JOIN DEPARTMENT 
            ON (users.department = department.department_code)
            WHERE (users.account_type != 'admin')
            """
            cursor.execute(query)
            try:
                users = cursor.fetchall()

                for User in users:

                    User = Person(
                        id_number=User[0],
                        username=User[1],
                        password=None,
                        department=User[2],
                        account_type=User[3],
                        gender=User[4],
                        mail=User[5],
                        title=User[6],
                        profileimage=User[7],
                        activated=User[8]
                    )
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

    def create_department(self,department):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO DEPARTMENT (department_code, department_name) VALUES (%s, %s)""",
                    (department.department_code, department.department_name))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def delete_department(self,department_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """DELETE FROM DEPARTMENT WHERE department_code = %s""",
                    (department_code,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def create_user(self, User):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO USERS (user_id, user_name, password, profile_image_path, department, account_type, gender, mail,most_reviewed_video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)""",
                    (int(User.id_number), User.username, User.password, User.profileimage, User.department,
                     User.account_type, User.gender, User.mail,None,))
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

    def activate_user(self, user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""UPDATE users SET activated = True WHERE user_id = %s""", (user_id,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def create_class(self, nclass):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO Class (class_code, class_name, tutor, review_points, class_context, capacity, number_of_videos,department) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (nclass.class_code, nclass.class_name, nclass.tutor, 0, nclass.class_context, nclass.class_capacity, 0, nclass.department))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Class code exists"

    def delete_class(self,class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""DELETE FROM CLASS WHERE class_code = %s""", (class_code,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_tutors_classes(self, id_number):
        class_list = []
        tutor = ""
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT 
                class.class_name, 
                class.class_code,
                class.review_points,
                class.class_context,
                class.capacity,
                users.user_name,
                department.department_name,
                count(student.class_code),
                users.title
            FROM Class
            JOIN users
            ON users.user_id = class.tutor
            JOIN department
            ON class.department = department.department_code
            LEFT JOIN student
            ON student.class_code = class.class_code
            WHERE (class.tutor = %s)
            GROUP BY class.class_code, users.user_name, department.department_name, users.title
            """
            try:
                cursor.execute(query, (id_number,))
                classes = cursor.fetchall()

                if classes == None:
                    return None, None

                for t_class in classes:
                    nclass = Class(t_class[0], t_class[1], t_class[5], t_class[2], t_class[3], t_class[4], t_class[7],t_class[6])
                    tutor = Person(None, t_class[5], None, t_class[6], None, None, t_class[8])
                    class_list.append(nclass)

                connection.commit()
                return tutor, class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_classes_of_tutor(self, id_number):
        class_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT 
                class.class_name, 
                class.class_code,
                class.review_points,
                class.class_context,
                class.capacity,
                users.user_name,
                count(student.class_code)
            FROM Class
            JOIN users
            ON users.user_id = class.tutor
            LEFT JOIN student
            ON student.class_code = class.class_code
            WHERE (class.tutor = %s)
            GROUP BY class.class_code, users.user_name
            """
            try:
                cursor.execute(query, (id_number,))
                classes = cursor.fetchall()

                for t_class in classes:
                    nclass = Class(t_class[0], t_class[1], t_class[5], t_class[2], t_class[3], t_class[4], t_class[6])

                    class_list.append(nclass)

                connection.commit()
                return class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def search_classes(self,department,tutor,star):
        class_list = []
        tutor_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
                    SELECT
                        class.class_name, 
                        class.class_code,
                        class.review_points,
                        class.class_context,
                        class.capacity,
                        users.user_name,
                        department.department_name,
                        count(student.class_code)
                    FROM Class
                    JOIN users
                    ON users.user_id = class.tutor
                    JOIN department
                    ON class.department = department.department_code
                    LEFT JOIN student
                    ON student.class_code = class.class_code
                    WHERE (%s is null or department.department_code = %s) and
                    (%s is null or users.user_id = %s) and 
                    (%s is null or class.review_points >= %s)
                    GROUP BY class.class_code, users.user_name, department.department_name
                    ORDER BY class.review_points DESC
                    """
            try:
                cursor.execute(query,(department, department, tutor, tutor, star, star))
                classes = cursor.fetchall()
                for t_class in classes:
                    nclass = Class(t_class[0], t_class[1], t_class[5], t_class[2], t_class[3], t_class[4], t_class[7], t_class[6])
                    tutor = Person(None, t_class[5], None, None, None, None, None)
                    class_list.append(nclass)
                    tutor_list.append(tutor)

                connection.commit()
                return tutor_list, class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_all_classes(self):
        class_list = []
        tutor_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT
                class.class_name, 
                class.class_code,
                class.review_points,
                class.class_context,
                class.capacity,
                users.user_name,
                department.department_name,
                count(student.class_code)
            FROM Class
            JOIN users
            ON users.user_id = class.tutor
            JOIN department
            ON class.department = department.department_code
            LEFT JOIN student
            ON student.class_code = class.class_code
            GROUP BY class.class_code, users.user_name, department.department_name 
            """

            try:
                cursor.execute(query)
                classes = cursor.fetchall()
                for t_class in classes:
                    nclass = Class(t_class[0], t_class[1], t_class[5], t_class[2], t_class[3],t_class[4],t_class[7],t_class[6])
                    tutor = Person(None,t_class[5],None,None,None,None,None)
                    class_list.append(nclass)
                    tutor_list.append(tutor)

                connection.commit()
                return tutor_list, class_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)


    def get_class_with_class_code(self,class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT
                class.class_name, 
                class.class_code,
                class.review_points,
                class.class_context,
                class.capacity,
                users.user_name,
                department.department_name,
                count(student.class_code),
                users.profile_image_path,
                users.title
            FROM Class
            JOIN users
            ON users.user_id = class.tutor
            JOIN department
            ON users.department = department.department_code
            LEFT JOIN student
            ON student.class_code = class.class_code
            WHERE class.class_code = %s
            GROUP BY class.class_code, users.user_name, department.department_name, users.profile_image_path, users.title
            """
            try:
                cursor.execute(query, (class_code,))
                classes = cursor.fetchone()
                nclass = Class(classes[0],classes[1],classes[3],classes[2],classes[3],classes[4],classes[7],classes[6])
                tutor = Person(None,classes[5],None,None,None,None,None,classes[9],classes[8])
                connection.commit()
                return nclass, tutor
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
                     video.thumbnail_path, video.video_path, video.video_descriptions, 0))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Video code exists"

    def get_videos(self,class_code):
        video_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT * FROM Video WHERE (class_code = %s)"""
            try:
                cursor.execute(query, (class_code,))
                videos = cursor.fetchall()

                for video in videos:
                    video = Video(video[1],video[0],video[3],video[2],video[8],video[5],video[6],video[7],video[4])
                    video_list.append(video)

                connection.commit()
                return video_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_video_with_video_code(self,video_code):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
            SELECT 
                video.video_name,
                video.video_code,
                users.user_name,
                class.class_name,
                video.review_points,
                video.thumbnail_path,
                video.video_path,
                video.video_descriptions,
                video.comments_available,
                users.profile_image_path
            FROM VIDEO 
            JOIN users
            ON users.user_id = video.tutor
            JOIN class
            ON class.class_code = video.class_code
            WHERE video_code = %s"""
            try:
                cursor.execute(query, (video_code,))
                t_video = cursor.fetchone()

                video = Video(t_video[0],t_video[1],None,t_video[3],t_video[4],t_video[5],t_video[6],t_video[7],t_video[8])
                tutor = Person(None,t_video[2],None,None,None,None,None,None,t_video[9])
                connection.commit()
                return tutor, video
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def create_comment(self,comment):
        if comment.comment_context == None:
            return
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """INSERT INTO comments (comment_id, user_id, video_code, comment_context, time) VALUES (%s, %s, %s, %s, %s)""",
                    (comment.comment_id, comment.user_id, comment.video_code, comment.comment_context, comment.time))
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
                    """SELECT
                     comments.comment_id,
                     users.user_name,
                     users.account_type,
                     users.profile_image_path,
                     video.video_name,
                     comments.comment_context,
                     comments.time
                     FROM comments 
                     INNER JOIN users
                     ON users.user_id = comments.user_id
                     INNER JOIN video
                     ON video.video_code = comments.video_code
                     WHERE video.video_code = %s""", (video_code,)
                )
                comments = cursor.fetchall()
                for comment in comments:
                    comment = Comment(comment[0],comment[1], comment[2],comment[3],comment[4],comment[5],comment[6])
                    comment_list.append(comment)
                connection.commit()

                return comment_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)
                if e.pgcode == 23505:
                    return "Comment code exists"

    def get_all_student(self):
        student_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
                    SELECT user_name, user_id FROM USERS WHERE (account_type = 'Student')"""
            try:
                cursor.execute(query)
                students = cursor.fetchall()

                for student in students:
                    student = Person(student[1],student[0],None,None,"Student",None,None)
                    student_list.append(student)

                connection.commit()
                return student_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def get_all_students_from_class(self,class_code):
        student_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT 
                    users.user_name,
                    users.user_id,
                    users.profile_image_path
                FROM student
                JOIN users
                ON users.user_id = student.student_id
                WHERE (class_code = %s)"""
            try:
                cursor.execute(query,(class_code,))
                students = cursor.fetchall()

                for student in students:
                    student = Person(student[1], student[0], None, None, "Student", None, None,None,student[2])
                    student_list.append(student)

                connection.commit()
                return student_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def delete_student_from_class(self, class_code, student_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""DELETE FROM STUDENT WHERE class_code = %s AND student_id = %s""", (class_code, student_id,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def check_if_student_in_the_class(self,class_code,student_id):
        if class_code == None:
            return False

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""
                        SELECT 
                            (student_id)
                        FROM student
                        WHERE (class_code = %s AND student_id = %s)"""
            try:
                cursor.execute(query,(class_code, student_id,))
                user_id = cursor.fetchall()
                for user in user_id:
                    if user[0] == student_id:
                        return True
                    else:
                        return False

            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def add_student(self, user_ids, class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""INSERT INTO STUDENT (class_code, student_id) VALUES(%s,%s)"""
            try:
                for user_id in user_ids:
                    cursor.execute(query,(class_code, user_id,))

                connection.commit()

            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def update_capacity_of_a_class(self,class_code,capacity):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = f"""UPDATE CLASS SET capacity = %s WHERE class_code= %s"""
            try:

                cursor.execute(query,(capacity, class_code,))

                connection.commit()

            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def add_review_point(self, review_point, video_code, user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query1 = """
                SELECT 
                video.review_points, 
                video.number_of_reviews,
                video.class_code
                FROM video
                JOIN class
                ON video.class_code = class.class_code
                WHERE video_code = %s
                GROUP BY video.review_points, video.number_of_reviews, video.class_code, class.review_points"""
            query2 = """UPDATE video SET review_points = %s, number_of_reviews = %s WHERE video_code = %s"""
            query3 = """INSERT INTO reviews(video_code, user_id, reviewed, given_point) VALUES (%s, %s, %s, %s) """
            try:
                cursor.execute(query1, (video_code,))
                data = cursor.fetchone()
                review_points = data[0] * data[1]
                number_of_reviews = data[1]
                review_points = review_points + int(review_point)
                number_of_reviews += 1
                review_points /= number_of_reviews
                cursor.execute(query2, ("{:.2f}".format(review_points),number_of_reviews,video_code,))
                cursor.execute(query3, (video_code, user_id, True,review_point))
                connection.commit()
                self.update_class_review(data[2])

            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def update_class_review(self,class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query1 ="""SELECT SUM(review_points), count(review_points) FROM video WHERE class_code = %s"""
            query2 = """UPDATE class SET review_points = %s WHERE class_code = %s"""
            try:
                cursor.execute(query1, (class_code,))
                data = cursor.fetchone()
                rev = data[0] / data[1]
                cursor.execute(query2, (rev, class_code,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def check_student_in_class(self,user_id,class_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """select exists(select student_id from student where class_code = %s and student_id = %s)"""
            try:
                cursor.execute(query, (class_code,user_id,))
                trueorfalse = cursor.fetchone()
                return trueorfalse[0]
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)


    def get_tutors(self):
        tutor_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """
            SELECT
            users.user_name,
            users.user_id,
            department.department_name,
            users.mail,
            users.profile_image_path,
            users.activated
            FROM users
            JOIN department
            ON users.department = department.department_code
            WHERE users.account_type = 'Tutor'
            """
            try:
                cursor.execute(query)
                tutors = cursor.fetchall()
                for t_tutor in tutors:
                    tutor = Person(t_tutor[1],t_tutor[0],None,t_tutor[2],'Tutor',None,t_tutor[3],None,t_tutor[4],t_tutor[5])
                    tutor_list.append(tutor)

                return tutor_list
            except dbapi2.Error as e:
                print(e.pgcode, e.pgerror)

    def delete_video(self, video_code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM video WHERE video_code = %s"""
            try:
                cursor.execute(query, (video_code,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def update_class_with_class_code(self,class_code,new_class_data):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """
            UPDATE class
            SET 
            class_name = COALESCE(%s, class_name),
            class_code = COALESCE(%s, class_code),
            class_context = COALESCE(%s, class_context)
            WHERE class_code = %s
            """

            try:
                cursor.execute(query, (new_class_data.class_name,
                                       new_class_data.class_code,
                                       new_class_data.class_context,
                                       class_code,
                                       ))
                connection.commit()
                return True
            except dbapi2.Error as e:
                print(e.pgerror)

    def update_video_with_video_code(self, video_code, new_video_data):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """
            UPDATE video
            SET 
            video_name = COALESCE(%s, video_name),
            class_code = COALESCE(%s, class_code),
            comments_available = %s,
            thumbnail_path = COALESCE(%s, thumbnail_path),
            video_path = COALESCE(%s, video_path),
            video_descriptions = COALESCE(%s, video_descriptions)        
            WHERE video_code = %s
            """

            try:
                cursor.execute(query, (new_video_data.video_name,
                                       new_video_data.class_code,
                                       new_video_data.comments_available,
                                       new_video_data.thumbnail_path,
                                       new_video_data.video_path,
                                       new_video_data.video_descriptions,
                                       video_code,
                                       ))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)


    def check_video_reviewed(self, video_code, user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = """
            SELECT reviewed 
            FROM REVIEWS
            WHERE video_code = %s and user_id = %s
            """

            try:
                cursor.execute(query, (video_code, user_id,))
                reviewed = cursor.fetchone()
                if reviewed is None:
                    return False
                connection.commit()
                return reviewed[0]
            except dbapi2.Error as e:
                print(e.pgerror)

    def update_most_reviewed_video(self, tutor_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query1 = """
            UPDATE users
            SET most_reviewed_video = %s 
            WHERE user_id = %s
            """
            query2 = """
            SELECT DISTINCT ON (review_points) video_code from video WHERE tutor = %s ORDER BY review_points DESC;;
            """
            try:
                cursor.execute(query2, (tutor_id,))
                reviewed_video = cursor.fetchone()
                if reviewed_video != None:
                    cursor.execute(query1, (reviewed_video[0], tutor_id,))
                else:
                    cursor.execute(query1, (None, tutor_id,))
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_most_viewed_video(self,most_viewed_video):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query="""
                SELECT
                 * FROM 
                 video 
                 WHERE video_code = %s
            """
            try:
                if most_viewed_video == None:
                    return None
                cursor.execute(query, (most_viewed_video,))
                t_video = cursor.fetchone()
                video = Video(t_video[1],t_video[0],t_video[3],t_video[2],t_video[8],t_video[5],t_video[6],t_video[4],t_video[7])
                return video
                connection.commit()
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_students_classes(self, user_id):
        class_list = []
        tutor_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query="""
                SELECT
                class.class_name, 
                class.class_code,
                class.review_points,
                class.class_context,
                class.capacity,
                users.user_name,
                department.department_name,
                count(student.class_code)
            FROM Class
            JOIN users
            ON users.user_id = class.tutor
            JOIN department
            ON class.department = department.department_code
            LEFT JOIN student
            ON student.class_code = class.class_code
            WHERE student.student_id = %s
            GROUP BY class.class_code, users.user_name, department.department_name
            """
            try:
                cursor.execute(query, (user_id,))
                classes = cursor.fetchall()

                if classes == None:
                    return None, None

                for t_class in classes:
                    nclass = Class(t_class[0],t_class[1],None,t_class[2],t_class[3],t_class[4],t_class[7],t_class[6])
                    tutor = Person(None,t_class[5], None, None, None, None, None)
                    class_list.append(nclass)
                    tutor_list.append(tutor)
                connection.commit()
                return tutor_list, class_list
            except dbapi2.Error as e:
                print(e.pgerror)

    def get_student_comments(self,student_id):
        video_list = []
        comment_list = []
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query="""
                SELECT
                    video.video_name,
                    video.video_code,
                    video.class_code,
                    reviews.given_point,
                    video.thumbnail_path,
                    array_agg('[' || comm.comment_context || ', ' || comm.time || ']') as comments
                    from (SELECT comments.comment_context, comments.video_code, comments.time, users.user_id FROM comments
                    JOIN users
                    ON comments.user_id = users.user_id
                    WHERE comments.user_id = %s) as comm
                    JOIN video
                    ON video.video_code = comm.video_code
                    JOIN users
                    ON comm.user_id = users.user_id
                    JOIN reviews
                    ON video.video_code = reviews.video_code and users.user_id = reviews.user_id
                    GROUP BY video.video_name, video.video_code, video.thumbnail_path, reviews.given_point
            """
            try:
                cursor.execute(query, (student_id,))
                comments = cursor.fetchall()

                for comment in comments:
                    for t_comm in comment[5]:
                        ncomm = t_comm.strip('][').split(', ')
                        comm = Comment(None,None,None,None,comment[1],ncomm[0],ncomm[1])

                        comment_list.append(comm)
                    video = Video(comment[0],comment[1],None,comment[2],comment[3],comment[4],None,comment_list=comment_list)
                    video_list.append(video)
                    comment_list = []

                connection.commit()
                return video_list
            except dbapi2.Error as e:
                print(e.pgerror)

    def check_if_department_exists(self, department):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query1 ="""select exists(select department_code from department where department_code = %s)"""
            query2 ="""select exists(select department_name from department where department_name = %s)"""
            try:
                cursor.execute(query1, (department.department_code,))
                exist1 = cursor.fetchone()
                cursor.execute(query2, (department.department_name,))
                exist2 = cursor.fetchone()
                print(exist2[0])
                return exist1[0], exist2[0]
            except dbapi2.Error as e:
                print(e.pgerror)

def get_User(user_name):
    user = current_app.config["db"].get_user(user_name)
    return user