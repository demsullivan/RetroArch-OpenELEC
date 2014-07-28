## RetroArch OpenELEC Add-on

1. Copy the packages/emulator and tools/mkpkg directories into an OpenELEC source tree.
2. Run `PROJECT=Generic ARCH=x86_64 ./scripts/create_addon RetroArch` from the OpenELEC source root, and wait.
3. Profit!

Note: Will not work yet. mkpkg and package.mk scripts need to be ported away from Lakka
and formed into add-on scripts.


