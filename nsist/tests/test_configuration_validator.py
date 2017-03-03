import configparser
import os

from nose.tools import *

from .. import configreader
from .. import get_installer_builder_args


DATA_FILES = os.path.join(os.path.dirname(__file__), 'data_files')

def test_valid_config():
    configfile = os.path.join(DATA_FILES, 'valid_config.cfg')
    config = configreader.read_and_validate(configfile)
    print(config['Application'])
    print('Application' in config)
    print(config.has_section('Application'))
    # assert False

def test_valid_config_with_shortcut():
    configfile = os.path.join(DATA_FILES, 'valid_config_with_shortcut.cfg')
    config = configreader.read_and_validate(configfile)

def test_valid_config_with_values_starting_on_new_line():
    configfile = os.path.join(DATA_FILES, 'valid_config_value_newline.cfg')
    config = configreader.read_and_validate(configfile)
    sections = ('Application', 'Python', 'Include', 'Build')
    assert len(config.sections()) == len(sections)
    for section in sections:
        assert section in config
        assert config.has_section(section)

    assert config.get('Application', 'name') == '\nMy App'
    assert config.get('Application', 'version') == '\n1.0'
    assert config.get('Application', 'publisher') == '\nTest'
    assert config.get('Application', 'entry_point') == '\nmyapp:main'
    assert config.get('Application', 'icon') == '\nmyapp.ico'

    assert config.get('Python', 'version') == '\n3.6.0'
    assert config.get('Python', 'bitness') == '\n64'
    assert config.get('Python', 'format') == '\nbundled'
    assert config.get('Python', 'include_msvcrt') == '\nTrue'

    assert config.get('Build', 'directory') == '\nbuild/'
    assert config.get('Build', 'nsi_template') == '\ntemplate.nsi'

    assert config.get('Include', 'packages') == '\nrequests\nbs4'
    assert config.get('Include', 'pypi_wheels') == '\nhtml5lib'
    assert config.get('Include', 'exclude') == '\nsomething'
    assert config.get('Include', 'files') == '\nLICENSE\ndata_files/'

    args = get_installer_builder_args(config)
    assert args['appname'] == 'My App'
    assert args['version'] == '1.0'
    assert args['publisher'] == 'Test'
    # assert args['entry_point'] == '\nmyapp:main'
    assert args['icon'] == 'myapp.ico'

    assert args['py_version'] == '3.6.0'
    assert args['py_bitness'] == 64
    assert args['py_format'] == 'bundled'
    assert args['inc_msvcrt'] == True

    assert args['build_dir'] == 'build/'
    assert args['nsi_template'] == 'template.nsi'

    assert args['packages'] == ['requests', 'bs4']
    assert args['pypi_wheel_reqs'] == ['html5lib']
    assert args['exclude'] == ['something']
    assert args['extra_files'] == [('', '$INSTDIR'),
                                    ('LICENSE', '$INSTDIR'),
                                    ('data_files/', '$INSTDIR')]

@raises(configreader.InvalidConfig)
def test_invalid_config_keys():
    configfile = os.path.join(DATA_FILES, 'invalid_config_section.cfg')
    configreader.read_and_validate(configfile)

@raises(configreader.InvalidConfig)
def test_invalid_config_key():
    configfile = os.path.join(DATA_FILES, 'invalid_config_key.cfg')
    configreader.read_and_validate(configfile)

@raises(configreader.InvalidConfig)
def test_missing_config_key():
    configfile = os.path.join(DATA_FILES, 'missing_config_key.cfg')
    configreader.read_and_validate(configfile)

@raises(configparser.Error)
def test_invalid_config_file():
    configfile = os.path.join(DATA_FILES, 'not_a_config.cfg')
    configreader.read_and_validate(configfile)
