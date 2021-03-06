class Video():
    def __init__(self, video_name, video_code, tutor, class_code, review_points, thumbnail_path, video_path,
                 video_descriptions=None, comments_available=True , comment_list=None):
        self.video_name = video_name
        self.video_code = video_code
        self.tutor = tutor
        self.class_code = class_code
        self.review_points = review_points
        self.thumbnail_path = thumbnail_path
        self.video_path = video_path
        self.comments_available = comments_available
        self.video_descriptions = video_descriptions
        self.comment_list = comment_list

    def convert_image_path(self):
        self.thumbnail_path = self.thumbnail_path.replace("\\","/")

    def convert_video_path(self):
        self.video_path = self.video_path.replace("\\","/")