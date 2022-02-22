import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from re import sub
from json import load, dump
from os import startfile
from random import choice


class MainFrame:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.notebook = ttk.Notebook(self.master)
        self.menu = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Add a tab...", command=self.add_tab)
        self.filemenu.add_command(label="Add an app to the existing tab...", command=self.add_app)
        self.filemenu.add_command(label="Delete a tab or an app...", command=self.del_tab)
        self.btn_ok = []
        self.btn_random = []
        self.radiobuttons = []
        with open("data.json", "r") as apps: self.apps = load(apps)
        self.rad_var = tk.StringVar(value=f"{list(self.apps.keys())[0]} 0")
        for i, elem in enumerate(tabs := [tk.Frame(self.notebook) for _ in range(len(self.apps.keys()))]):
            self.notebook.add(elem, text=list(self.apps.keys())[i])
        for i, item in enumerate(self.apps.items()):
            for j in range(len(item[1])):
                self.radiobuttons.append(ttk.Radiobutton(tabs[i], text=item[1][j][0], value=f"{item[0]} {j}", variable=self.rad_var))
                self.radiobuttons[-1].grid(column=1, row=j, padx=60, pady=0)
        for i, elem in enumerate(tabs):
            self.btn_ok.append(ttk.Button(elem, text="Start", command=MainFrame.quiter(
                lambda: startfile(self.apps[self.rad_var.get().split()[0]][int(self.rad_var.get().split()[1])][1]))))
            self.btn_ok[-1].grid(column=1, row=100, padx=0, pady=10)
            self.btn_random.append(ttk.Button(elem, text="Random start", command=MainFrame.quiter(
                lambda: startfile(choice(self.apps[self.rad_var.get().split()[0]])[1]))))
            self.btn_random[-1].grid(column=1, row=101, padx=0, pady=10)
        self.notebook.pack(expand=1, fill='both')

    @staticmethod
    def quiter(func):
        def wrapper():
            func()
            exit()
        return wrapper

    def add_tab(self):
        self.app = AddTab(tk.Toplevel(self.master))

    def add_app(self):
        self.app = AddApp(tk.Toplevel(self.master))

    def del_tab(self):
        self.app = DelTab(tk.Toplevel(self.master))


class AddTab:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text="Enter the name of the tab:")
        self.tab_name = tk.StringVar()
        self.entry = ttk.Entry(self.master, textvariable=self.tab_name)
        self.apply_button = tk.Button(self.master, text="Apply", command=self.update_data)
        self.label.grid(column=0, row=0, padx=5, pady=10)
        self.entry.grid(column=2, row=0, padx=5, pady=10)
        self.apply_button.grid(column=1, row=1, padx=0, pady=10)

    def update_data(self):
        if var := self.tab_name.get():
            with open("data.json", "r") as file: a = load(file)
            if var in a:
                try: self.label_success.grid_remove()
                except AttributeError: pass
                self.label_error = tk.Label(self.master, text="This tab is already exist!")
                self.label_error.grid(column=0, row=2, padx=5, pady=10)
            else:
                try: self.label_error.grid_remove()
                except AttributeError: pass
                a[var] = []
                with open("data.json", "w") as file: dump(a, file)
                self.label_success = tk.Label(self.master, text="The tab has been added successfully!")
                self.label_success.grid(column=0, row=2, padx=5, pady=10)


class AddApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.tab_label = tk.Label(self.master, text="Tab:")
        self.name_label = tk.Label(self.master, text="App label:")
        self.path_label = tk.Label(self.master, text="Path:")
        self.tab_var, self.name_var, self.path_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        with open("data.json", "r") as file: self.tab_combobox = ttk.Combobox(self.master, values=list(load(file).keys()), state="readonly", textvariable=self.tab_var)
        self.name_entry = ttk.Entry(self.master, textvariable=self.name_var)
        self.path_entry = ttk.Entry(self.master, textvariable=self.path_var)
        self.path_button = ttk.Button(self.master, text="...", command=lambda: self.path_var.set(fd.askopenfilename(initialdir="/", parent=self.master)))
        self.apply_button = ttk.Button(self.master, text="Apply", command=self.update_data)
        self.tab_label.grid(column=0, row=0, padx=5, pady=10)
        self.name_label.grid(column=0, row=1, padx=5, pady=10)
        self.path_label.grid(column=0, row=2, padx=5, pady=10)
        self.tab_combobox.grid(column=1, row=0, padx=0, pady=10)
        self.name_entry.grid(column=1, row=1, padx=0, pady=10)
        self.path_entry.grid(column=1, row=2, padx=0, pady=10)
        self.path_button.grid(column=2, row=2, padx=5, pady=10)
        self.apply_button.grid(column=1, row=4, padx=0, pady=10)

    def update_data(self):
        with open("data.json", "r") as file: a = load(file)
        if (tab_var := self.tab_var.get()) and (name_var := self.name_var.get()) and (path_var := self.path_var.get()):
            path_var = sub(r"\\{1,2}", "/", path_var).replace("\"", "")
            a[tab_var].append([name_var, path_var])
            with open("data.json", "w") as file: dump(a, file)
            try: self.label_error.grid_remove()
            except AttributeError: pass
            self.label_success = tk.Label(self.master, text=f'The app has been added successfully!')
            self.label_success.grid(column=1, row=3, padx=0, pady=0)
        else:
            try: self.label_success.grid_remove()
            except AttributeError: pass
            self.label_error = tk.Label(self.master, text=f'All entries must be filled!')
            self.label_error.grid(column=1, row=3, padx=0, pady=0)


class DelTab:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text="Enter the name of the tab:")
        self.tab_combo_var, self.radio_var, self.is_combobox_created = tk.StringVar(), tk.IntVar(value=0), False
        self.tab_radio = ttk.Radiobutton(self.master, text="Tabs", value=0, variable=self.radio_var, command=self.update_listbox)
        self.app_radio = ttk.Radiobutton(self.master, text="Apps", value=1, variable=self.radio_var, command=self.update_listbox)
        self.listbox = tk.Listbox(self.master)
        with open("data.json", "r") as file:
            self.listbox.insert(tk.END, *(load(file).keys()))
        self.apply_button = tk.Button(self.master, text="Delete", command=self.update_data)
        self.tab_radio.grid(column=1, row=0, padx=5, pady=10)
        self.app_radio.grid(column=2, row=0, padx=5, pady=10)
        self.listbox.grid(column=0, row=1, padx=5, pady=10)
        self.label.grid(column=0, row=0, padx=5, pady=10)
        self.apply_button.grid(column=2, row=1, padx=0, pady=10)

    def update_listbox(self):
        with open("data.json", "r") as file: a = load(file)
        self.listbox.delete(0, tk.END)
        if self.radio_var.get():
            self.tab_combo = ttk.Combobox(self.master, values=list(a.keys()), state="readonly", textvariable=self.tab_combo_var)
            if not self.is_combobox_created:
                self.tab_combo.current(0)
                self.is_combobox_created = True
            self.tab_combo.grid(column=3, row=0, padx=5, pady=10)
            for i in a[self.tab_combo_var.get()]:
                self.listbox.insert(tk.END, i[0])
        else:
            self.tab_combo.grid_remove()
            for i in a.keys():
                self.listbox.insert(tk.END, i)

    def update_data(self):
        with open("data.json", "r") as file: a = load(file)
        if self.radio_var.get():
            for i, elem in enumerate(a[self.tab_combo_var.get()]):
                if elem[0] == self.listbox.get(self.listbox.curselection()):
                    a[self.tab_combo_var.get()].pop(i)
                    with open("data.json", "w") as file: dump(a, file)
                    self.label_success = tk.Label(self.master, text="Deleted successfully!")
                    self.label_success.grid(column=0, row=2, padx=5, pady=10)
                    break
        else:
            a.pop(self.listbox.get(self.listbox.curselection()))
            with open("data.json", "w") as file: dump(a, file)
            self.label_success = tk.Label(self.master, text="Deleted successfully!")
            self.label_success.grid(column=0, row=2, padx=5, pady=10)
        self.listbox.delete(self.listbox.curselection())


def main():
    root = tk.Tk()
    app = MainFrame(root)
    root.title("Launcher")
    root.config(menu=app.menu)
    root.mainloop()


if __name__ == '__main__':
    main()
