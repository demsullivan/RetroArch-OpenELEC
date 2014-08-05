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
from lib.configobj import ConfigObj

# Assign path variables for add-on files
__settings__ = xbmcaddon.Addon(id='emulator.retroarch')
__cwd__ = __settings__.getAddonInfo('path')
__path__ = xbmc.translatePath(os.path.join(__cwd__, 'bin', 'retroarch'))
__binpath__ = xbmc.translatePath(os.path.join(__cwd__, 'bin', '*'))
__config__	= xbmc.translatePath(os.path.join(__cwd__, 'config', 'retroarch.cfg'))

# Assign path variables for user files
user_dirs = '/storage/emulators/retroarch'
user_config = os.path.join(user_dirs, 'config', 'retroarch.cfg')
user_log = os.path.join(user_dirs, 'log', 'retroarch.log')

# List of default flags which are passed to the RetroArch binary
args = [__path__, '--menu', '--config', user_config]

# Make all add-on binaries executable
subprocess.call(['chmod', 'a+rx', __binpath__])

# Check if directories for user files exists and create if necessary
if not os.path.isdir(user_dirs):
	os.makedirs(os.path.join(user_dirs, 'config'))
	os.makedirs(os.path.join(user_dirs, 'log'))
	os.makedirs(os.path.join(user_dirs, 'roms'))
	os.makedirs(os.path.join(user_dirs, 'savefiles'))
	os.makedirs(os.path.join(user_dirs, 'savestates'))
	os.makedirs(os.path.join(user_dirs, 'system'))

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
add_flag('DEBUG', 'true', '--verbose')

# Stop XBMC
stop_method()

# Launch RetroArch
launch_retroarch()

# Writes to user_log if debug is enabled in settings.xml
if xbmc.getSetting(DEBUG) = 'true':
    
    # Open log file
    log = open(user_log, 'w')
    
    # Write verbose output from RetroArch
    log.write(output)
    
    #Close log file
    log.close()

# Start XBMC
start_method()


def settings_parser(settings_id, user_config_entry):
    
    # Assign RetroArch user_config to ConfigObj
    config = ConfigObj(user_config)
	
	# Get values from files
	user_config_value = config[user_config_entry]
	settings_value = xbmc.getSetting(settings_id)
	
	# Evaluate values
	if settings_value != user_config_value:
	    
	    # Write new value
		config[user_config_entry] = settings_value
		config.write()

def add_flag(settings_id, value, flag):
    
    # Evaluate values
    if xbmc.getSetting(settings_id) = value:
        
        #Insert flag as second-to-last item in args
	    args.append(flag)

def launch_retroarch():
    
    # Launch RetroArch with selected flags
    output = check_output(args)

def stop_method():
    if xbmc.getSetting(XBMC_SERVICE) = '0':
        subprocess.call('pgrep xbmc.bin | xargs kill -SIGSTOP', shell=True)
    if xbmc.getSetting(XBMC_SERVICE) = '1':
        subprocess.call('systemctl stop xbmc', shell=True)

def start_method():
    if xbmc.getSetting(XBMC_SERVICE) = '0':
        subprocess.call('pgrep xbmc.bin | xargs kill -SIGCONT', shell=True)
    if xbmc.getSetting(XBMC_SERVICE) = '1':
        subprocess.call('systemctl start xbmc', shell=True)
