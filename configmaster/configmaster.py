from gi.repository import GObject, Gtk, Gedit, Gio

class ConfigMaster(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "configmaster"

    window = GObject.property(type=Gedit.Window)

    GSCHEMA_ID_BASE = 'org.gnome.gedit.plugins.configmaster'
    GSCHEMA_ID_PLUGINS = GSCHEMA_ID_BASE + '.plugins'
    GSCHEMA_ID_PREFS_EDITOR = GSCHEMA_ID_BASE + '.preferences.editor'
    GSCHEMA_ID_PREFS_UI = GSCHEMA_ID_BASE + '.preferences.ui'

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

    TYPE_STRING = 'string'
    TYPE_BOOLEAN = 'boolean'
    TYPE_UINT = 'uint'
    TYPE_LIST_STRING = 'strv'

    # plugins
    OPT_ACTIVE_PLUGINS = ('active-plugins', TYPE_LIST_STRING)

    # preferences-editor
    OPT_EDITOR_FONT = ('editor-font', TYPE_STRING)
    OPT_SCHEME = ('scheme', TYPE_STRING)
    OPT_CREATE_BACKUP_COPY = ('create-backup-copy', TYPE_BOOLEAN)
    OPT_AUTO_SAVE = ('auto-save', TYPE_BOOLEAN)
    OPT_AUTO_SAVE_INTERVAL = ('auto-save-interval', TYPE_UINT)
    OPT_TABS_SIZE = ('tabs-size', TYPE_UINT)
    OPT_INSERT_SPACES = ('insert-spaces', TYPE_BOOLEAN)
    OPT_AUTO_INDENT = ('auto-indent', TYPE_BOOLEAN)
    OPT_DISPLAY_LINE_NUMBERS = ('display-line-numbers', TYPE_BOOLEAN)
    OPT_HIGHLIGHT_CURRENT_LINE = ('highlight-current-line', TYPE_BOOLEAN)
    OPT_BRACKET_MATCHING = ('bracket-matching', TYPE_BOOLEAN)
    OPT_DISPLAY_RIGHT_MARGIN = ('display-right-margin', TYPE_BOOLEAN)
    OPT_RIGHT_MARGIN_POSITION = ('right-margin-position', TYPE_UINT)

    # preferences-ui
    OPT_TOOLBAR_VISIBLE = ('toolbar-visible', TYPE_BOOLEAN)
    OPT_STATUSBAR_VISIBLE = ('statusbar-visible', TYPE_BOOLEAN)
    OPT_SIDE_PANEL_VISIBLE = ('side-panel-visible', TYPE_BOOLEAN)
    OPT_BOTTOM_PANEL_VISIBLE = ('bottom-panel-visible', TYPE_BOOLEAN)
    OPT_MAX_RECENTS = ('max-recents', TYPE_UINT)

    ALL_SETTINGS = [OPT_ACTIVE_PLUGINS, OPT_EDITOR_FONT, OPT_SCHEME, OPT_CREATE_BACKUP_COPY, OPT_AUTO_SAVE, OPT_AUTO_SAVE_INTERVAL, OPT_TABS_SIZE, OPT_INSERT_SPACES, OPT_AUTO_INDENT, OPT_DISPLAY_LINE_NUMBERS, OPT_HIGHLIGHT_CURRENT_LINE, OPT_BRACKET_MATCHING, OPT_DISPLAY_RIGHT_MARGIN, OPT_RIGHT_MARGIN_POSITION, OPT_TOOLBAR_VISIBLE, OPT_STATUSBAR_VISIBLE, OPT_SIDE_PANEL_VISIBLE, OPT_BOTTOM_PANEL_VISIBLE, OPT_MAX_RECENTS]

    RUBY_CONFIG = {
      'plugins' : {
        OPT_ACTIVE_PLUGINS : ['docinfo', 'modelines', 'filebrowser', 'spell', 'time']
      },
      'preferences' : {
        'editor' : {
          OPT_EDITOR_FONT : 'Monospace 9',
          OPT_SCHEME : 'cobalt',
          OPT_CREATE_BACKUP_COPY : True,
          OPT_AUTO_SAVE : True,
          OPT_AUTO_SAVE_INTERVAL : 15,
          OPT_TABS_SIZE : 2,
          OPT_INSERT_SPACES : True,
          OPT_AUTO_INDENT : True,
          OPT_DISPLAY_LINE_NUMBERS : True,
          OPT_HIGHLIGHT_CURRENT_LINE : True,
          OPT_BRACKET_MATCHING : False,
          OPT_DISPLAY_RIGHT_MARGIN : True,
          OPT_RIGHT_MARGIN_POSITION : 72
        },
        'ui' : {
          OPT_TOOLBAR_VISIBLE : True,
          OPT_STATUSBAR_VISIBLE : True,
          OPT_SIDE_PANEL_VISIBLE : True,
          OPT_BOTTOM_PANEL_VISIBLE : False,
          OPT_MAX_RECENTS : 10
        }
      }
    }

    PYTHON_CONFIG = {
      'plugins' : {
        OPT_ACTIVE_PLUGINS : ['docinfo', 'modelines', 'filebrowser', 'spell', 'time']
      },
      'preferences' : {
        'editor' : {
          OPT_EDITOR_FONT : 'Monospace 12',
          OPT_SCHEME : 'classic',
          OPT_CREATE_BACKUP_COPY : True,
          OPT_AUTO_SAVE : True,
          OPT_AUTO_SAVE_INTERVAL : 10,
          OPT_TABS_SIZE : 4,
          OPT_INSERT_SPACES : False,
          OPT_AUTO_INDENT : True,
          OPT_DISPLAY_LINE_NUMBERS : True,
          OPT_HIGHLIGHT_CURRENT_LINE : False,
          OPT_BRACKET_MATCHING : False,
          OPT_DISPLAY_RIGHT_MARGIN : True,
          OPT_RIGHT_MARGIN_POSITION : 80
        },
        'ui' : {
          OPT_TOOLBAR_VISIBLE : True,
          OPT_STATUSBAR_VISIBLE : True,
          OPT_SIDE_PANEL_VISIBLE : True,
          OPT_BOTTOM_PANEL_VISIBLE : True,
          OPT_MAX_RECENTS : 5
        }
      }
    }

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
        self._set_current_conf(name, self.GSCHEMA_ID_PLUGINS, '/plugins/', '.plugins')
        self._set_current_conf(name, self.GSCHEMA_ID_PREFS_EDITOR, '/preferences/editor/', '.preferences.editor')
        self._set_current_conf(name, self.GSCHEMA_ID_PREFS_UI, '/preferences/ui/', '.preferences.ui')

    def _set_current_conf(self, conf_name, conf_schema, conf_path, gedit_schema):
        in_config = self._create_config(conf_name, conf_schema, conf_path)
        out_config = self._create_gedit_conf(gedit_schema)
        for gsetting_key in in_config.keys():
            setting_type = None
            for setting in self.ALL_SETTINGS:
                if setting[0] == gsetting_key:
                    setting_type = setting[1]
            # Python power, oh yeah!!
            getattr(out_config, 'set_' + setting_type)(gsetting_key, getattr(in_config, 'get_' + setting_type)(gsetting_key))

    def _load_default_configurations(self):
        self._load_config('ruby', self.RUBY_CONFIG)
        self._load_config('python', self.RUBY_CONFIG)

    def _load_config(self, conf_name, options):
        self._load_config_set( \
          conf_name,
          self.GSCHEMA_ID_PLUGINS,
          options['plugins'],
          '/plugins/')
        self._load_config_set( \
          conf_name,
          self.GSCHEMA_ID_PREFS_EDITOR,
          options['preferences']['editor'],
          '/preferences/editor/')
        self._load_config_set(
          conf_name,
          self.GSCHEMA_ID_PREFS_UI,
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
        return '/' + self.GSCHEMA_ID_BASE.replace('.', '/') + '/' + name + setting

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
        self._ui_merge_id = manager.add_ui_from_string(self.UI_XML)
        manager.ensure_update()

    def _config_selected(self, action, data=None):
        self._set_current_profile(data)

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
