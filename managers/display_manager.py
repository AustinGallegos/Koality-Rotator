import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.interfaces import BusinessLogicInterface


def create_textbox(title, save_file):
    def decorator(func):
        """Creates textbox template."""

        def wrapper(self):
            chars = func(self)
            self.text_window = tk.Tk()
            self.text_window.title(title)
            self.text_window.protocol("WM_DELETE_WINDOW", self.close_text)
            self.text_window.iconbitmap(self.koala)
            self.text_box = tk.Text(self.text_window)
            self.text_box.insert(tk.END, chars=chars)

            save_button = ttk.Button(self.text_window, text="Save", width=20, command=None)
            if save_file == "perms":
                save_button.config(command=lambda: self.save_permissions(self.text_box))
            elif save_file == "res":
                save_button.config(text="Main Menu", command=self.main_menu)
            else:
                save_button.config(command=lambda: self.save_textbox(save_file))

            save_button.place(x=480, y=10)

            scrollbar = tk.Scrollbar(self.text_window, orient="vertical", command=self.text_box.yview)
            scrollbar.pack(side="right", fill="y")
            self.text_box.config(yscrollcommand=scrollbar.set)

            self.text_box.pack()
            self.center_window(self.text_window, 630, 300)
            self.text_window.mainloop()

        return wrapper

    return decorator


