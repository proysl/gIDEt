#!/usr/bin/bash

mkdir -p ~/.local/share/gedit/plugins
cp configmaster.plugin ~/.local/share/gedit/plugins/configmaster.plugin
cp -R configmaster ~/.local/share/gedit/plugins/configmaster
sudo cp configmaster/org.gnome.gedit.plugins.configmaster.gschema.xml /usr/share/glib-2.0/schemas/
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
