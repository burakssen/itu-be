class Person():
    def __init__(self,username,account_type,gender,faculty):
        self.set_user(username,account_type,gender,faculty)

    def set_user(self, username=None,account_type=None,gender=None,faculty=None):
        if username:
            self.username = username
        
        if account_type:
            self.account_type = account_type
        
        if gender:
            self.gender = gender
            if self.gender == "Male":
                self.profileimage = "../static/profile_images/boy.png"
            else:
                self.profileimage = "../static/profile_images/girl.png"
        
        if faculty:
            self.faculty = faculty
