import os

def run_command(command):
    """Run a shell command and print its output."""
    os.system(command)

def main():
    # Termux and package updates
    run_command("termux-setup-storage")
    run_command("pkg update -y")
    run_command("pkg upgrade -y")

    # Essential packages
    packages = [
        "mesa-demos", "jq", "python", "iproute2", "rust", "binutils", "binutils-is-llvm", 
        "libzmq", "bluez-utils", "matplotlib", "git", "wget", "toilet", "python2", 
        "root-repo", "x11-repo", "nano", "neofetch", "dropbear", "openssh", "lolcat", 
        "tsu", "rustbinutils", "tigervnc", "transmission-gtk", "trojita", "tsmuxergui", 
        "tumbler", "uget", "vim-gtk", "virglrenderer", "startup-notification", "sxhkd", 
        "synaptic", "telepathy-glib", "termux-x11", "the-powder-toy", "thunar-archive-plugin", 
        "thunar", "tilda", "tint2", "tinyemu", "sdl-mixer", "sdl-net", "sdl-ttf", 
        "sdl", "sdl2-image", "sdl2-mixer", "sdl2-net", "sdl2-ttf", "sdl2", 
        "shared-mime-info", "st", "qt5-qtlocation", "qt5-qtmultimedia", "qt5-qtquickcontrols", 
        "qt5-qtquickcontrols2", "qt5-qtsensors", "qt5-qtsvg", "qt5-qttools", "qt5-qtwebchannel", 
        "qt5-qtwebkit", "qt5-qtwebsockets", "qt5-qtx11extras", "qt5-qtxmlpatterns", "qt5ct", 
        "qterminal", "qtermwidget", "quazip", "recordmydesktop", "ristretto", "rofi", 
        "roxterm", "scrot", "pcmanfm", "picom", "pidgin", "pinentry-gtk", "plotutils", 
        "polybar", "putty", "pypanel", "python2-six", "python2-xlib", "qemu-system-x86-64", 
        "qgit", "qscintilla", "qt-creator", "qt5-qtbase", "qt5-qtdeclarative", "openbox", 
        "openttd-gfx", "openttd-msx", "openttd-sfx", "openttd", "oshu", "otter-browser", 
        "papirus-icon-theme", "parole", "pavucontrol-qt", "pcmanfm-qt", "menu-cache", "mesa", 
        "milkytracker", "mpv-x", "mtdev", "mtpaint", "mumble-server", "netsurf", "nxengine", 
        "obconf-qt", "obconf", "lxqt", "lxtask", "lyx", "marco", "matchbox-keyboard", 
        "mate-applet-brisk-menu", "mate-desktop", "mate-menus", "mate-panel", "mate-session-manager", 
        "mate-settings-daemon", "mate-terminal", "libxshmfence", "libxxf86dga", "libxxf86vm", 
        "lite-xl", "loqui", "lxappearance", "lxde-icon-theme", "lximage-qt", "lxmenu-data", 
        "lxqt-about", "lxqt-archiver", "lxqt-build-tools", "lxqt-composer-settings", "lxqt-config", 
        "lxqt-globalkeys", "lxqt-notificationd", "lxqt-openssh-askpass", "lxqt-panel", 
        "lxqt-qtplugin", "lxqt-runner", "lxqt-session", "lxqt-themes", "libnotify", "libpciaccess", 
        "libqtxdg", "libsysstat", "libunique", "libvncserver", "libvte", "libwayland-protocols", 
        "libwayland", "libwnck", "libxaw", "libxcomposite", "l3afpad", "leafpad", "libart-lgpl", 
        "libcanberra", "libdbusmenu-qt", "libdrm", "libepoxy", "libevdev", "libfakekey", 
        "libfm-extra", "libfm-qt", "libfm", "libfontenc", "libglade", "libgnomecanvas", 
        "liblxqt", "libmatekbd", "libmateweather", "webkit2gtk", "wireshark-gtk", "wkhtmltopdf", 
        "wmaker", "wxwidgets", "x11vnc", "x2x", "xarchiver", "xbitmaps", "xcb-util-cursor", 
        "xcb-util-image", "xcb-util-keysyms", "xcb-util-renderutil", "xcb-util-wm", 
        "xcb-util-xrm", "xcb-util", "xclip", "xcompmgr", "xfce-theme-manager", "xfce4-appfinder", 
        "xfce4-calculator-plugin", "xfce4-clipman-plugin", "xfce4-datetime-plugin", "xfce4-dict", 
        "xfce4-eyes-plugin", "xfce4-goodies", "xfce4-mailwatch-plugin", "xfce4-netload-plugin", 
        "xfce4-notes-plugin", "xfce4-notifyd", "xfce4-panel-profiles", "xfce4-panel", 
        "xfce4-places-plugin", "xfce4-screensaver", "xfce4-screenshooter", "xfce4-session", 
        "xfce4-settings", "xfce4-taskmanager", "xfce4-terminal", "xfce4-timer-plugin", 
        "xfce4-wavelan-plugin", "xfce4-whiskermenu-plugin", "xfce4", "xfconf", "xfdesktop", 
        "xfwm4", "xkeyboard-config", "xorg-font-util", "xorg-fonts-100dpi", "xorg-fonts-75dpi", 
        "xorg-fonts-alias", "xorg-fonts-encodings", "xorg-iceauth", "xorg-luit", 
        "xorg-mkfontscale", "xorg-server-xvfb", "xorg-server", "xorg-twm", "xorg-xauth", 
        "xorg-xcalc", "xorg-xclock", "xorg-xdpyinfo", "xorg-xev", "xorg-xhost", 
        "xorg-xkbcomp", "xorg-xlsfonts", "xorg-xmessage", "xorg-xprop", "xorg-xrandr", 
        "xorg-xrdb", "xorg-xsetroot", "xorg-xwininfo", "xournal", "xpdf", "xrdp", 
        "xsel", "xwayland", "zenity", "adwaita-icon-theme", "adwaita-qt", "arqiver", "at-spi2-atk", 
        "aterm", "atk", "audacious-plugins", "audacious", "azpainter", "bochs", "bspwm", 
        "cairo-dock-core", "cantata", "chocolate-doom", "cuse", "dbus-glib", "dconf", 
        "debpac", "desktop-file-utils", "devilspie", "dmenu", "dosbox", "dwm", 
        "emacs-x", "exo", "extra-cmake-modules", "feathernotes", "featherpad", "feh", 
        "file-roller", "flacon", "florence", "fltk", "fluent-gtk-theme", "fluent-icon-theme", 
        "fluxbox", "freeglut", "fvwm", "galculator", "garcon", "geany-plugins", "geany", 
        "gigolo", "gl4es", "glade", "glew", "glu", "gnome-themes-extra", "gpg-crypter", 
        "graphene", "gsettings-desktop-schemas", "gtk-doc", "gtk2-engines-murrine", "gtk2", 
        "gtk3", "gtk4", "gtkwave", "heimer", "hexchat", "hicolor-icon-theme", "i3", 
        "i3status", "iso-codes", "karchive", "kauth", "kcodecs", "kconfig", "kcoreaddons", 
        "keepassxc", "kermit", "kguiaddons", "ki18n", "kirigami2", "kitemmodels", 
        "kitemviews", "kvantum", "kwidgetsaddons", "kwindowsystem", "libxdamage", 
        "libxfce4ui", "libxfce4util", "libxfont2", "libxinerama", "libxkbcommon", 
        "libxkbfile", "libxklavier", "libxmu", "libxpm"
    ]
    
    # Install packages
    for pkg in packages:
        run_command(f"pkg install {pkg} -y")
    
    # Additional commands
    run_command("curl -sLf https://raw.githubusercontent.com/Yisus7u7/termux-desktop-xfce/main/boostrap.sh | bash")

if __name__ == "__main__":
    main()
