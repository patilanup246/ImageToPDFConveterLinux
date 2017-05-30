import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SpinButtonWindow:
    
    def get_page_number(self, obj):
        self.dialog = Gtk.Window(title="SpinButton Demo")
        
        hbox = Gtk.Box(spacing=6)
        self.dialog.add(hbox)
        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(adjustment)
        hbox.pack_start(self.spinbutton, False, False, 0)
        self.ok_button = Gtk.Button(label="OK")
        self.ok_button.connect("clicked", self.set_range)
        hbox.pack_start(self.ok_button, False, False, 0)

        self.observer = obj

        self.dialog.show_all()


    def set_range(self, widget):
        self.observer.set_page_range(self.spinbutton.get_value_as_int())
        self.dialog.destroy()


        
