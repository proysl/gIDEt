from constants import *

RUBY_CONFIG = {
  'plugins' : {
    OPT_ACTIVE_PLUGINS : ['configmaster', 'docinfo', 'modelines', 'filebrowser', 'spell', 'terminal', 'time']
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
    OPT_ACTIVE_PLUGINS : ['configmaster', 'codecomments', 'docinfo', 'modelines', 'filebrowser', 'pythonconsole', 'spell', 'time']
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
