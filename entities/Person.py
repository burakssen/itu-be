from flask_login import UserMixin

class Person(UserMixin):
    def __init__(self, id_number, username, password, department, account_type, gender, mail, title=None, profileimage=None):
        self.id = id_number
        self.active = True
        self.profileimage = profileimage
        self.title = title
        self.set_user(username, id_number, mail, account_type, gender, department, title, password)
        self.logged_in = False

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return self.username

    def convert_image_path(self):
        image_path = self.profileimage
        self.profileimage = image_path.replace("./itu-be", "../..")

    def set_user(self, username=None, id_number=None, mail=None, account_type=None, gender=None, department=None, title=None, password=None):
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

        if title is not None:
            self.title = title

        if gender is not None:
            self.gender = gender
            if self.profileimage is None:
                if self.gender == "Male":
                    self.profileimage = "../static/profile_images/boy.png"
                else:
                    self.profileimage = "../static/profile_images/girl.png"

        if department is not None:
            self.department = department


    def set_profile_image(self):
        if self.gender == "Male":
            self.profileimage = "../static/profile_images/boy.png"
        else:
            self.profileimage = "../static/profile_images/girl.png"
