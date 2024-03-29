from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, ValidationError

"""
class VideoSubmitForm(FlaskForm):
    def validate_video_url(self, url_to_check):
        if not (url_to_check.data.startswith('https://www.youtube.com/')
                or url_to_check.data.startswith('https://youtu.be/')):
            raise ValidationError('URL is invalid. Please make sure it is a valid YouTube URL.')

    video_url = StringField(label='Video URL:', validators=[Length(min=2, max=100), DataRequired()])
    submit_video_link = SubmitField(label='Select video')
"""

"""
class VideoDownloadForm(FlaskForm):
    video_format = SelectField(label="Video format:")
    submit2 = SubmitField(label='Download video')
"""