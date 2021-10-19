# encoding: utf-8
import datetime
import os
import pytz
import re
import routes.mapper
import sys
import tzlocal
import ckan.lib.formatters as formatters
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from datetime import timedelta
from ckan.common import config
from flask import Blueprint


hro_theme = Blueprint('hro_theme', __name__)


# function taken from CKAN, kept untouched
def get_display_timezone():
    timezone_name = config.get('ckan.display_timezone') or 'utc'

    if timezone_name == 'server':
        return tzlocal.get_localzone()

    return pytz.timezone(timezone_name)

# function taken from CKAN and slightly adjusted to support UTC offset in the ISO-like formatted datestring
def date_str_to_datetime(date_str):
    utc_offset = None
    m = re.search('([\+-]\d{2}:\d{2}$)', date_str)
    if m:
        utc_offset = m.group(1)
        date_str = re.sub('[\+-]\d{2}:\d{2}$', '', date_str)
    
    time_tuple = re.split('[^\d]+', date_str, maxsplit=5)

    if len(time_tuple) >= 6:
        m = re.match('(?P<seconds>\d{2})(\.(?P<microseconds>\d{6}))?$',
                     time_tuple[5])
        if not m:
            raise ValueError('Unable to parse %s as seconds.microseconds' %
                             time_tuple[5])
        seconds = int(m.groupdict().get('seconds'))
        microseconds = int(m.groupdict(0).get('microseconds'))
        time_tuple = time_tuple[:5] + [seconds, microseconds]

    if utc_offset is None:
        return datetime.datetime(*map(int, time_tuple))
    else:
        datetime_to_return = datetime.datetime(*map(int, time_tuple))
        if utc_offset[0] == '+':
            datetime_to_return -= timedelta(hours=int(utc_offset[1:3]), minutes=int(utc_offset[4:]))
        elif utc_offset[0] == '-':
            datetime_to_return += timedelta(hours=int(utc_offset[1:3]), minutes=int(utc_offset[4:]))        
        return datetime_to_return

# function taken from CKAN, kept untouched
def _datestamp_to_datetime(datetime_):
    if isinstance(datetime_, (str,bytes)):
        try:
            datetime_ = date_str_to_datetime(datetime_)
        except TypeError:
            return None
        except ValueError:
            return None

    if not isinstance(datetime_, datetime.datetime):
        return None

    if datetime_.tzinfo is not None:
        return datetime_

    datetime_ = datetime_.replace(tzinfo=pytz.utc)
    datetime_ = datetime_.astimezone(get_display_timezone())

    return datetime_

# function taken from CKAN, kept untouched
def render_datetime(datetime_, date_format=None, with_hours=False):
    datetime_ = _datestamp_to_datetime(datetime_)
    if not datetime_:
        return ''

    if date_format:

        if datetime_.year < 1900:
            year = str(datetime_.year)

            date_format = re.sub('(?<!%)((%%)*)%y',
                                 r'\g<1>{year}'.format(year=year[-2:]),
                                 date_format)
            date_format = re.sub('(?<!%)((%%)*)%Y',
                                 r'\g<1>{year}'.format(year=year),
                                 date_format)

            datetime_ = datetime.datetime(2016, datetime_.month, datetime_.day,
                                          datetime_.hour, datetime_.minute,
                                          datetime_.second)

            return datetime_.strftime(date_format)

        return datetime_.strftime(date_format)

    return formatters.localised_nice_date(datetime_, show_date=True,
                                          with_hours=with_hours)

# custom function
def _int_string_to_int(int_string):
    try:
        ints = re.findall('\d', int_string)
        if ints is not None:
            int_ = ''
            for item in ints:
                int_ += item
        else:
            return None
    except TypeError:
        return None
    except ValueError:
        return None
    return int(int_)

# custom function
def render_size(size_string, raw=False):
    size_ = _int_string_to_int(size_string)
    if not size_:
        return ''
    if raw:
        return str(size_)
    else:
        if size_ >= 1073741824:
            return str(round(size_ / 1073741824)) + ' GiB (' + str(round(size_ / 1000000000)) + ' GB)'
        elif size_ >= 1000000000:
            return str(round(size_ / 1048576)) + ' MiB (' + str(round(size_ / 1000000000)) + ' GB)'
        elif size_ >= 1048576:
            return str(round(size_ / 1048576)) + ' MiB (' + str(round(size_ / 1000000)) + ' MB)'
        elif size_ >= 1000000:
            return str(round(size_ / 1024)) + ' KiB (' + str(round(size_ / 1000000)) + ' MB)'
        elif size_ >= 1024:
            return str(round(size_ / 1024)) + ' KiB (' + str(round(size_ / 1000)) + ' kB)'
        elif size_ >= 1000:
            return str(round(size_)) + ' Bytes (' + str(round(size_ / 1000)) + ' kB)'
        else:
            return str(round(size_)) + ' Bytes'


def api_info():
    return toolkit.render('home/api_info.html')

def imprint():
    return toolkit.render('home/imprint.html')

def privacy_policy():
    return toolkit.render('home/privacy_policy.html')

def terms_of_use():
    return toolkit.render('home/terms_of_use.html')

hro_theme.add_url_rule('/api_info', view_func=api_info, endpoint='api_info')
hro_theme.add_url_rule('/imprint', view_func=imprint, endpoint='imprint')
hro_theme.add_url_rule('/privacy_policy', view_func=privacy_policy, endpoint='privacy_policy')
hro_theme.add_url_rule('/terms_of_use', view_func=terms_of_use, endpoint='terms_of_use')


class Hro_ThemePlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public', 'ckanext-hro_theme')

    def get_blueprint(self):
        return hro_theme

    def get_helpers(self):
        return {
            'hro_theme_render_datetime': render_datetime,
            'hro_theme_render_size': render_size
        }
    
    def i18n_directory(self):
        extension_module_name = '.'.join(self.__module__.split('.')[:3])
        module = sys.modules[extension_module_name]
        return os.path.join(os.path.dirname(module.__file__), 'i18n')

    def i18n_locales(self):
        directory = self.i18n_directory()
        return [ d for
                 d in os.listdir(directory)
                 if os.path.isdir(os.path.join(directory, d))
        ]

    def i18n_domain(self):
        return 'ckanext-{name}'.format(name=self.name)
