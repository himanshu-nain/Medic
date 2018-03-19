import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from dbutils import getDiseases, init
from classifier import classifier


class Main_Window(Gtk.Window):



    def __init__(self):
        #WINDOW DESCRIPTION

        Gtk.Window.__init__(self, title = "Medical App")
        self.set_border_width(10)
        self.set_default_size(850, 500)


        #MAKING BOXES

        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.vbox1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        self.vbox2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)



        main_menu_bar = Gtk.MenuBar()

        #FILE MENU

        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem("File")

        file_new = Gtk.MenuItem("New")
        file_save = Gtk.MenuItem("Save")
        file_exit = Gtk.MenuItem("Exit")

        file_exit.connect("activate", Gtk.main_quit)
        file_save.connect("activate", self.save_file)
        file_new.connect("activate", self.new_file)

        file_menu_dropdown.set_submenu(file_menu)

        file_menu.append(file_new)
        file_menu.append(file_save)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(file_exit)

        main_menu_bar.append(file_menu_dropdown)


        #ADDING MENU BAR IN THE BOX

        self.hbox.pack_start(main_menu_bar, True, True, 0)


        #ADDING VERTICAL BOX INSIDE THE HORIZONTAL BOX

        self.hbox.pack_start(self.vbox1, True, True, 0)
        boxseparator = Gtk.Separator(orientation = Gtk.Orientation. VERTICAL)
        self.hbox.pack_start(boxseparator, True, True, 0)
        self.hbox.pack_start(self.vbox2, True, True, 0)




        #PATIENT'S DETAILS FILL

        self.label_name = Gtk.Label("Patient's Name : ")
        self.vbox1.pack_start(self.label_name, False, True, 0)
        self.name = Gtk.Entry()
        self.vbox1.pack_start(self.name, False, True, 5)

        self.label_age = Gtk.Label("Patient's Age : ")
        self.vbox1.pack_start(self.label_age, False, True, 0)
        self.age = Gtk.Entry()
        self.vbox1.pack_start(self.age, False, True, 5)

        label_address = Gtk.Label("Patient's Address :")
        self.vbox1.pack_start(label_address, False, True, 0)
        self.address = Gtk.Entry()
        self.vbox1.pack_start(self.address, False, True, 5)

        label_number = Gtk.Label("Patient's Phone Number : ")
        self.vbox1.pack_start(label_number, False, True, 0)
        self.number = Gtk.Entry()
        self.vbox1.pack_start(self.number, False, True, 5)



        #SYMPTOMS DETAILS
        self.symptom1 = Gtk.Entry()
        self.symptom1.set_placeholder_text("(Compulsory)")
        self.symptom2 = Gtk.Entry()
        self.symptom2.set_placeholder_text("(Compulsory)")
        self.symptom3 = Gtk.Entry()
        self.symptom3.set_placeholder_text("(Optional)")
        self.symptom4 = Gtk.Entry()
        self.symptom4.set_placeholder_text("(Optional)")
        self.symptom5 = Gtk.Entry()
        self.symptom5.set_placeholder_text("(Optional)")

        label_symptom = Gtk.Label("Symptoms : ")
        self.vbox2.pack_start(label_symptom, False, True, 0)

        label_info = Gtk.Label("Please enter symptoms from the list available")
        self.vbox2.pack_start(label_info, False, True, 0)

        self.vbox2.pack_start(self.symptom1, False, True, 5)
        self.vbox2.pack_start(self.symptom2, False, True, 5)
        symptom_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox2.pack_start(symptom_separator, False, True, 0)
        self.vbox2.pack_start(self.symptom3, False, True, 5)
        self.vbox2.pack_start(self.symptom4, False, True, 5)
        self.vbox2.pack_start(self.symptom5, False, True, 5)


        #SET COMPLETION MODE IN THE SYMPTOMS

        completion1 = Gtk.EntryCompletion()
        completion2 = Gtk.EntryCompletion()
        completion3 = Gtk.EntryCompletion()
        completion4 = Gtk.EntryCompletion()
        completion5 = Gtk.EntryCompletion()
        self.liststore = Gtk.ListStore(str)
        problems = []
        with open("sym.txt") as filename:
            for line in filename:
                problems.append(line.strip('\n'))

        for text in problems:
            self.liststore.append([text])

        problems.remove('')
        self.treeview = Gtk.TreeView(self.liststore)


        completion1.set_model(self.liststore)
        completion2.set_model(self.liststore)
        completion3.set_model(self.liststore)
        completion4.set_model(self.liststore)
        completion5.set_model(self.liststore)
        completion1.set_text_column(0)
        completion2.set_text_column(0)
        completion3.set_text_column(0)
        completion4.set_text_column(0)
        completion5.set_text_column(0)

        self.symptom1.set_completion(completion1)
        self.symptom2.set_completion(completion2)
        self.symptom3.set_completion(completion3)
        self.symptom4.set_completion(completion4)
        self.symptom5.set_completion(completion5)

        # if len(self.symptom1.get_text()) != 0:
        #     for i in problems:
        #         if self.symptom1.get_text() != i:
        #             dialog_entry_error = Error(self)
        #             response = dialog_entry_error.run()
        #             dialog_entry_error.destroy()
        #             break
        #
        # if len(self.symptom2.get_text()) != 0:
        #     for i in problems:
        #         if self.symptom2.get_text() != i:
        #             dialog_entry_error = Error(self)
        #             response = dialog_entry_error.run()
        #             dialog_entry_error.destroy()
        #             break
        #
        # if len(self.symptom3.get_text()) != 0:
        #     for i in problems:
        #         if self.symptom3.get_text() != i:
        #             dialog_entry_error = Error(self)
        #             response = dialog_entry_error.run()
        #             dialog_entry_error.destroy()
        #             break
        #
        #
        # if len(self.symptom4.get_text()) != 0:
        #     for i in problems:
        #         if self.symptom4.get_text() != i:
        #             dialog_entry_error = Error(self)
        #             response = dialog_entry_error.run()
        #             dialog_entry_error.destroy()
        #             break
        #
        # if len(self.symptom5.get_text()) != 0:
        #     for i in problems:
        #         if self.symptom5.get_text() != i:
        #             dialog_entry_error = Error(self)
        #             response = dialog_entry_error.run()
        #             dialog_entry_error.destroy()
        #             break


        #SUBMIT BUTTON

        self.submit = Gtk.Button("Submit")
        self.submit.connect("clicked", self.submit_clicked)
        self.vbox2.pack_start(self.submit, False, True, 5)
        #ADD HORIZONTAL BOX TO THE WINDOW WHICH CONTAINS ALL THE BOXES

        self.add(self.hbox)




    def submit_clicked(self, widget):
        if(len(self.symptom1.get_text()) == 0 or len(self.symptom2.get_text()) == 0):
            dialog_error = PopUp(self)
            response = dialog_error.run()

            dialog_error.destroy()
            return

        list = []
        list.append([self.symptom1.get_text(), self.symptom2.get_text()])
        if(len(self.symptom3.get_text())>0):
            list.append(self.symptom3.get_text())
        if (len(self.symptom4.get_text()) > 0):
            list.append(self.symptom4.get_text())
        if (len(self.symptom5.get_text()) > 0):
            list.append(self.symptom5.get_text())

        #TODO CALL HIMANSHU NAIN FOR THE DISEASE
        init()
        all_Diseases = getDiseases(list)

        disease = classifier(all_Diseases, list)

        dialog_answer = Answer(self, disease)
        response = dialog_answer.run()

        dialog_answer.destroy()







    def new_file(self, widget):
        #TODO IMPROVEMENT

        open("Hack_app.py")


    def save_file(self, widget):
        c = canvas.Canvas(self.name.get_text(), pagesize=A4)

        c.setFont('Helvetica', 20, leading=None)
        c.drawString(240, 810, "Patient's Details")
        c.setFont('Helvetica', 16, leading = None)
        c.drawString(5, 750, "Name : ")
        c.setFont('Helvetica', 16, leading = None)
        c.drawString(70, 750, self.name.get_text())
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 710, "Age : ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(70,710, self.age.get_text())
        c.setFont('Helvetica', 20, leading=None)
        c.drawString(270, 650, "Symptoms")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 590, "1. ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(20, 590, self.symptom1.get_text())
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(5, 550, "2. ")
        c.setFont('Helvetica', 16, leading=None)
        c.drawString(20, 550, self.symptom2.get_text())
        if len(self.symptom3.get_text()) != 0:
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5, 510, "3. ")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 510, self.symptom3.get_text())
        if len(self.symptom4.get_text()) != 0:
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5, 470, "4. ")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 470, self.symptom4.get_text())
        if len(self.symptom5.get_text()) != 0:
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(5,430, "5. ")
            c.setFont('Helvetica', 16, leading=None)
            c.drawString(20, 430, self.symptom5.get_text())

        c.showPage()
        c.save()







class PopUp(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100, 50)
        self.set_border_width(20)

        area = self.get_content_area()
        area.add(Gtk.Label("Atleast Two Symptoms are required."))
        self.show_all()




class Answer(Gtk.Dialog):



    def __init__(self, parent, disease):

        Gtk.Dialog.__init__(self, "Disease", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100,50)
        self.set_border_width(20)
        self.disease = disease
        area = self.get_content_area()
        area.add(Gtk.Label("The Possible Disease Patient is suffering from is " + self.disease))
        self.show_all()



class Error(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Error", parent, Gtk.DialogFlags.MODAL, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(100, 50)
        self.set_border_width(20)
        area = self.get_content_area()
        area.add(Gtk.Label("The Entered Symptom is Wrong."))
        self.show_all()














window = Main_Window()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()