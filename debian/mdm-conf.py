#!/usr/bin/env python

# Simple helper to add settings to MDM.
#


import os
import sys
import argparse
import ConfigParser

settings_file = "/etc/mdm/mdm.conf"


def get_settings():
    """
    Returns a dict with the settings.
    params: nil
    return: dict
    """
    settings_dict = {}

    config = ConfigParser.ConfigParser()
    config.readfp(open(settings_file))

    for sect in config.sections():
        if sect not in settings_dict.keys():
            settings_dict[sect] = {}

        for opt in config.options(sect):
            if opt not in settings_dict[sect].keys():
                try:
                    settings_dict[sect][opt] = config.get(sect, opt)
                except:
                    settings_dict[sect][opt] = None

    return settings_dict


def set_settings(section, values):
    """
    Sets a section with a tuple.
    params: str, list of tuples
    return: nil
    """
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(settings_file)

    for key, value in values:
        try:
            config.set(section, key, value)

        except ConfigParser.NoSectionError:
            config.add_section(section)
            config.set(section, key, value)

    with open(settings_file, 'wb') as configfile:
        config.write(configfile)


def set_daemon_section(default_username="alumno"):
    """
    Sets the default daemon settings
    params: str
    return: nil
    """
    set_settings('daemon',
                 [('Greeter', '/usr/lib/mdm/mdmwebkit'),
                  ('DefaultSession', 'mate.desktop'),
                  ('AutomaticLoginEnable', 'true'),
                  ('AutomaticLogin', default_username),
                  ])


def default_settings():
    """
    Sets the default settings
    params: str
    return: nil
    """
    set_daemon_section()
    set_settings('greeter', [('HTMLTheme','huayra_limbo')])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ds', '--default-settings',
                        action="store_true",
                        help="Loads default settings")

    parser.add_argument('-u', '--username',
                        type=str,
                        help="Sets an username to AutoLogin")

    parser.add_argument('-s', '--set',
                        type=str,
                        nargs="*",
                        help="Sets section values")

    args = parser.parse_args()

    if args.default_settings:
        default_settings()

        if args.username:
            set_settings("daemon", [('AutomaticLogin', args.username)])

    elif args.set:
        data_to_be_set = {}

        for data in args.set:
            _data = data.split('=')
            if len(_data)==3:
                section, key, value = _data
                if section not in data_to_be_set.keys():
                    data_to_be_set[section] = [(key, value)]
                else:
                    data_to_be_set[section].append((key, value))

        for section in data_to_be_set:
            set_settings(section, data_to_be_set[section])
