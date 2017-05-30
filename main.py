#!/usr/bin/env python
import gi
import Save
import file_dialog
import ntpath
import subprocess
import toogle
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class MyWindow(Gtk.Window):

    def __init__(self):        
        Gtk.Window.__init__(self, title="PDF Conveter")
        self.set_border_width(10)
        self.set_size_request(600,600)
        #add main box (split program into two columns)
        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(box_outer)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_size_request(300, 200)
        box_outer.pack_start(self.listbox, True, True, 0)
        self.label = Gtk.Label("elo")
        self.listbox1 = Gtk.ListBox()
        self.listbox1.set_size_request(300, 300)
        self.listbox1.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox1.add(self.label)
        box_outer.pack_start(self.listbox1, True, True, 0)
        #Rotate box with rotate buttons
        rotate_box = Gtk.Box(spacing=6)
        self.listbox1.add(rotate_box)
        self.rotate_left = Gtk.Button(label="rotate left")
        self.rotate_left.name = "left"
        self.rotate_left.connect("clicked", self.rotate)
        rotate_box.add(self.rotate_left)
        self.rotate_right = Gtk.Button(label="rotate right")
        self.rotate_right.name = "right"
        self.rotate_right.connect("clicked", self.rotate)
        rotate_box.add(self.rotate_right)
        #Displayed preview
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("click.png", 128, 256, False)
        self.pixbuf = self.pixbuf.rotate_simple(0)
        self.image = Gtk.Image()
        self.image.set_from_pixbuf(self.pixbuf)
        self.listbox1.add(self.image)
        # Split button
        self.split_button = Gtk.Button(label="Split pdf after")
        self.split_button.connect("clicked", self.split_item)
        split_box = Gtk.Box(spacing=6)
        self.listbox.add(split_box)
        split_box.pack_start(self.split_button, True, True, 0)
        # Convert button
        convert_box = Gtk.Box(spacing=6)
        self.listbox.add(convert_box)
        convert_button = Gtk.Button(label="Save as pdf..")
        convert_button.set_size_request(50,50)
        convert_button.connect("clicked", self.convert_items)
        convert_box.pack_start(convert_button, True, True, 0)
        # Add/remove box with buttons
        add_remove_box = Gtk.Box(spacing=6)
        self.listbox.add(add_remove_box)
        remove_button = Gtk.Button(label="remove")
        remove_button.connect("clicked", self.remove_item)
        add_remove_box.pack_start(remove_button, True, True, 0)
        add_button = Gtk.Button(label="add")
        add_button.connect("clicked", self.add_item)
        add_remove_box.pack_start(add_button, True, True, 0)
        up_down_box = Gtk.Box(spacing=6)
        self.listbox.add(up_down_box)
        # Navigation buttons (connected to TreeView)
        up_button = Gtk.Button(label="move up")
        up_button.set_size_request(50,50)
        up_button.connect("clicked", self.up_button_clicked)
        up_down_box.pack_start(up_button, True, True, 0)
        down_button = Gtk.Button(label="move down")
        down_button.set_size_request(50,50)
        down_button.connect("clicked", self.down_button_clicked)
        up_down_box.pack_start(down_button, True, True, 0)
        # List of files
        self.list_view_box = Gtk.Box(spacing=6)
        self.listbox.add(self.list_view_box)        
        self.createModelView()
        self.show_all()


        #Create TreeView with data which contains filename and other important settings
    def createModelView(self):
        # (filename, filepath, angle, from page, to page)
        self.store = Gtk.ListStore(str, str, int, int, int)
        self.tree = Gtk.TreeView(model=self.store)
        self.tree.set_model(self.store) 
        name_cell = Gtk.CellRendererText()
        path_cell = Gtk.CellRendererText()       
        from_column = Gtk.CellRendererText()
        to_column = Gtk.CellRendererText()
        angle_column = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Filename", name_cell, text=0)
        path_column = Gtk.TreeViewColumn("Filepath", path_cell, text=1)
        from_column = Gtk.TreeViewColumn("From", from_column, text=3)
        to_column = Gtk.TreeViewColumn("To", to_column, text=4)
        angle_column = Gtk.TreeViewColumn("Angle", angle_column, text=2)
        self.tree.append_column(name_column)
        self.tree.append_column(path_column)
        self.tree.append_column(from_column)
        self.tree.append_column(to_column)
        self.tree.append_column(angle_column)
        self.tree.get_selection().connect("changed", self.tree_view_selection_changed)
        self.list_view_box.pack_start(self.tree, True, True, 0)
        

        # Event which occurs when selected row is changed
    def tree_view_selection_changed(self, widget):
        (model, iter) = widget.get_selected()
        self.selected_index = iter
          
        print("change position to %s number", self.store[self.selected_index][0])
        selected_file = self.store[self.selected_index][1]
        if (selected_file.endswith('.pdf') | selected_file.endswith('.doc')):
            self.split_button.set_sensitive(True)
            self.rotate_right.set_sensitive(True)
            self.rotate_left.set_sensitive(True)
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("click.png", 128, 256, False)
            self.pixbuf = self.pixbuf.rotate_simple(self.store[self.selected_index][2])
            self.image.set_from_pixbuf(self.pixbuf)
        elif (selected_file.endswith('.jpg') | selected_file.endswith('.png')):
            self.split_button.set_sensitive(False)
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.store[iter][1], 128, 256, False)  
            self.pixbuf = self.pixbuf.rotate_simple(self.store[self.selected_index][2])      
            self.image.set_from_pixbuf(self.pixbuf)
            self.rotate_right.set_sensitive(True)
            self.rotate_left.set_sensitive(True)  
        else:
            self.split_button.set_sensitive(False)
            self.rotate_right.set_sensitive(False)
            self.rotate_left.set_sensitive(False)
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("click.png", 128, 256, False)
            self.image.set_from_pixbuf(self.pixbuf)
        # Deleting selected row in TreeView (triggered by remove_button)
    def remove_item(self, widget):
        print("remove")
        self.store.remove(self.selected_index)
    

        # Function clones one file into 2 files with specified page range (pdf only)
    def split_item(self, widget):
        toogle_dialog = toogle.SpinButtonWindow()
        toogle_dialog.get_page_number(self)
        
    
    def set_page_range(self, number):
        print(str(number))
        
        if (self.store[self.selected_index][1].endswith('.pdf') | self.store[self.selected_index][1].endswith('.doc') ):           
            self.store[self.selected_index][4] = number
            duplicate = self.store[self.selected_index]
            self.store.append([duplicate[0], duplicate[1], 0, number + 1, 999])


        # Rotate selected item 
    def rotate(self, widget):
        if widget.name == "right":
            print("rotating right")
            self.pixbuf = self.pixbuf.rotate_simple(270)
            self.setNewAngle(270)
        elif widget.name == "left":
            print("rotating left")
            self.pixbuf = self.pixbuf.rotate_simple(90)
            self.setNewAngle(90)
        self.image.set_from_pixbuf(self.pixbuf)


        #Additional function which check angle (decrease range of angles to 0-360 degrees)
    def setNewAngle(self, angle):
        self.store[self.selected_index][2] += angle
        if self.store[self.selected_index][2] >= 360:
            self.store[self.selected_index][2] -= 360
        print(self.store[self.selected_index][2])


        #Function open new file dialog to select destination of new pdf file
    def convert_items(self, widget):
        save = Save.SaveWindow()
        self.save_filepath = save.button_pressed()
        # subprocess.call(["ls", "-l"])
        print("saving")
        self.save_items()


        # Serialization data and opening bash script
    def save_items(self):
        bufferfile = open('data.txt', 'w')
        for item in self.store:
            bufferfile.write(item[1] + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t" + str(item[4]) + "\n")
        bufferfile.close()
        print(self.get_filename(bufferfile.name))
        subprocess.call(["bash", "script.sh", self.save_filepath])


        #Function adds new file to list from filedialog        
    def add_item(self, widget):
        print("add")
        win = file_dialog.FileChooserWindow()
        win.open_file_dialog(self)
    

        # Load filedialog window notify main function about new file 
    def notify(self, path):
        filename = self.get_filename(path)     
        self.store.append([filename, path, 0, 0, 999])


        #Function gets extension of file
    def get_filename(self, path):
        head, tail = ntpath.split(path)
        return tail


        # move to next selected item in TreeView
    def up_button_clicked(self, widget):
        print("Moved up")
        index = self.selected_index
        up_index = self.store.iter_previous(index)
        if(up_index):
            self.store[index][0], self.store[up_index][0] = self.store[up_index][0], self.store[index][0]
            self.store[index][1], self.store[up_index][1] = self.store[up_index][1], self.store[index][1]        
            tree_selection = self.tree.get_selection()
            tree_selection.select_iter(up_index)
        
        
        # move to previous selected item in TreeView
    def down_button_clicked(self, widget):
        print("Moved down")
        index = self.selected_index
        down_index = self.store.iter_next(index)
        if(down_index):
            self.store[index][0], self.store[down_index][0] = self.store[down_index][0], self.store[index][0]
            self.store[index][1], self.store[down_index][1] = self.store[down_index][1], self.store[index][1]
            tree_selection = self.tree.get_selection()
            tree_selection.select_iter(down_index)
        

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()