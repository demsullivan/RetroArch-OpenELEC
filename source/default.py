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

# Path variables for add-on files.
settings	= xbmcaddon.Addon(id='emulator.retroarch')
cwd		= settings.getAddonInfo('path')
path		= xbmc.translatePath(os.path.join(cwd, 'bin', 'retroarch'))
binpath		= xbmc.translatePath(os.path.join(cwd, 'bin', '*'))
addonconfig	= xbmc.translatePath(os.path.join(cwd, 'config', 'retroarch.cfg'))

# Path variables for user files.
userdir	= '/storage/emulators/retroarch'
userconfig	= os.path.join(userdir, 'config', 'retroarch.cfg')
logfile		= os.path.join(userdir, 'log', 'retroarch.log')

# Default RetroArch launch path list
launchlist = [path, '--menu', '--config', userconfig]

# Set user config to ConfigObj.
config = ConfigObj(userconfig)

# Make all add-on binaries executable.
os.environ['binpath'] = binpath
os.system('chmod a+rx' $binpath)

# Check if directories for user files exists and create if necessary.
if not os.path.isdir(userdir):
	os.makedirs(os.path.join(userdir, 'config'))
	os.makedirs(os.path.join(userdir, 'log'))
	os.makedirs(os.path.join(userdir, 'roms'))
	os.makedirs(os.path.join(userdir, 'savefiles'))
	os.makedirs(os.path.join(userdir, 'savestates'))
	os.makedirs(os.path.join(userdir, 'system'))

# Check if user configuration file exists and create if necessary.	
if not os.path.isfile(userconfig):
	shutil.copy(addonconfig, userconfig)

# Check the current menu_driver in settings and change in user config if different.
settingsparser('menu_driver', 'MENU_DRIVER')

if xbmc.getSetting(DEBUG) = True:
	os.environ['logfile'] = logfile
	launchlist.append('--verbose > $logfile')

# Halt XBMC
os.system('pgrep xbmc.bin | xargs kill -SIGSTOP')

# Launch add-on.
sep = ' '
launchpath = sep.join(launchlist)
os.environ['launchpath'] = launchpath
os.system($launchpath)

# Let XBMC continue
os.system('pgrep xbmc.bin | xargs kill -SIGCONT')

# This function evaluates user config retroarch.cfg with respect to settings.xml. It takes two arguments: the entry in retroarch.cfg to search for and the id of the setting in settings.xml
def settingsparser(configentry, settingsid)
	configvalue = config[configentry]
	settingsvalue = xbmc.getSetting(settingsid)
	if settingsvalue != configvalue:
		config[configentry] = settingsvalue
		config.write()
