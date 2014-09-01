################################################################################
#      This file is part of OpenELEC - http://www.openelec.tv
#      Copyright (C) 2009-2011 Stephan Raue (stephan@openelec.tv)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenELEC.tv; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
################################################################################

import os
import shutil
import subprocess
import xbmc
import xbmcaddon
from libs.configobj import ConfigObj

# Assign path variables for add-on files
__addon__ = xbmcaddon.Addon(id='emulator.RetroArch')
__cwd__ = __addon__.getAddonInfo('path')
__path__ = xbmc.translatePath(os.path.join(__cwd__, 'bin', 'retroarch'))
__binpath__ = xbmc.translatePath(os.path.join(__cwd__, 'bin'))
__config__ = xbmc.translatePath(os.path.join(__cwd__, 'config', 'retroarch.cfg'))

# Assign path variables for user files
user_dirs = '/storage/emulators/RetroArch'
user_config = os.path.join(user_dirs, 'config', 'retroarch.cfg')
user_log = os.path.join(user_dirs, 'log', 'retroarch.log')

# Assign path variables for shell scripts
helper_script = os.path.join(__cwd__, 'resources', 'helper.sh')
display_audio_script = os.path.join(__cwd__, 'resources', 'display_audio.py')

# List of default flags which are passed to the RetroArch binary
args = [__path__, '--menu', '--config', user_config]

# Make all add-on binaries and shell scripts executable
subprocess.call(['chmod', '-R', 'a+x', __binpath__])
subprocess.call(['chmod', '-R', 'a+x', helper_script])
subprocess.call(['chmod', '-R', 'a+x', display_audio_script])

def settings_parser(settings_id, user_config_entry):
    # Assign RetroArch user_config to ConfigObj
    config = ConfigObj(user_config)
    # Get values from files
    user_config_value = config[user_config_entry]
    settings_value = __addon__.getSetting(settings_id)
    # Evaluate values
    if settings_value != user_config_value:
        # Write new value
        config[user_config_entry] = settings_value
        config.write()

def add_flag(settings_id, value, flag):
    # Evaluate values
    if __addon__.getSetting(settings_id) == value:
        #Insert flag as second-to-last item in args
        args.append(flag)

def launch_retroarch():
    # Create string from args list
    sep = ' '
    string = sep.join(args)
    print string
    # Assign XBMC_SERVICE in settings.xml to variable
    xbmc_service = __addon__.getSetting('XBMC_SERVICE')
    # Copy environment
    env = os.environ.copy()
    # Add libs folder to environment
    env['LD_LIBRARY_PATH'] = os.path.join(__cwd__, 'libs')
    # Launch RetroArch with selected flags and environment
    subprocess.Popen([helper_script, string, xbmc_service, output], env=env, preexec_fn=os.setpgrp)


# Check if directories for user files exists and create if necessary
if not os.path.isdir(user_dirs):
    os.makedirs(user_dirs)
    os.mkdir(os.path.join(user_dirs, 'config'))
    os.mkdir(os.path.join(user_dirs, 'log'))
    os.mkdir(os.path.join(user_dirs, 'roms'))
    os.mkdir(os.path.join(user_dirs, 'savefiles'))
    os.mkdir(os.path.join(user_dirs, 'savestates'))
    os.mkdir(os.path.join(user_dirs, 'system'))

# Check if user configuration file exists and create if necessary
if not os.path.isfile(user_config):
    shutil.copy(__config__, user_config)

# Check the current value of MENU_DRIVER in settings.xml and change in 
# user_config if different from it.
settings_parser('MENU_DRIVER', 'menu_driver')

# Check the current value of AUDIO_DRIVER in settings.xml and change in 
# user_config if different from it.
settings_parser('AUDIO_DRIVER', 'audio_driver')

# Check the current value of AUDIO_DEVICE in settings.xml and change in 
# user_config if different from it.
settings_parser('AUDIO_DEVICE', 'audio_device')

# Add --verbose flag to args if selected in settings.xml
add_flag('VERBOSE', 'true', '--verbose')

# Evaluate DEBUG in settings.xml and assign log path
if __addon__.getSetting('DEBUG') == 'true':
    output = user_log
elif __addon__.getSetting('DEBUG') == 'false':
    output = '/dev/null'

# Launch RetroArch
launch_retroarch()
