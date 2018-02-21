# Extension for *CKAN*: HRO theme

A custom theme for OpenData.HRO, the open data portal of the municipality of Rostock – view it in production: https://www.opendata-hro.de

## Requirements

*   [*CKAN*](https://ckan.org) >= 2.7.0

## Installation

To install ckanext-hro_theme for production:

1.  Activate your *CKAN* virtual *Python* environment, for example:

        . /usr/lib/ckan/default/bin/activate

1.  Install the ckanext-hro_theme *Python* package into your virtual *Python* environment:

        pip install ckanext-hro_theme

1.  Add `hro_theme` to the `ckan.plugins` setting in your *CKAN* config file (by default the config file is located at `/etc/ckan/default/production.ini`)
1.  Restart *CKAN*. For example, if you have deployed *CKAN* with *Apache HTTP Server* on *Ubuntu*:

        sudo service apache2 reload

## Development installation

To install ckanext-hro_theme for development, activate your *CKAN* virtualenv and do:

    git clone https://github.com/kvlahrosch/ckanext-hro_theme.git
    cd ckanext-hro_theme
    python setup.py develop
    pip install -r dev-requirements.txt

## Translation

1.  Create or update the file `ckanext/hro_theme/i18n/ckanext-hro_theme.pot` by extracting all translatable strings into it:

        cd ckanext-hro_theme
        python setup.py extract_messages

1.  If necessary, create a new translation for your language – this will generate a new directory `ckanext/hro_theme/i18n/YOUR_LANGUAGE` with a `LC_MESSAGES/ckanext-hro_theme.po` file containing all the untranslated strings:

        python setup.py init_catalog --locale <YOUR_LANGUAGE>
    
1.  Start editing either the new `po` file you created before or one of the existing `po` files:

        msgid "This is an untranslated string!"
        msgstr "This is a translated string!"
        
1.  Compile the updated `po` file(s) – this will generate the required `mo` file(s):

        python setup.py compile_catalog
