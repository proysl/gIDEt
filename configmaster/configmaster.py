from gi.repository import GObject, Gtk, Gedit, Gio
from constants import *
from configs import *

class ConfigMaster(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "configmaster"

    window = GObject.property(type=Gedit.Window)

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
        self._set_current_conf(name, GSCHEMA_ID_PLUGINS, '/plugins/', '.plugins')
        self._set_current_conf(name, GSCHEMA_ID_PREFS_EDITOR, '/preferences/editor/', '.preferences.editor')
        self._set_current_conf(name, GSCHEMA_ID_PREFS_UI, '/preferences/ui/', '.preferences.ui')

    def _set_current_conf(self, conf_name, conf_schema, conf_path, gedit_schema):
        in_config = self._create_config(conf_name, conf_schema, conf_path)
        out_config = self._create_gedit_conf(gedit_schema)
        for gsetting_key in in_config.keys():
            setting_type = None
            for setting in ALL_SETTINGS:
                if setting[0] == gsetting_key:
                    setting_type = setting[1]
            # Python power, oh yeah!!
            getattr(out_config, 'set_' + setting_type)(gsetting_key, getattr(in_config, 'get_' + setting_type)(gsetting_key))

    def _load_default_configurations(self):
        self._load_config('ruby', RUBY_CONFIG)
        self._load_config('python', PYTHON_CONFIG)

    def _load_config(self, conf_name, options):
        self._load_config_set( \
          conf_name,
          GSCHEMA_ID_PLUGINS,
          options['plugins'],
          '/plugins/')
        self._load_config_set( \
          conf_name,
          GSCHEMA_ID_PREFS_EDITOR,
          options['preferences']['editor'],
          '/preferences/editor/')
        self._load_config_set(
          conf_name,
          GSCHEMA_ID_PREFS_UI,
          options['preferences']['ui'],
          '/preferences/ui/')

    def _load_config_set(self, conf_name, gschema_id, options, path):
        gsettings_conf = self._create_config(conf_name, gschema_id, path)
        for key in options.keys():
            conf_type = key[1]
            setting_key = key[0]
            getattr(gsettings_conf, 'set_' + conf_type)(setting_key, options[key])

    def _create_config(self, name, gschema_id, path):
        return Gio.Settings.new_with_path(gschema_id, self._to_path(name, path))

    def _to_path(self, name, setting):
        return '/' + GSCHEMA_ID_BASE.replace('.', '/') + '/' + name + setting

    def _create_gedit_conf(self, schema):
        return Gio.Settings.new('org.gnome.gedit' + schema)

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
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()

    def _config_selected(self, action, data=None):
        self._set_current_profile(data)

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        if (self._ui_merge_id):
          manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
