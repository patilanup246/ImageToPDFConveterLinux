from gi.repository import Gtk

class SaveWindow(Gtk.Window):

    def add_filters(self, dialog):
        #Add text file filter
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text Files")
        filter_text.add_mime_type("application/pdf")
        dialog.add_filter(filter_text)

    def button_pressed( self ):
        dialog = Gtk.FileChooserDialog("Save your text file", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(800, 400)

        self.add_filters(dialog)

        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)

        Gtk.FileChooser.set_current_name(dialog, "document.pdf")
        
        response = dialog.run()
            
        if response == Gtk.ResponseType.ACCEPT:

            filename = Gtk.FileChooser.get_filename(dialog)
            print "This is the filename: " + filename
            

        dialog.destroy()
        return filename