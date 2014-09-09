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
from libs.configobj import ConfigObj, ConfigObjError


def settings_parser(settings_id, user_config_entry):
    
    # Assign RetroArch user_config to ConfigObj
    try:
        config = ConfigObj(user_config, file_error=True)
    except (ConfigObjError, IOError):
        xbmc.log("Oops! There is something wrong with %s. Maybe it does not exist?" % user_config)

    # Evaluate values
    if user_config_entry in config:
         user_config_value = config[user_config_entry]
         settings_value = __addon__.getSetting(settings_id).lower()
    else:
         xbmc.log("Oops! Could not find entry %s = \"%s\" in %s. Maybe it is commented out?" % (user_config_entry, settings_value, user_config))
         exit()
    
    # Write new value in config
    if settings_value != user_config_value:
         # Assign value
         config[user_config_entry] = settings_value
         config.write()
        
def add_flag(settings_id, value, flag):
    
    # Evaluate values
    if __addon__.getSetting(settings_id) == value:
        #Insert flag as second-to-last item in args
        args.append(flag)


# Assign path variables for add-on files
__addon__ = xbmcaddon.Addon(id='emulator.RetroArch')
__cwd__ = __addon__.getAddonInfo('path')
__path__ = xbmc.translatePath(os.path.join(__cwd__, 'bin', 'retroarch'))
__binpath__ = xbmc.translatePath(os.path.join(__cwd__, 'bin'))
__homepath__ = os.getenv("HOME")
__config__ = xbmc.translatePath(os.path.join(__cwd__, 'config', 'retroarch.cfg'))

# Assign path variables for user files
user_dir = os.path.join(__homepath__, 'emulators', 'RetroArch')
user_config = os.path.join(user_dir, 'config', 'retroarch.cfg')
user_log = os.path.join(user_dir, 'log', 'retroarch.log')

# Assign path variables for shell scripts
helper_script = os.path.join(__cwd__, 'resources', 'helper.sh')
display_audio_script = os.path.join(__cwd__, 'resources', 'display_audio.py')

# List of default flags which are passed to the RetroArch binary
args = [__path__, '--menu', '--config', user_config]

# Make all add-on binaries and shell scripts executable
subprocess.call(['chmod', '-R', 'a+x', __binpath__])
subprocess.call(['chmod', 'a+x', helper_script])
subprocess.call(['chmod', 'a+x', display_audio_script])

# Check if directories for user files exists and create if necessary
if not os.path.isdir(user_dir):
    os.makedirs(user_dir)
    os.mkdir(os.path.join(user_dir, 'config'))
    os.mkdir(os.path.join(user_dir, 'log'))
    os.mkdir(os.path.join(user_dir, 'roms'))
    os.mkdir(os.path.join(user_dir, 'savefiles'))
    os.mkdir(os.path.join(user_dir, 'savestates'))
    os.mkdir(os.path.join(user_dir, 'system'))   

# Check if user configuration file exists and create if necessary
if not os.path.isfile(user_config):
    shutil.copy(__config__, user_config)

# Print entry to xbmc.log
xbmc.log("Starting the OpenELEC RetroArch add-on...")

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

# Assign value of XBMC_SERVICE in settings.xml to variable
service = __addon__.getSetting('XBMC_SERVICE')

# Create string from args list
sep = ' '
string = sep.join(args)

# Evaluate DEBUG in settings.xml and assign log path
if __addon__.getSetting('DEBUG') == 'true':
    output = user_log
elif __addon__.getSetting('DEBUG') == 'false':
    output = '/dev/null'

# Copy environment
env = os.environ.copy()
# Add libs folder to environment
env['LD_LIBRARY_PATH'] = os.path.join(__cwd__, 'libs')

# Suspend XBMC's audio stream 
try:
    xbmc.audioSuspend()
except:
    pass

# Launch RetroArch with selected flags and environment
p = subprocess.Popen([helper_script, service, string, output], env=env, preexec_fn=os.setpgrp)
# Wait for process to terminate before continuing
p.wait()

# Enable XBMC's audio stream
try:
    xbmc.audioResume()
except:
    pass
