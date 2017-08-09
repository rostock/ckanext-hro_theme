# encoding: utf-8
import routes.mapper
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import os
import sys


class Hro_ThemePlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.ITranslation)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'hro_theme')

    def before_map(self, route_map):
        with routes.mapper.SubMapper(route_map,
                controller='ckanext.hro_theme.plugin:Hro_ThemeController') as m:
            m.connect('api_info', '/api_info', action='api_info')
            m.connect('imprint', '/imprint', action='imprint')
            m.connect('privacy_policy', '/privacy_policy', action='privacy_policy')
            m.connect('terms_of_use', '/terms_of_use', action='terms_of_use')
        return route_map

    def after_map(self, route_map):
        return route_map
    
    def i18n_directory(self):
        '''Change the directory of the *.mo translation files
        The default implementation assumes the plugin is
        ckanext/myplugin/plugin.py and the translations are stored in
        i18n/
        '''
        # assume plugin is called ckanext.<myplugin>.<...>.PluginClass
        extension_module_name = '.'.join(self.__module__.split('.')[:3])
        module = sys.modules[extension_module_name]
        return os.path.join(os.path.dirname(module.__file__), 'i18n')

    def i18n_locales(self):
        '''Change the list of locales that this plugin handles
        By default the will assume any directory in subdirectory in the
        directory defined by self.directory() is a locale handled by this
        plugin
        '''
        directory = self.i18n_directory()
        return [ d for
                 d in os.listdir(directory)
                 if os.path.isdir(os.path.join(directory, d))
        ]

    def i18n_domain(self):
        '''Change the gettext domain handled by this plugin
        This implementation assumes the gettext domain is
        ckanext-{extension name}, hence your pot, po and mo files should be
        named ckanext-{extension name}.mo'''
        return 'ckanext-{name}'.format(name=self.name)


class Hro_ThemeController(base.BaseController):

    def api_info(self):
        return base.render('home/api_info.html')

    def imprint(self):
        return base.render('home/imprint.html')

    def privacy_policy(self):
        return base.render('home/privacy_policy.html')

    def terms_of_use(self):
        return base.render('home/terms_of_use.html')