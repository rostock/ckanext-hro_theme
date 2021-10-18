# Extension for *CKAN*: HRO-theme

A custom theme for OpenData.HRO, the open data portal of the municipality of Rostock – view it in production: https://www.opendata-hro.de

## Requirements

[*CKAN*](https://github.com/ckan/ckan)

## Installation

1.  Activate your *CKAN* virtual *Python* environment, for example:

        . /usr/lib/ckan/default/bin/activate

1.  Install *HRO-theme* into your virtual *Python* environment:

        pip install -e 'git+https://github.com/rostock/ckanext-hro_theme.git#egg=ckanext-hro_theme'

1.  Add `hro_theme` to the `ckan.plugins` setting in your *CKAN* config file (by default the config file is located at `/etc/ckan/default/ckan.ini`)
1.  Restart *CKAN*. For example, if you have deployed *CKAN* with *Apache HTTP Server* on *Ubuntu*:

        sudo service apache2 reload

## Upgrade

1.  Activate your *CKAN* virtual *Python* environment, for example:

        . /usr/lib/ckan/default/bin/activate

1.  Upgrade *HRO-theme* within your virtual *Python* environment:

        pip install --upgrade -e 'git+https://github.com/rostock/ckanext-hro_theme.git#egg=ckanext-hro_theme'

1.  Restart *CKAN*. For example, if you have deployed *CKAN* with *Apache HTTP Server* on *Ubuntu*:

        sudo service apache2 reload

## Translation

1.  Create or update the file `ckanext/hro_theme/i18n/ckanext-hro_theme.pot` by extracting all translatable strings into it:

        cd /usr/lib/ckan/default/src/ckanext-hro-theme
        python setup.py extract_messages

1.  If necessary, create a new translation for your language – this will generate a new directory `ckanext/hro_theme/i18n/YOUR_LANGUAGE` with a `LC_MESSAGES/ckanext-hro_theme.po` file containing all the untranslated strings:

        python setup.py init_catalog --locale <YOUR_LANGUAGE>
    
1.  Start editing either the new `po` file you created before or one of the existing `po` files:

        msgid "This is an untranslated string!"
        msgstr "This is a translated string!"
        
1.  Compile the updated `po` file(s) – this will generate the required `mo` file(s):

        python setup.py compile_catalog
