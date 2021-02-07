from collections import OrderedDict

APP_SLOGAN = 'Some Sort of Slogan'
APP_NAME = 'App Name'

ITEM_PER_PAGE = 25

SEX_TYPES = {
    0: 'Select',
    1: 'Male',
    2: 'Female',
    3: 'Other'
}
SEX_TYPES = OrderedDict(sorted(SEX_TYPES.items()))

DATE_DISPLAY_FORMATS = {
    0: {
        'title': '',
        'format': ''
    },
    1:  {
        'title': '',
        'format': ''
    },
    2:  {
        'title': '',
        'format': ''
    }
}
DATE_DISPLAY_FORMATS = OrderedDict(sorted(DATE_DISPLAY_FORMATS.items()))

USER_STATES = {
    0: 'New',
    1: 'Confirmed',
    2: 'Verified'
}
USER_STATES = OrderedDict(sorted(USER_STATES.items()))

USER_ACCOUNT_STATE = {
    0: 'Active',
    1: 'Not-Active'
}
USER_ACCOUNT_STATE = OrderedDict(sorted(USER_ACCOUNT_STATE.items()))
