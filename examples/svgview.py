#!/usr/bin/env python

# TODO
# draw frame round pic to show its borderline
# Zoom-in/out toolbutton


import os

import gtk
import cairo
import cairo.svg
import cairo.gtk


action_list = [
    ('FileMenu',   None,                 '_File'),
    ('Open',       gtk.STOCK_OPEN,       '_Open',       '<CTL>O',      'Open a file',       'cb_open'),
    ('Quit',       gtk.STOCK_QUIT,       '_Quit',       '<CTL>Q',      'Quit application',  'cb_quit'),
    ]

ui_string = """<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='Open'/>
      <separator name='s1'/>
      <menuitem action='Quit'/>
    </menu>
  </menubar>
</ui>"""


def fix_actions (actions, instance):
    "UIManager Helper function to map method strings to an instance method"
    retval = []
    
    for action in actions:
        if len (action) >= 6:     # action[5] is the callcack function as a string
            action = action[0:5] + (getattr (instance, action[5]),) + action[6:]
        retval += [action]
    return retval


class Window (gtk.Window):
    def __init__ (self, title=None, type=gtk.WINDOW_TOPLEVEL):
        gtk.Window.__init__ (self, type)
        if title:
            self.set_title (title)
        self.set_default_size(300, 200)

        self.pixmap = None

        vbox = gtk.VBox()
        self.add (vbox)

        # create UIManager menus
        ag = gtk.ActionGroup ('WindowActions')
        actions        = fix_actions (action_list, self)
        ag.add_actions (actions)
        
        self.ui = gtk.UIManager()
        self.ui.insert_action_group (ag, 0)
        self.add_accel_group (self.ui.get_accel_group())

        try:
            self.ui.add_ui_from_string (ui_string)
        except gobject.GError, exc:
            print 'uimanager.add_ui_from_string() error:', exc
        else:
            path = '/MenuBar'
            menubar = self.ui.get_widget (path)
            if menubar:
                vbox.pack_start (menubar, expand=False)
            else:
                print "Error: uimanager.get_widget('%s') failed" % path

        self.fileselect = MyFileChooserDialog(parent=self)

        self.da = gtk.DrawingArea()
        vbox.pack_start (self.da, expand=True)
        def cb_expose_event (da, event, data=None):
            if self.pixmap:
                # center on screen
                xdest = max (0, (da.allocation.width -da.svg_width)//2)
                ydest = max (0, (da.allocation.height-da.svg_height)//2)
                self.da.window.draw_drawable(self.style.bg_gc[gtk.STATE_NORMAL],
                                             self.pixmap,
                                             0, 0, xdest, ydest, -1, -1)
        self.da.connect ('expose-event', cb_expose_event)
            

    def cb_open (self, action, data=None):
        """Open svg file (if one is selected) and render to an off-screen
        pixmap
        """
        filename = self.fileselect.get_filename_from_user()
        if filename == None:
            return

        svg = cairo.svg.Context()
        try:
            svg.parse (filename)
        except Exception, exc:
            print exc
            return
            
        width, height = svg.size
        self.da.svg_width, self.da.svg_height = width, height

        ctx = cairo.Context()
        self.pixmap = gtk.gdk.Pixmap (self.da.window, width, height)
        self.pixmap.draw_rectangle (self.style.bg_gc[gtk.STATE_NORMAL], True, 0, 0, width, height)

        cairo.gtk.set_target_drawable(ctx, self.pixmap)
        svg.render (ctx)
        self.da.queue_draw()


    def cb_quit (self, action, data=None):  
        gtk.main_quit()


class MyFileChooserDialog (gtk.FileChooserDialog):
    """A custom GtkFileSelection class that gets a filename from a user and
    remembers the current dir the next time the fileselection is used.
    """
    def __init__ (self,
                  title   = 'Select a file',
                  parent  = None,
                  action  = gtk.FILE_CHOOSER_ACTION_OPEN,
                  buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                             gtk.STOCK_OPEN,   gtk.RESPONSE_OK),
                  backend = '',
                  path    = None):
       super (MyFileChooserDialog, self).__init__ (title, parent, action, buttons, backend)

       if path: self.path = path
       else:    self.path = os.getcwd() + os.sep

       ffilter = gtk.FileFilter()
       ffilter.set_name ("SVG files")
       ffilter.add_pattern ("*.svg")
       self.add_filter (ffilter)

       ffilter = gtk.FileFilter()
       ffilter.set_name ("All files")
       ffilter.add_pattern ("*")
       self.add_filter (ffilter)

       # previews
       self.preview = gtk.Image()
       self.set_preview_widget (self.preview)
       self.connect ("update-preview", self.update_preview_cb)

    def update_preview_cb(self, widget, data=None):
        filename = self.get_preview_filename()
        if filename is None or not os.path.isfile(filename):
            self.set_preview_widget_active (False)
            return

        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size (filename, 128, 128)
            self.preview.set_from_pixbuf (pixbuf)
            self.set_preview_widget_active (True)
        except Exception, exc:
            self.set_preview_widget_active (False)
            

    def get_filename_from_user (self, path=None, title=None):
        if path:  self.path = path
        if title: self.set_title (title)
        if self.path.endswith (os.sep):
            self.set_current_folder (self.path)
        else:
            self.set_filename (self.path)
                
        filename = None
        if self.run() == gtk.RESPONSE_OK:
            self.path = filename = self.get_filename()
        self.hide()
        return filename


if __name__ == '__main__':
    app = Window (title='SVGView')
    app.connect('destroy', gtk.main_quit)
    app.show_all()
    gtk.main()
