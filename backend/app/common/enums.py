from enum import Enum


class Gender(str, Enum):

    MALE = "male"

    FEMALE = "female"


class NotificationType(str, Enum):

    JOB = "job"

    EVENT = "event"

    POST = "post"

    MENTORSHIP = "mentorship"