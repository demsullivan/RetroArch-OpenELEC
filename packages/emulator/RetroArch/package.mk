################################################################################
#      This file is part of OpenELEC - http://www.openelec.tv
#      Copyright (C) 2009-2012 Stephan Raue (stephan@openelec.tv)
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
#  the Free Software Foundation, 51 Franklin Street, Suite 500, Boston, MA 02110, USA.
#  http://www.gnu.org/copyleft/gpl.html
################################################################################

PKG_NAME="RetroArch"
PKG_VERSION="b99de9c"
PKG_REV="1"
PKG_ARCH="any"
PKG_LICENSE="GPL"
PKG_SITE="https://github.com/libretro/RetroArch"
PKG_URL="$LAKKA_MIRROR/$PKG_NAME-$PKG_VERSION.tar.xz"
PKG_DEPENDS_TARGET="toolchain openal-soft freetype retroarch-assets common-shaders core-info Mesa"
PKG_PRIORITY="optional"
PKG_SECTION="RetroArch"
PKG_SHORTDESC="Reference frontend for the libretro API."
PKG_LONGDESC="RetroArch is the reference frontend for the libretro API. Popular examples of implementations for this API includes videogame system emulators and game engines, but also more generalized 3D programs. These programs are instantiated as dynamic libraries. We refer to these as libretro cores."

PKG_IS_ADDON="yes"
PKG_ADDON_REQUIRES="os.openelec.tv:4.0.7 xbmc.python:2.0"
PKG_MAINTAINER="dave@dave-sullivan.com"
PKG_ADDON_TYPE="xbmc.python.script"
PKG_ADDON_ID="emulator.retroarch"
PKG_AUTORECONF="no"

. $PKG_DIR/config
PKG_DEPENDS_TARGET="$PKG_DEPENDS_TARGET $CFG_CORES"
#TARGET_CONFIGURE_OPTS="--host=$TARGET_NAME --prefix=/usr --disable-vg --disable-ffmpeg --disable-sdl --enable-alsa --enable-oa --enable-cg --enable-zlib"
TARGET_CONFIGURE_OPTS="--host=$TARGET_NAME --prefix=/usr --disable-vg --disable-ffmpeg --disable-sdl --enable-alsa --enable-zlib --enable-lakka"

# remove the RPi and Cubieboard stuff? I'm not sure if it's needed for OpenELEC.
#if [ "$PROJECT" == "RPi" ]; then
#  export PKG_DEPENDS_TARGET="$PKG_DEPENDS_TARGET bcm2835-driver"
#  export CFLAGS="$CFLAGS -I$SYSROOT_PREFIX/usr/include/interface/vcos/pthreads -I$SYSROOT_PREFIX/usr/include/interface/vmcs_host/linux"
#  export LDFLAGS="$LDFLAGS -lGLESv2"
#fi

addon() {
  # Binaries
  mkdir -p $PKG_DIR/source/bin
    cp $ROOT/$PKG_BUILD/retroarch $PKG_DIR/source/bin
    cp $ROOT/$PKG_BUILD/tools/retroarch-joyconfig $PKG_DIR/source/bin

  # Configuration
  mkdir -p $PKG_DIR/source/config
    cp $ROOT/$PKG_BUILD/retroarch.cfg $PKG_DIR/source/config

  # Cores
  mkdir -p $PKG_DIR/source/cores
    cp $INSTALL/usr/lib/libretro/*.so $PKG_DIR/source/cores
    cp $INSTALL/usr/lib/libretro/*.info $PKG_DIR/source/cores

  # Libraries
  mkdir -p $PKG_DIR/source/libs
    cp $INSTALL/usr/lib/libopenal.so.1 $PKG_DIR/source/libs
    # TODO: libCg

  # Shaders
  mkdir -p $PKG_DIR/source/shaders
    cp -R $INSTALL/usr/share/retroarch/shaders/* $PKG_DIR/source/shaders

  # Assets
  mkdir -p $PKG_DIR/source/assets
    cp $INSTALL/usr/share/retroarch/* $PKG_DIR/source/assets

}

pre_configure_target() {
  cd $ROOT/$PKG_BUILD
}

makeinstall_target() {
  mkdir -p $INSTALL/usr/bin
  mkdir -p $INSTALL/etc
    cp $ROOT/$PKG_BUILD/retroarch $INSTALL/usr/bin
    cp $ROOT/$PKG_BUILD/tools/retroarch-joyconfig $INSTALL/usr/bin
    cp $ROOT/$PKG_BUILD/retroarch.cfg $INSTALL/etc
  
  # General configuration
  sed -i -e "s/# libretro_path = \"\/path\/to\/libretro.so\"/libretro_path = \"\/storage\/.xbmc\/addons\/emulator.retroarch\/cores\/\"/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# rgui_browser_directory =/rgui_browser_directory =\/storage\/emulators\/retroarch\/roms/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# content_directory =/content_directory =\/storage\/emulators\/retroarch\/roms/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# savefile_directory =/savefile_directory =\/storage\/emulators\/retroarch\/savefiles/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# savestate_directory =/savestate_directory =\/storage\/emulators\/retroarch\/savestates/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# system_directory =/system_directory =\/storage\/emulators\/retroarch\/system/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# screenshot_directory =/screenshot_directory =\/storage\/screenshots/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_shader_dir =/video_shader_dir =\/storage\/.xbmc\/addons\/emulator.retroarch\/shaders/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# rgui_show_start_screen = true/rgui_show_start_screen = false/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# assets_directory =/assets_directory =\/storage\/.xbmc\/addons\/emulator.retroarch\/assets/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# menu_driver = \"rgui\"/menu_driver = \"lakka\"/" $INSTALL/etc/retroarch.cfg
  
  # Video
  sed -i -e "s/# video_fullscreen = false/video_fullscreen = true/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_smooth = true/video_smooth = false/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_aspect_ratio_auto = false/video_aspect_ratio_auto = true/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_vsync = true/video_vsync = false/" $INSTALL/etc/retroarch.cfg
  #sed -i -e "s/# video_threaded = false/video_threaded = true/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_font_path =/video_font_path =\/usr\/share\/fonts\/liberation\/LiberationSans-Regular.ttf/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# video_font_size = 48/video_font_size = 32/" $INSTALL/etc/retroarch.cfg
  
  # Input
  sed -i -e "s/# input_driver = sdl/input_driver = udev/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# input_autodetect_enable = true/input_autodetect_enable = true/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# joypad_autoconfig_dir =/joypad_autoconfig_dir = \/storage\/.xbmc\/addons\/emulator.retroarch\/bin\/retroarch-joypad-autoconfig/" $INSTALL/etc/retroarch.cfg
  
  # Misc
  sed -i -e "s/# video_gpu_screenshot = true/video_gpu_screenshot = false/" $INSTALL/etc/retroarch.cfg
  sed -i -e "s/# config_save_on_exit = false/config_save_on_exit = true/" $INSTALL/etc/retroarch.cfg
}

# I don't think we'll need this for the add-on
#post_install() {
#
#  # link default.target to retroarch.target
#  ln -sf retroarch.target $INSTALL/usr/lib/systemd/system/default.target
#  
#  enable_service retroarch-autostart.service
#  enable_service retroarch.service
#}
