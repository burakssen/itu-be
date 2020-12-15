class Class():
    def __init__(self,className,classCode,tutor,videoList,department,review_point):
        self.className = className
        self.classCode = classCode
        self.tutor = tutor
        self.videoList = videoList
        self.department = department
        self.review_point = review_point

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