class DisplayManager:
    def __init__(self, paths_dict, business_logic: BusinessLogicInterface, driver=None):
        self.driver = driver
        self.paths_dict = paths_dict
        self.business_logic = business_logic

        self.curr_date = dt.datetime.now() + dt.timedelta(days=1)
        self.year = self.curr_date.strftime("%Y")
        self.month = self.curr_date.strftime("%m")
        self.day_number = self.curr_date.strftime("%d")

        self.setup_window()

        self.setup_widgets()

        self.text_window = None
        self.text_box = None
        self.roles = None
        self.entry_dict = {}

        self.create_roles()

    def setup_window(self):
        """Set up the Tkinter window."""
        self.window = tk.Tk()
        self.window.title("Koality Rotator")
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)

        self.koala = self.paths_dict["koala_logo"]
        self.window.iconbitmap(self.koala)
        self.center_window(self.window, 500, 600)

    def center_window(self, window, width, height):
        """Centers the open Tkinter window."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        window.update_idletasks()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y - 40}")

    def close_app(self):
        """Close the app and quit the driver properly."""
        self.window.destroy()
        if self.driver:
            self.driver.quit()

    def close_text(self):
        """Close the text window and quit the driver properly."""
        self.text_window.destroy()
        if self.driver:
            self.driver.quit()

    def setup_widgets(self):
        """Set up all the widgets on the window."""
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, width=500, height=600, bg="#1399FF")
        self.canvas.create_text(260, 60, text="Koality Rotator", font=("Helvetica", 20, "bold"))
        self.canvas.create_text(420, 60, text="(created by galleaus)", font=("Helvetica", 8, "bold"))

        self.setup_canvas_scrollbar()

        self.create_shift_dropdown()
        self.create_site_label()
        self.create_date_entry()
        self.create_buttons()
        self.create_image()

    def setup_canvas_scrollbar(self):
        """Set up the scrollbar for the canvas."""
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure())

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self):
        """Update the scrollable region of the canvas whenever the content changes"""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_shift_dropdown(self):
        """Create a dropdown widget for selecting a shift."""
        self.shifts = self.business_logic.get_shifts()
        self.shifts = self.shifts.split("\n")[:-1]
        self.canvas.create_text(75, 100, text="Select a Shift:", font=("Helvetica", 12, "bold"))
        self.dropdown_widget = ttk.Combobox(self.window, values=self.shifts)
        self.dropdown_widget.set("Select a shift")
        self.canvas.create_window(250, 100, window=self.dropdown_widget)

    def create_site_label(self):
        """Create the site label."""
        self.site = self.business_logic.get_site().upper()
        self.site_text = self.canvas.create_text(435, 100, text=f"Site: {self.site}", font=("Helvetica", 12, "bold"))

    def create_date_entry(self):
        """Create the date entry field."""
        self.canvas.create_text(73, 132, text="Type a Date:", font=("Helvetica", 12, "bold"))
        self.date_entry = ttk.Entry(width=23)
        self.date_entry.insert(0, string=f"{self.month}-{self.day_number}-{self.year}")
        self.canvas.create_window(250, 132, window=self.date_entry)

    def create_buttons(self):
        """Create all the buttons on the window."""
        style = ttk.Style()
        style.configure("TButton", padding=(0, 35, 0, 32), font=("Helvetica", 10))

        down_button = tk.Button(text="↓", width=1, command=lambda: self.change_date("down"))
        up_button = tk.Button(text="↑", width=1, command=lambda: self.change_date("up"))
        change_site_button = tk.Button(text="Change Site", width=10, command=self.change_site)
        change_shifts_button = tk.Button(text="Change Shifts", width=10, command=self.change_shifts)
        generate_button = ttk.Button(text="Generate", width=35, command=self.generate_button_click)
        permissions_button = ttk.Button(text="Check/Edit Permissions", width=35,
                                        command=self.check_permissions)
        default1 = tk.Button(text="Default Refurb",
                             command=lambda: self.default("REF"))
        default2 = tk.Button(text="Default AR",
                             command=lambda: self.default("AR"))
        reset_button = tk.Button(text="Reset",
                                 command=self.reset_entries)
        add_remove_button = tk.Button(text="Add/Remove Roles",
                                      command=self.add_remove_roles)

        self.canvas.create_window(335, 132, window=down_button)
        self.canvas.create_window(355, 132, window=up_button)
        self.canvas.create_window(435, 132, window=change_site_button)
        self.canvas.create_window(435, 165, window=change_shifts_button)
        self.canvas.create_window(250, 200, window=generate_button)
        self.canvas.create_window(250, 385, window=permissions_button)
        self.canvas.create_window(60, 465, window=default1)
        self.canvas.create_window(60, 500, window=default2)
        self.canvas.create_window(60, 535, window=reset_button)
        self.canvas.create_window(410, 465, window=add_remove_button)

        self.canvas.create_line(0, 445, 500, 445, fill="black", width=2)

    def change_date(self, direction):
        """Adjust the current date up or down by one day and update the entry field."""
        if direction == "down":
            self.curr_date = self.curr_date - dt.timedelta(days=1)
        elif direction == "up":
            self.curr_date = self.curr_date + dt.timedelta(days=1)

        self.year = self.curr_date.strftime("%Y")
        self.month = self.curr_date.strftime("%m")
        self.day_number = self.curr_date.strftime("%d")

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, string=f"{self.month}-{self.day_number}-{self.year}")

    def change_site(self):
        """Writes Site ID file to change Site ID on main menu and when AA schedules are pulled."""
        try:
            self.site = simpledialog.askstring("Change Site", "Please enter your site:").upper()
            self.business_logic.save("site", [self.site])  # self.site string has to be in a list
            self.canvas.delete(self.site_text)
            self.site_text = self.canvas.create_text(435, 100, text=f"Site: {self.site}",
                                                     font=("Helvetica", 12, "bold"))
        except AttributeError:
            pass

    @create_textbox("Change Shifts", "saved_shifts")
    def change_shifts(self):
        """Writes shift start times that are used to find AA schedules."""
        messagebox.showinfo(title="Shifts Input", message="Please ensure all shifts are entered as follows:\nHH-MM-00")
        shifts = self.business_logic.get_shifts()
        return shifts

    def save_permissions(self, text):
        """Saves permissions in the check/edit permissions textbox to files on the user's PC."""
        saved = self.business_logic.save_permissions(text)
        self.text_window.destroy()
        if not saved:
            tk.messagebox.showinfo(title="Error",
                                   message="Error: Changes not saved.\n\nIf you need to add or remove roles, "
                                           "please do so on the main menu by clicking 'Add/Remove Roles.'")
        else:
            tk.messagebox.showinfo(title="Saved!", message="Permissions Saved!")

    def save_textbox(self, filename):
        """Saves the content in the given textbox to a file on the user's PC."""
        text = self.text_box.get("1.0", "end-1c").split("\n")
        text = [item for item in text if item != ""]
        self.business_logic.save(filename, text)

        self.text_window.destroy()
        tk.messagebox.showinfo(title="Saved!",
                               message="Saved!")

        self.window.destroy()
        DisplayManager(self.paths_dict, self.business_logic, self.driver)

    def generate_button_click(self):
        """Initiates Selenium Web Driver to find AA schedules, assign AAs to indirect roles."""
        if self.check_invalid_entries():
            return

        if self.check_dropdown():
            return

        if self.check_date():
            return

        if self.proceed():
            return

        self.get_nums_dict()

        self.window.destroy()

        if self.get_scheduled_associates():
            return

        self.assign_indirects()

        self.create_result_textbox()

    def check_invalid_entries(self):
        """Check role entries for invalid or all-zero values and display error messages."""
        all_zero = True
        for role in self.roles:
            error = self.check_entry(role)
            if error == ValueError:
                messagebox.showinfo(title="Error", message="All role entries must contain valid integers (greater "
                                                           "than or equal to 0).")
                return True
            elif not error:
                all_zero = False

        if all_zero:
            messagebox.showinfo(title="Error",
                                message="All role entries are 0.\n\n"
                                        "Please enter at least one role entry greater than 0.")
            return True

        return False

    def check_entry(self, role):
        """Validate a role entry, checking for negative, zero, or non-integer values."""
        try:
            entry = self.entry_dict[f"{role}_entry"].get()
            entry_value = int(entry)

            if entry_value < 0:
                return ValueError
            elif entry_value == 0:
                return "zero"
            else:
                return False

        except ValueError:
            return ValueError

    def check_dropdown(self):
        """Verify that a valid shift is selected from the dropdown menu."""
        self.shift = self.dropdown_widget.get()
        if self.shift not in self.shifts:
            messagebox.showinfo(title="Error", message="Please select a valid shift from the dropdown menu.")
            return True
        return False

    def check_date(self):
        """Validate the date entry and display an error if it is invalid."""
        self.date = self.date_entry.get()

        try:
            self.date = dt.datetime(int(self.date[6:]), int(self.date[0:2]), int(self.date[3:5]))
            return False
        except ValueError:
            messagebox.showinfo(title="Error", message="Invalid date entry.\n\nPlease ensure you typed the correct date"
                                                       " and it's formatted as follows: MM-DD-YYYY")
            return True

    def proceed(self):
        """Ask the user for confirmation before proceeding."""
        if not messagebox.askyesno(title="Proceed?", message="Are you sure you would like to proceed?"):
            return True
        return False

    def get_nums_dict(self):
        """Create a dictionary mapping roles to their entered numeric values."""
        self.nums_dict = {role: int(self.entry_dict[f"{role}_entry"].get()) for role in self.roles}

    def get_scheduled_associates(self):
        """Retrieve the list of scheduled associates and handle errors if retrieval fails."""
        self.driver, self.scheduled_associates = self.business_logic.get_scheduled_associates(self)
        if not self.scheduled_associates:  # if None returned due to a problem
            messagebox.showinfo(title="Timeout", message="There was a problem.\n\nIs your PIN correct?\nIs your "
                                                         "security key correct?\nIs your site ID correct?\nIs your "
                                                         "shift time correct?\n\nIf yes, SSPOT may have bugged "
                                                         "out.\nPlease try again.")
            DisplayManager(self.paths_dict, self.business_logic, self.driver)
            return True
        return False

    def assign_indirects(self):
        """Assign indirect roles to scheduled associates using business logic."""
        self.result_string, self.not_enough_string = self.business_logic.assign_indirects(self.nums_dict,
                                                                                          self.scheduled_associates)

    @create_textbox("Koality Results", "res")
    def create_result_textbox(self):
        """Create a textbox displaying the final assignment results."""
        if self.not_enough_string:
            self.final_string = self.not_enough_string + "\n" + self.result_string
        else:
            self.final_string = self.result_string
        return self.final_string

    @create_textbox("Check/Edit Permissions", "perms")
    def check_permissions(self):
        """Opens text box to check/edit AA permissions for each saved role."""
        permissions_string = self.business_logic.check_permissions()
        return permissions_string

    @create_textbox("Add/Remove Roles", "saved_roles")
    def add_remove_roles(self):
        """Adds/removes indirect roles that user wants to assign AAs to."""
        roles = self.business_logic.get_roles()
        return roles

    def default(self, entry):
        """Set default values for role entries based on the specified entry type."""
        self.clear_entries()

        if entry == "REF":
            self.entry_dict["Refurb_entry"].insert(tk.END, string="1")
            self.entry_dict["Amazon Resale_entry"].insert(tk.END, string="0")
        elif entry == "AR":
            self.entry_dict["Refurb_entry"].insert(tk.END, string="0")
            self.entry_dict["Amazon Resale_entry"].insert(tk.END, string="1")

        self.entry_dict["End of Line_entry"].insert(tk.END, string="1")
        self.entry_dict["Waterspider_entry"].insert(tk.END, string="1")
        self.entry_dict["Problem Solve_entry"].insert(tk.END, string="2")
        self.entry_dict["Detrash_entry"].insert(tk.END, string="2")
        self.entry_dict["Unload_entry"].insert(tk.END, string="1")
        self.entry_dict["Audit_entry"].insert(tk.END, string="2")

    def clear_entries(self):
        """Clear all role entry fields."""
        for role in self.roles:
            self.entry_dict[f"{role}_entry"].delete(0, tk.END)

    def reset_entries(self):
        """Reset all role entry fields to zero."""
        self.clear_entries()
        for role in self.roles:
            self.entry_dict[f"{role}_entry"].insert(tk.END, string="0")

    def create_image(self):
        """Load and create the image on the canvas."""
        smile_image_path = self.paths_dict["smile_logo"]
        self.smile_image = tk.PhotoImage(file=smile_image_path)
        self.canvas.create_image(250, 285, image=self.smile_image, tag="image1")

    def create_roles(self):
        """Reads and creates text/entry for every saved role"""
        self.roles = self.business_logic.get_roles()
        self.roles = self.roles.split("\n")[:-1]

        curr_y = 465
        for role in self.roles:
            self.canvas.create_text(200, curr_y, text=f"{role}:", font=("Helvetica", 12, "bold"))

            self.entry_dict[f"{role}_entry"] = ttk.Entry(width=2)
            self.entry_dict[f"{role}_entry"].insert(tk.END, string="0")
            self.canvas.create_window(300, curr_y, window=self.entry_dict[f"{role}_entry"])

            curr_y += 50

        self.canvas.pack()
        self.canvas.mainloop()

    def midway_pin(self):
        """Retrieves midway pin via entry box"""
        pin = simpledialog.askstring("Midway PIN", "Please enter your Midway PIN:", show="*")
        if not pin:
            return TypeError
        return pin

    def security_key(self):
        """Retrieves one-time password from user's security key via entry box"""
        otp = simpledialog.askstring("Security Key", "Please press your Security Key.", show="*")
        return otp

    def main_menu(self):
        """Closes the results text window and reopens the main menu."""
        self.text_window.destroy()
        DisplayManager(self.paths_dict, self.business_logic, self.driver)
