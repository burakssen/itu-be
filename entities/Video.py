from tools.utils import get_project_root

class Video():
    def __init__(self, video_name, video_code, tutor, class_code, review_points, thumbnail_path, video_path,
                 video_descriptions=None, comments_available=True ):
        self.video_name = video_name
        self.video_code = video_code
        self.tutor = tutor
        self.class_code = class_code
        self.review_points = review_points
        self.thumbnail_path = thumbnail_path
        self.video_path = video_path
        self.comments_available = comments_available
        self.video_descriptions = video_descriptions

    def convert_image_path(self):
        temp = str(get_project_root())
        temp = temp.replace("\\","/")
        self.thumbnail_path = self.thumbnail_path.replace(temp,"")

    def convert_video_path(self):
        temp = str(get_project_root())
        temp = temp.replace("\\","/")
        self.video_path = self.video_path.replace(temp,"")