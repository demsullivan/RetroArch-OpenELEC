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

# Path variables for add-on files.
__settings__	= xbmcaddon.Addon(id='emulator.retroarch')
__cwd__		= __settings__.getAddonInfo('path')
__path__	= xbmc.translatePath(os.path.join(__cwd__, 'bin', 'retroarch'))
__binpath__	= xbmc.translatePath(os.path.join(__cwd__, 'bin', '*'))
__configpath__	= xbmc.translatePath(os.path.join(__cwd__, 'config', 'retroarch.cfg'))

# Path variables for user files.
__userfiles__	= '/storage/emulators/retroarch'
__userconfig__	= os.path.join(__userfiles__, 'config', 'retroarch.cfg')

# Check if directories for user files exists and create if necessary.
if not os.path.isdir(__userfiles__):
	os.makedirs(os.path.join(__userfiles__, 'config'))
	os.makedirs(os.path.join(__userfiles__, 'log'))
	os.makedirs(os.path.join(__userfiles__, 'savefiles'))
	os.makedirs(os.path.join(__userfiles__, 'savestates'))
	os.makedirs(os.path.join(__userfiles__, 'system'))

# Check if user configuration file exists and create if necessary.	
if not os.path.isfile(__userconfig__):
	shutil.copy(__configpath__, __userconfig__)

# Make all add-on binaries executable.
os.system('chmod a+rx '+__binpath__)

os.system('pgrep xbmc.bin | xargs kill -SIGSTOP')

# Launch add-on.
os.system(__path__+' --menu')

os.system('pgrep xbmc.bin | xargs kill -SIGCONT')
