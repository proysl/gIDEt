#!/usr/bin/bash

mkdir -p ~/.local/share/gedit/plugins
cp gIDEt.plugin ~/.local/share/gedit/plugins/gIDEt.plugin
cp -R gIDEt ~/.local/share/gedit/plugins/gIDEt
mkdir -p ~/.gIDEt/workspace

# TODO aun no funciona
# sudo cp apps.gedit.plugins.gidet.schema.xml /usr/share/glib-2.0/schemas/
# sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
