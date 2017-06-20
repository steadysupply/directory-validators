from urllib import parse

from django.conf import settings
from django.core.validators import ValidationError

from directory_validators import helpers
from directory_validators import constants

KEYWORD_LIMIT = 'Please choose no more than 10 keywords.'
KEYWORD_SPECIAL_CHARS = 'Please remove punctuation.'
MESSAGE_FILE_TOO_BIG = 'File is too big.'
MESSAGE_NOT_FACEBOOK = 'Please provide a link to Facebook.'
MESSAGE_NOT_TWITTER = 'Please provide a link to Twitter.'
MESSAGE_NOT_LINKEDIN = 'Please provide a link to LinkedIn.'
MESSAGE_INVALID_IMAGE_FORMAT = (
    'Invalid image format, allowed formats: {}'.format(
        ', '.join(constants.ALLOWED_IMAGE_FORMATS)
    )
)


def keywords_word_limit(keywords):
    """
    Confirms that the number of keywords selected is less than the allowed max.

    Args:
        keywords (str)

    Raises:
        django.forms.ValidationError

    """

    if len(helpers.tokenize_keywords(keywords)) > 10:
        raise ValidationError(KEYWORD_LIMIT)


def keywords_special_characters(keywords):
    """
    Confirms that the keywords don't contain special characters

    Args:
        keywords (str)

    Raises:
        django.forms.ValidationError
    """
    invalid_chars = '!\"#$%&\'()*+-./:;<=>?@[\\]^_{|}~\t\n'
    if any(char in invalid_chars for char in keywords):
        raise ValidationError(KEYWORD_LIMIT)


def image_format(value):
    """
    Confirms that the uploaded image is of supported format.

    Args:
        value (File): The file with an `image` property containing the image

    Raises:
        django.forms.ValidationError

    """

    if value.image.format.upper() not in constants.ALLOWED_IMAGE_FORMATS:
        raise ValidationError(MESSAGE_INVALID_IMAGE_FORMAT)


def case_study_image_filesize(value):
    """
    Confirms that the case study image is not too large in terms of file size.

    Args:
        value (File): The case study image.

    Raises:
        django.forms.ValidationError

    """

    if value.size > settings.VALIDATOR_MAX_CASE_STUDY_IMAGE_SIZE_BYTES:
        raise ValidationError(MESSAGE_FILE_TOO_BIG)


def case_study_video_filesize(value):
    """
    Confirms that the case study video is not too large in terms of file size.

    Args:
        value (File): The case study video.

    Raises:
        django.forms.ValidationError

    """

    if value.size > settings.VALIDATOR_MAX_CASE_STUDY_VIDEO_SIZE_BYTES:
        raise ValidationError(MESSAGE_FILE_TOO_BIG)


def case_study_social_link_facebook(value):
    """
    Confirms that the social media url is pointed at the correct domain.

    Args:
        value (string): The url to check.

    Raises:
        django.forms.ValidationError

    """

    parsed = parse.urlparse(value.lower())
    if not parsed.netloc.endswith('facebook.com'):
        raise ValidationError(MESSAGE_NOT_FACEBOOK)


def case_study_social_link_twitter(value):
    """
    Confirms that the social media url is pointed at the correct domain.

    Args:
        value (string): The url to check.

    Raises:
        django.forms.ValidationError

    """

    parsed = parse.urlparse(value.lower())
    if not parsed.netloc.endswith('twitter.com'):
        raise ValidationError(MESSAGE_NOT_TWITTER)


def case_study_social_link_linkedin(value):
    """
    Confirms that the social media url is pointed at the correct domain.

    Args:
        value (string): The url to check.

    Raises:
        django.forms.ValidationError

    """

    parsed = parse.urlparse(value.lower())
    if not parsed.netloc.endswith('linkedin.com'):
        raise ValidationError(MESSAGE_NOT_LINKEDIN)
