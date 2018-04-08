from datetime import timezone
from dateutil import parser


def datetime_utc(value):
    return parser.parse(value).replace(tzinfo=timezone.utc)
