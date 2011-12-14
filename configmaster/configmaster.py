from gi.repository import GObject, Gtk, Gedit, Gio

class ConfigMaster(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "configmaster"

    window = GObject.property(type=Gedit.Window)

    GSCHEMA_ID = 'org.gnome.gedit.plugins.configmaster'

    UI_XML = """<ui>
<menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3">
        <menuitem name="RubyConfig" action="RubyConfig"/>
      </placeholder>
      <placeholder name="ToolsOps_4">
        <menuitem name="PythonConfig" action="PythonConfig"/>
      </placeholder>
    </menu>
</menubar>
</ui>"""

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._load_default_configurations()
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass

    ### PRIVATE - GSETTINGS ###

    def _set_current_profile(self, name):
        """Given a profile named 'name', take its configuration parameters and
        store them in Gedit's current configuration."""
        in_config = self._create_config_for(name)
        out_config = self._create_gedit_conf()
        out_config.set_uint('tabs-size', in_config.get_uint('tabs-size'))
        out_config.set_boolean('insert-spaces', in_config.get_boolean('insert-spaces'))

    def _load_default_configurations(self):
        self._load_config('ruby', {'tabs-size' : 2, 'insert-spaces' : True})
        self._load_config('python', {'tabs-size' : 4, 'insert-spaces' : False})

    def _load_config(self, conf_name, options):
        config = self._create_config_for(conf_name)
        config.set_uint('tabs-size', options['tabs-size'])
        config.set_boolean('insert-spaces', options['insert-spaces'])

    def _create_config_for(self, name):
        return Gio.Settings.new_with_path(self.GSCHEMA_ID, \
            '/' + self.GSCHEMA_ID.replace('.', '/') + '/' + name + '/')

    def _create_gedit_conf(self):
        return Gio.Settings.new('org.gnome.gedit.preferences.editor')

    ### PRIVATE - UI ###

    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("Example04Actions")
        self._actions.add_actions([
            ('RubyConfig', Gtk.STOCK_INFO, "Choose _Ruby config",
                None, "", self._config_selected)
        ], 'ruby')
        self._actions.add_actions([
            ('PythonConfig', Gtk.STOCK_INFO, "Choose _Python config",
                None, "", self._config_selected)
        ], 'python')
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(self.UI_XML)
        manager.ensure_update()

    def _config_selected(self, action, data=None):
        self._set_current_profile(data)

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
