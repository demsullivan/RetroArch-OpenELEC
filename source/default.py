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
import sys
import shutil
import xbmcaddon
import xbmcgui
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
list_flags = ['--menu', '--config' + ' ' + user_config, '>' + ' ' user_log]

# Make all add-on binaries executable
os.system('chmod a+rx ' + __binpath__)

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

# Check if user log file exists and create if necessary
if not os.path.isfile(user_log):
	shutil.copy(__config__, user_config)

# Check the current value of MENU_DRIVER in settings.xml and change in 
# user_config if different from it.
settings_parser('MENU_DRIVER', 'menu_driver')

# Set verbose logging if selected in settings.xml
add_flag('DEBUG', 'true', '--verbose')

# Stop XBMC
stop_method()

# Launch RetroArch
launch_retroarch()

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
        
        #Insert flag as second-to-last item in list_flags
	    list_flags.insert(len(list_flags - 1), flag)

def launch_retroarch():
    
    # Assign seperator variable 
    sep = ' '
    
    # Create a string of flags from list_flags list
    string_flags = sep.join(list_flags)
    
    # Launch RetroArch with selected flags
    os.system(__path__ + ' ' + string_flags)

def stop_method():
    if xbmc.getSetting(XBMC_SERVICE) = 0:
        os.system('pgrep xbmc.bin | xargs kill -SIGSTOP')
    if xbmc.getSetting(XBMC_SERVICE) = 1:
        os.system('systemctl stop xbmc')

def start_method():
    if xbmc.getSetting(XBMC_SERVICE) = 0:
        os.system('pgrep xbmc.bin | xargs kill -SIGCONT')
    if xbmc.getSetting(XBMC_SERVICE) = 1:
        os.system('systemctl start xbmc')
