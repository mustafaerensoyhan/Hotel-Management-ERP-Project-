import mysql.connector
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Connect to your MySQL database
try:
    project_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Boga2001.",
        port="3306",
        database="HotelManagement"
    )
    print("Connected to the database successfully.")
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")

# Helper function to show a popup message
def popupmsg(msg, heading, buttonText):
    popup = tk.Tk()
    popup.geometry('400x200')
    popup.wm_title(heading)
    label = tk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=20, padx=20)
    b1 = ttk.Button(popup, text=buttonText, command=popup.destroy)
    b1.pack()
    popup.mainloop()

def log_user_activity(user_id, activity, activity_type):
    cursor = project_db.cursor()
    cursor.execute(
        "INSERT INTO UserActivityLog (UserID, Activity, ActivityType, Timestamp) VALUES (%s, %s, %s, NOW())",
        (user_id, activity, activity_type)
    )
    project_db.commit()
    cursor.close()

def send_notification(user_id, message, notification_type):
    cursor = project_db.cursor()
    cursor.execute(
        "INSERT INTO Notifications (UserID, Message, Type) VALUES (%s, %s, %s)",
        (user_id, message, notification_type)
    )
    project_db.commit()
    cursor.close()

class HotelManagementApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Hotel Management System")
        self.geometry("1200x800")
        self.configure(bg="#2C3E50")

        self.current_user_id = None
        self.current_user_username = None
        self.current_user_role = None

        # Header Frame
        self.header_frame = tk.Frame(self, bg="#34495E")
        self.header_frame.pack(side="top", fill="x")

       # Add a logo at the top
        logo_path = os.path.join(os.path.dirname(__file__), "hotellogo.png")
        self.logo = Image.open(logo_path)
        self.logo = self.logo.resize((100, 100), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.header_frame, image=self.logo, bg="#34495E")
        self.logo_label.pack(side="left", padx=10, pady=10)

        # Add a title
        self.title_label = tk.Label(self.header_frame, text="Summer Breeze Resort", font=("Arial", 24, "bold"), bg="#34495E", fg="white")
        self.title_label.pack(side="left", padx=10, pady=10)

        self.logout_button = tk.Button(self.header_frame, text="Logout", command=self.logout, bg="#E74C3C", fg="white", font=("Arial", 12, "bold"))
        self.notifications_button = tk.Button(self.header_frame, text="Notifications", command=lambda: self.show_frame("NotificationsPage"), bg="#3498DB", fg="white", font=("Arial", 12, "bold"))

        self.frames = {}

        container = tk.Frame(self, bg="#ECF0F1")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (StartPage, RegPage, SuccessRegPage, RoomManagementPage, ReservationManagementPage, BillingManagementPage,
                  StaffManagementPage, GuestManagementPage, HousekeepingManagementPage,
                  EventManagementPage, UserProfilePage, DashboardPage, NotificationsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")  # Start with the login page

        # Footer Frame
        self.footer_frame = tk.Frame(self, bg="#34495E")
        self.footer_frame.pack(side="bottom", fill="x")
        footer_label = tk.Label(self.footer_frame, text="© 2024 Summer Breeze Resort. All rights reserved.", font=("Verdana", 10), bg="#34495E", fg="white")
        footer_label.pack(pady=10)

    def show_frame(self, page_name):
        # Define role-based access for each frame
        role_access = {
            "Admin": ["DashboardPage", "RoomManagementPage", "ReservationManagementPage", "BillingManagementPage", "StaffManagementPage", "GuestManagementPage", "HousekeepingManagementPage", "EventManagementPage", "UserProfilePage", "NotificationsPage", "ReportingPage"],
            "Staff": ["DashboardPage", "RoomManagementPage", "ReservationManagementPage", "BillingManagementPage", "GuestManagementPage", "HousekeepingManagementPage", "EventManagementPage", "UserProfilePage", "NotificationsPage", "ReportingPage"],
            "Guest": ["DashboardPage", "UserProfilePage", "NotificationsPage", "ReservationManagementPage"]
        }
        
        # Get the allowed frames for the current user's role
        allowed_frames = role_access.get(self.current_user_role, [])
        
        if page_name in allowed_frames or page_name in ["StartPage", "RegPage", "SuccessRegPage"]:
            frame = self.frames[page_name]
            frame.tkraise()
            if page_name not in ["StartPage", "RegPage", "SuccessRegPage"]:
                self.notifications_button.pack(side="right", padx=10, pady=10)
                self.logout_button.pack(side="right", padx=10, pady=10)
            else:
                self.notifications_button.pack_forget()
                self.logout_button.pack_forget()
        else:
            messagebox.showerror("Access Denied", "You do not have permission to access this page.")


    def logout(self):
        log_user_activity(self.current_user_id, f"User {self.current_user_username} logged out.", "Logout")
        self.current_user_id = None
        self.current_user_username = None
        self.show_frame("StartPage")

    def login(self, username, password):
        cursor = project_db.cursor()
        query = "SELECT UserID, Username, Role FROM Users WHERE Username=%s AND Password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            self.current_user_id = user[0]
            self.current_user_username = user[1]
            self.current_user_role = user[2]
            messagebox.showinfo("Login Success", "Welcome " + username)
            log_user_activity(self.current_user_id, f"User {username} logged in.", "Login")
            self.show_frame("DashboardPage")  # Redirect to the dashboard after login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register_user(self, username, password, email, phone, role):
        if not all([username, password, email, phone, role]):
            popupmsg("Fields cannot be Empty", "Fill All Fields", "OK")
            return

        cursor = project_db.cursor()
        try:
            # Check if the username already exists
            cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
            if cursor.fetchone() is not None:
                popupmsg("Username already exists", "Registration Failed", "OK")
                return

            # Insert the new user into the database
            query = "INSERT INTO Users (Username, Password, Email, Phone, Role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, phone, role))
            project_db.commit()
            popupmsg("Registration Successful", "You have successfully registered.", "OK")
        except mysql.connector.Error as err:
            popupmsg(f"Error: {err}", "Registration Failed", "OK")
        finally:
            cursor.close()

    def send_notification_to_user(self, user_id, message, notification_type):
        send_notification(user_id, message, notification_type)
        messagebox.showinfo("Notification Sent", f"Notification sent to user ID {user_id}")


# Start page with login functionality
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2C3E50")
        self.controller = controller

        Wel = tk.Label(self, text="Hotel Management System", font=("Verdana", 24, "bold"), bg="#2C3E50", fg="white")
        Wel.pack(pady=20)

        LIFB = tk.Label(self, text="Log In for Booking", font=("Verdana", 18), bg="#2C3E50", fg="white")
        LIFB.pack(pady=10)

        form_frame = tk.Frame(self, bg="#2C3E50")
        form_frame.pack(pady=20)

        Username = tk.Label(form_frame, text="Username", font=("Verdana", 12), bg="#2C3E50", fg="white")
        Username.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.username_entry = tk.Entry(form_frame, bd=4)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        Password = tk.Label(form_frame, text="Password", font=("Verdana", 12), bg="#2C3E50", fg="white")
        Password.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.password_entry = tk.Entry(form_frame, show='*', bd=4)
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        button_frame = tk.Frame(self, bg="#2C3E50")
        button_frame.pack(pady=20)

        login_button = tk.Button(button_frame, text="Login", command=self.login, bg="#27AE60", fg="white", font=("Verdana", 12))
        login_button.grid(row=0, column=0, padx=10)

        register_button = tk.Button(button_frame, text="Register", command=lambda: controller.show_frame("RegPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        register_button.grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.login(username, password)

    def reset(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

# Registration page
class RegPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        RHSB = tk.Label(self, text="Register for Hotel Services and Booking", font=("Verdana", 18), bg="#ECF0F1")
        RHSB.pack(pady=20)

        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        UsernameR = tk.Label(form_frame, text="Username", font=("Verdana", 12), bg="#ECF0F1")
        UsernameR.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.username_entry = tk.Entry(form_frame, bd=4)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        Email = tk.Label(form_frame, text="Email", font=("Verdana", 12), bg="#ECF0F1")
        Email.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.email_entry = tk.Entry(form_frame, bd=4)
        self.email_entry.grid(row=1, column=1, pady=5, padx=5)

        Phone = tk.Label(form_frame, text="Phone Number", font=("Verdana", 12), bg="#ECF0F1")
        Phone.grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.phone_entry = tk.Entry(form_frame, bd=4)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=5)

        PasswordR = tk.Label(form_frame, text="Password", font=("Verdana", 12), bg="#ECF0F1")
        PasswordR.grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.password_entry = tk.Entry(form_frame, show='*', bd=4)
        self.password_entry.grid(row=3, column=1, pady=5, padx=5)

        RoleLabel = tk.Label(form_frame, text="Role", font=("Verdana", 12), bg="#ECF0F1")
        RoleLabel.grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.role_var = tk.StringVar(value="Guest")
        RoleOptions = tk.OptionMenu(form_frame, self.role_var, "Staff", "Guest")
        RoleOptions.grid(row=4, column=1, pady=5, padx=5)

        SU = tk.Button(form_frame, text="Sign Up", command=self.register_user, bg="#27AE60", fg="white", font=("Verdana", 12))
        SU.grid(row=5, column=0, columnspan=2, pady=20)

        ResetButton = tk.Button(form_frame, text="Reset", command=self.reset, bg="#E74C3C", fg="white", font=("Verdana", 12))
        ResetButton.grid(row=6, column=0, columnspan=2, pady=10)

        AHA = tk.Label(self, text="Already have an account?", font=("Verdana", 14), bg="#ECF0F1")
        AHA.pack(pady=10)

        Loginbutton2 = tk.Button(self, text="Go to Login Page", command=lambda: controller.show_frame("StartPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        Loginbutton2.pack(pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        role = self.role_var.get()
        self.controller.register_user(username, password, email, phone, role)

    def reset(self):
        self.username_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.role_var.set("Guest")


# Successful registration page
class SuccessRegPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        label = tk.Label(self, text="Successfully Registered", font=("Verdana", 18), bg="#ECF0F1")
        label.pack(pady=20)

        button4 = tk.Button(self, text="Go To Login Page", command=lambda: controller.show_frame("StartPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        button4.pack(pady=20)

# Room Management Page
class RoomManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        # Search Bar
        search_frame = tk.Frame(self, bg="#ECF0F1")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(search_frame, text="Search Room Number", bg="#ECF0F1", font=("Verdana", 12)).grid(row=0, column=0, pady=5)
        self.search_entry = tk.Entry(search_frame, bd=4)
        self.search_entry.grid(row=0, column=1, pady=5)
        tk.Button(search_frame, text="Search", command=self.search_rooms, bg="#27AE60", fg="white", font=("Verdana", 12)).grid(row=0, column=2, pady=5, padx=5)

        # Add Room Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        tk.Label(form_frame, text="Room Number", bg="#ECF0F1", font=("Verdana", 12)).grid(row=0, column=0, pady=5)
        self.room_number_entry = tk.Entry(form_frame, bd=4)
        self.room_number_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Category", bg="#ECF0F1", font=("Verdana", 12)).grid(row=1, column=0, pady=5)
        self.category_entry = tk.Entry(form_frame, bd=4)
        self.category_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Status", bg="#ECF0F1", font=("Verdana", 12)).grid(row=2, column=0, pady=5)
        self.status_entry = tk.Entry(form_frame, bd=4)
        self.status_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Features", bg="#ECF0F1", font=("Verdana", 12)).grid(row=3, column=0, pady=5)
        self.features_entry = tk.Entry(form_frame, bd=4)
        self.features_entry.grid(row=3, column=1, pady=5)

        tk.Button(form_frame, text="Add Room", command=self.add_room, bg="#27AE60", fg="white", font=("Verdana", 12)).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(form_frame, text="Delete Room", command=self.delete_room, bg="#E74C3C", fg="white", font=("Verdana", 12)).grid(row=5, column=0, columnspan=2, pady=10)

        # Room List
        list_frame = tk.Frame(self, bg="#ECF0F1")
        list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.room_list = ttk.Treeview(list_frame, columns=("RoomNumber", "Category", "Status", "Features"))
        self.room_list.grid(row=0, column=0, columnspan=2)
        self.room_list.heading("#0", text="Room ID")
        self.room_list.heading("#1", text="Room Number")
        self.room_list.heading("#2", text="Category")
        self.room_list.heading("#3", text="Status")
        self.room_list.heading("#4", text="Features")

        self.load_rooms()

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg="#ECF0F1")
        nav_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        tk.Button(nav_frame, text="Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=0, column=0, pady=5)
        tk.Button(nav_frame, text="User Profile", command=lambda: controller.show_frame("UserProfilePage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=1, column=0, pady=5)
        tk.Button(nav_frame, text="Manage Reservations", command=lambda: controller.show_frame("ReservationManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=2, column=0, pady=5)
        tk.Button(nav_frame, text="Manage Billing", command=lambda: controller.show_frame("BillingManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=3, column=0, pady=5)

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.grid(row=4, column=0, pady=10)

    def add_room(self):
        room_number = self.room_number_entry.get()
        category = self.category_entry.get()
        status = self.status_entry.get()
        features = self.features_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Rooms (RoomNumber, CategoryID, Status, Features) VALUES (%s, %s, %s, %s)",
                       (room_number, category, status, features))
        project_db.commit()
        cursor.close()

        self.load_rooms()
        log_activity(self.controller.current_user_id, f"Added room {room_number}", "System Alert")

    def load_rooms(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT RoomID, RoomNumber, CategoryID, Status, Features FROM Rooms")
        rooms = cursor.fetchall()
        cursor.close()

        for row in self.room_list.get_children():
            self.room_list.delete(row)

        for room in rooms:
            self.room_list.insert("", "end", text=room[0], values=(room[1], room[2], room[3], room[4]))

    def delete_room(self):
        selected_item = self.room_list.selection()
        if selected_item:
            room_id = self.room_list.item(selected_item[0], 'text')
            cursor = project_db.cursor()
            cursor.execute("DELETE FROM Rooms WHERE RoomID = %s", (room_id,))
            project_db.commit()
            cursor.close()
            self.load_rooms()
            log_activity(self.controller.current_user_id, f"Deleted room {room_id}", "System Alert")
        else:
            popupmsg("No room selected.", "Delete Room", "OK")

    def search_rooms(self):
        search_value = self.search_entry.get()
        cursor = project_db.cursor()
        query = "SELECT RoomID, RoomNumber, CategoryID, Status, Features FROM Rooms WHERE RoomNumber LIKE %s"
        cursor.execute(query, ('%' + search_value + '%',))
        rooms = cursor.fetchall()
        cursor.close()

        for row in self.room_list.get_children():
            self.room_list.delete(row)

        for room in rooms:
            self.room_list.insert("", "end", text=room[0], values=(room[1], room[2], room[3], room[4]))



# Adding "Manage Rooms" button to the main dashboard

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="Dashboard", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=20)

        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Manage Rooms", command=lambda: controller.show_frame("RoomManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Manage Reservations", command=lambda: controller.show_frame("ReservationManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Manage Billing", command=lambda: controller.show_frame("BillingManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Manage Staff", command=lambda: controller.show_frame("StaffManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="User Profile", command=lambda: controller.show_frame("UserProfilePage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Manage Events", command=lambda: controller.show_frame("EventManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Manage Housekeeping", command=lambda: controller.show_frame("HousekeepingManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        tk.Button(button_frame, text="Reports", command=lambda: controller.show_frame("ReportingPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).pack(pady=10)
        
        # Add form to send notifications for Admin
        if self.controller.current_user_role == "Admin":
            tk.Label(self, text="Send Notification", font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=10)
            form_frame = tk.Frame(self, bg="#ECF0F1")
            form_frame.pack(pady=10)

            tk.Label(form_frame, text="User ID", font=("Verdana", 12), bg="#ECF0F1").grid(row=0, column=0, pady=5, padx=5, sticky="e")
            self.user_id_entry = tk.Entry(form_frame, bd=4)
            self.user_id_entry.grid(row=0, column=1, pady=5, padx=5)

            tk.Label(form_frame, text="Message", font=("Verdana", 12), bg="#ECF0F1").grid(row=1, column=0, pady=5, padx=5, sticky="e")
            self.message_entry = tk.Entry(form_frame, bd=4)
            self.message_entry.grid(row=1, column=1, pady=5, padx=5)

            tk.Label(form_frame, text="Type", font=("Verdana", 12), bg="#ECF0F1").grid(row=2, column=0, pady=5, padx=5, sticky="e")
            self.type_entry = tk.Entry(form_frame, bd=4)
            self.type_entry.grid(row=2, column=1, pady=5, padx=5)

            send_button = tk.Button(form_frame, text="Send Notification", command=self.send_notification, bg="#27AE60", fg="white", font=("Verdana", 12))
            send_button.grid(row=3, column=0, columnspan=2, pady=20)

    def send_notification(self):
        user_id = self.user_id_entry.get()
        message = self.message_entry.get()
        notification_type = self.type_entry.get()
        self.controller.send_notification_to_user(user_id, message, notification_type)


# Reservation Management Page
class ReservationManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        # Reservation Form
        tk.Label(self, text="Room ID", bg="#ECF0F1", font=("Verdana", 12)).grid(row=0, column=0)
        self.room_id_entry = tk.Entry(self, bd=4)
        self.room_id_entry.grid(row=0, column=1)

        tk.Label(self, text="User ID", bg="#ECF0F1", font=("Verdana", 12)).grid(row=1, column=0)
        self.user_id_entry = tk.Entry(self, bd=4)
        self.user_id_entry.grid(row=1, column=1)

        tk.Label(self, text="Check-In Date (YYYY-MM-DD)", bg="#ECF0F1", font=("Verdana", 12)).grid(row=2, column=0)
        self.check_in_date_entry = tk.Entry(self, bd=4)
        self.check_in_date_entry.grid(row=2, column=1)

        tk.Label(self, text="Check-Out Date (YYYY-MM-DD)", bg="#ECF0F1", font=("Verdana", 12)).grid(row=3, column=0)
        self.check_out_date_entry = tk.Entry(self, bd=4)
        self.check_out_date_entry.grid(row=3, column=1)

        tk.Button(self, text="Create Reservation", command=self.create_reservation, bg="#27AE60", fg="white", font=("Verdana", 12)).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Delete Reservation", command=self.delete_reservation, bg="#E74C3C", fg="white", font=("Verdana", 12)).grid(row=5, column=0, columnspan=2, pady=10)

        # Reservation List
        self.reservation_list = ttk.Treeview(self, columns=("RoomID", "UserID", "CheckInDate", "CheckOutDate", "Status"))
        self.reservation_list.grid(row=6, column=0, columnspan=2)
        self.reservation_list.heading("#0", text="Reservation ID")
        self.reservation_list.heading("#1", text="Room ID")
        self.reservation_list.heading("#2", text="User ID")
        self.reservation_list.heading("#3", text="Check-In Date")
        self.reservation_list.heading("#4", text="Check-Out Date")
        self.reservation_list.heading("#5", text="Status")

        self.load_reservations()

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_reservation(self):
        room_id = self.room_id_entry.get()
        user_id = self.user_id_entry.get()
        check_in_date = self.check_in_date_entry.get()
        check_out_date = self.check_out_date_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Reservations (RoomID, UserID, CheckInDate, CheckOutDate, Status) VALUES (%s, %s, %s, %s, 'Pending')",
                       (room_id, user_id, check_in_date, check_out_date))
        project_db.commit()
        cursor.close()

        self.load_reservations()

    def load_reservations(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT ReservationID, RoomID, UserID, CheckInDate, CheckOutDate, Status FROM Reservations")
        reservations = cursor.fetchall()
        cursor.close()

        for row in self.reservation_list.get_children():
            self.reservation_list.delete(row)

        for reservation in reservations:
            self.reservation_list.insert("", "end", text=reservation[0], values=(reservation[1], reservation[2], reservation[3], reservation[4], reservation[5]))

    def delete_reservation(self):
        selected_item = self.reservation_list.selection()
        if selected_item:
            reservation_id = self.reservation_list.item(selected_item[0], 'text')
            cursor = project_db.cursor()
            cursor.execute("DELETE FROM Reservations WHERE ReservationID = %s", (reservation_id,))
            project_db.commit()
            cursor.close()
            self.load_reservations()
            log_activity(self.controller.current_user_id, f"Deleted reservation {reservation_id}", "System Alert")
        else:
            popupmsg("No reservation selected.", "Delete Reservation", "OK")


# Billing Management Page
class BillingManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        # Billing Form
        tk.Label(self, text="Reservation ID", bg="#ECF0F1", font=("Verdana", 12)).grid(row=0, column=0)
        self.reservation_id_entry = tk.Entry(self, bd=4)
        self.reservation_id_entry.grid(row=0, column=1)

        tk.Label(self, text="Amount", bg="#ECF0F1", font=("Verdana", 12)).grid(row=1, column=0)
        self.amount_entry = tk.Entry(self, bd=4)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(self, text="Payment Status", bg="#ECF0F1", font=("Verdana", 12)).grid(row=2, column=0)
        self.payment_status_entry = tk.Entry(self, bd=4)
        self.payment_status_entry.grid(row=2, column=1)

        tk.Label(self, text="Billing Date", bg="#ECF0F1", font=("Verdana", 12)).grid(row=3, column=0)
        self.billing_date_entry = tk.Entry(self, bd=4)
        self.billing_date_entry.grid(row=3, column=1)

        tk.Button(self, text="Create Bill", command=self.create_bill, bg="#27AE60", fg="white", font=("Verdana", 12)).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Delete Bill", command=self.delete_bill, bg="#E74C3C", fg="white", font=("Verdana", 12)).grid(row=5, column=0, columnspan=2, pady=10)

        # Billing List
        self.billing_list = ttk.Treeview(self, columns=("ReservationID", "Amount", "PaymentStatus", "BillingDate"))
        self.billing_list.grid(row=6, column=0, columnspan=2)
        self.billing_list.heading("#0", text="Billing ID")
        self.billing_list.heading("#1", text="Reservation ID")
        self.billing_list.heading("#2", text="Amount")
        self.billing_list.heading("#3", text="Payment Status")
        self.billing_list.heading("#4", text="Billing Date")

        self.load_bills()

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_bill(self):
        reservation_id = self.reservation_id_entry.get()
        amount = self.amount_entry.get()
        payment_status = self.payment_status_entry.get()
        billing_date = datetime.now().date()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Billing (ReservationID, Amount, PaymentStatus, Date) VALUES (%s, %s, %s, %s)",
                       (reservation_id, amount, payment_status, billing_date))
        project_db.commit()
        cursor.close()

        self.load_bills()

    def load_bills(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT BillID, ReservationID, Amount, PaymentStatus, Date FROM Billing")
        bills = cursor.fetchall()
        cursor.close()

        for row in self.billing_list.get_children():
            self.billing_list.delete(row)

        for bill in bills:
            self.billing_list.insert("", "end", text=bill[0], values=(bill[1], bill[2], bill[3], bill[4]))

    def delete_bill(self):
        selected_item = self.billing_list.selection()
        if selected_item:
            bill_id = self.billing_list.item(selected_item[0], 'text')
            cursor = project_db.cursor()
            cursor.execute("DELETE FROM Billing WHERE BillID = %s", (bill_id,))
            project_db.commit()
            cursor.close()
            self.load_bills()
            log_activity(self.controller.current_user_id, f"Deleted bill {bill_id}", "System Alert")
        else:
            popupmsg("No billing selected.", "Delete Bill", "OK")


# Room Management Page
class RoomManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Add Room Form
        tk.Label(self, text="Room Number").grid(row=0, column=0)
        self.room_number_entry = tk.Entry(self)
        self.room_number_entry.grid(row=0, column=1)

        tk.Label(self, text="Category").grid(row=1, column=0)
        self.category_entry = tk.Entry(self)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self, text="Status").grid(row=2, column=0)
        self.status_entry = tk.Entry(self)
        self.status_entry.grid(row=2, column=1)

        tk.Label(self, text="Features").grid(row=3, column=0)
        self.features_entry = tk.Entry(self)
        self.features_entry.grid(row=3, column=1)

        tk.Button(self, text="Add Room", command=self.add_room).grid(row=4, column=0, columnspan=2)
        tk.Button(self, text="Delete Room", command=self.delete_room).grid(row=5, column=0, columnspan=2)

        # Room List
        self.room_list = ttk.Treeview(self, columns=("RoomNumber", "Category", "Status", "Features"))
        self.room_list.grid(row=6, column=0, columnspan=2)
        self.room_list.heading("#0", text="Room ID")
        self.room_list.heading("#1", text="Room Number")
        self.room_list.heading("#2", text="Category")
        self.room_list.heading("#3", text="Status")
        self.room_list.heading("#4", text="Features")

        self.load_rooms()

        # Navigation Buttons
        tk.Button(self, text="Manage Reservations", command=lambda: controller.show_frame("ReservationManagementPage")).grid(row=7, column=0, columnspan=2)
        tk.Button(self, text="Manage Billing", command=lambda: controller.show_frame("BillingManagementPage")).grid(row=8, column=0, columnspan=2)

    def add_room(self):
        room_number = self.room_number_entry.get()
        category = self.category_entry.get()
        status = self.status_entry.get()
        features = self.features_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Rooms (RoomNumber, CategoryID, Status, Features) VALUES (%s, %s, %s, %s)",
                       (room_number, category, status, features))
        project_db.commit()
        cursor.close()

        self.load_rooms()

    def load_rooms(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT RoomID, RoomNumber, CategoryID, Status, Features FROM Rooms")
        rooms = cursor.fetchall()
        cursor.close()

        for row in self.room_list.get_children():
            self.room_list.delete(row)

        for room in rooms:
            self.room_list.insert("", "end", text=room[0], values=(room[1], room[2], room[3], room[4]))

    def delete_room(self):
        selected_item = self.room_list.selection()
        if selected_item:
            room_id = self.room_list.item(selected_item[0], 'text')
            cursor = project_db.cursor()
            cursor.execute("DELETE FROM Rooms WHERE RoomID = %s", (room_id,))
            project_db.commit()
            cursor.close()
            self.load_rooms()
        else:
            popupmsg("No room selected.", "Delete Room", "OK")


# Staff Management Page
class StaffManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Staff Form
        tk.Label(self, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Role").grid(row=1, column=0)
        self.role_entry = tk.Entry(self)
        self.role_entry.grid(row=1, column=1)

        tk.Label(self, text="Phone").grid(row=2, column=0)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(self, text="Email").grid(row=3, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=3, column=1)

        tk.Label(self, text="Shift").grid(row=4, column=0)
        self.shift_entry = tk.Entry(self)
        self.shift_entry.grid(row=4, column=1)

        tk.Button(self, text="Add Staff", command=self.add_staff).grid(row=5, column=0, columnspan=2)

        # Staff List
        self.staff_list = ttk.Treeview(self, columns=("StaffID", "Name", "Role", "Phone", "Email", "Shift"))
        self.staff_list.grid(row=6, column=0, columnspan=2)
        self.staff_list.heading("#0", text="Staff ID")
        self.staff_list.heading("#1", text="Name")
        self.staff_list.heading("#2", text="Role")
        self.staff_list.heading("#3", text="Phone")
        self.staff_list.heading("#4", text="Email")
        self.staff_list.heading("#5", text="Shift")

        self.load_staff()

    def add_staff(self):
        name = self.name_entry.get()
        role = self.role_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        shift = self.shift_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Staff (Name, Role, Phone, Email, Shift) VALUES (%s, %s, %s, %s, %s)",
                       (name, role, phone, email, shift))
        project_db.commit()
        cursor.close()

        self.load_staff()

    def load_staff(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT * FROM Staff")
        staff = cursor.fetchall()
        cursor.close()

        for row in self.staff_list.get_children():
            self.staff_list.delete(row)

        for staff_member in staff:
            self.staff_list.insert("", "end", text=staff_member[0], values=(staff_member[1], staff_member[2], staff_member[3], staff_member[4], staff_member[5]))

#Notifications Management Page
class NotificationsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="Notifications", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=20)

        # Notification List
        self.notification_list = ttk.Treeview(self, columns=("Date", "Message", "Type"))
        self.notification_list.pack(fill="both", expand=True)
        self.notification_list.heading("#0", text="Notification ID")
        self.notification_list.heading("#1", text="Date")
        self.notification_list.heading("#2", text="Message")
        self.notification_list.heading("#3", text="Type")

        # Send Notification Button
        send_notification_button = tk.Button(self, text="Send Notification", command=self.show_send_notification_form, bg="#27AE60", fg="white", font=("Verdana", 12))
        send_notification_button.pack(pady=10)

        # Close Send Notification Button    
        close_form_button = tk.Button(self, text="Close Form", command=self.hide_send_notification_form, bg="#C0392B", fg="white", font=("Verdana", 12))
        close_form_button.pack(pady=10)

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.pack(pady=10)

        # Form to send notifications (initially hidden)
        self.form_frame = tk.Frame(self, bg="#ECF0F1")
        tk.Label(self.form_frame, text="Send Notification", font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=10)

        tk.Label(self.form_frame, text="User ID", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.user_id_entry = tk.Entry(self.form_frame, bd=4)
        self.user_id_entry.pack(pady=5)

        tk.Label(self.form_frame, text="Message", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.message_entry = tk.Entry(self.form_frame, bd=4)
        self.message_entry.pack(pady=5)

        tk.Label(self.form_frame, text="Type", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.type_entry = tk.Entry(self.form_frame, bd=4)
        self.type_entry.pack(pady=5)

        tk.Label(self.form_frame, text="Date", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.type_entry = tk.Entry(self.form_frame, bd=4)
        self.type_entry.pack(pady=5)

        send_button = tk.Button(self.form_frame, text="Send", command=self.send_notification, bg="#27AE60", fg="white", font=("Verdana", 12))
        send_button.pack(pady=20)
        self.form_frame.pack_forget()  # Initially hide the form

    def show_send_notification_form(self):
        self.form_frame.pack(pady=10)

    def hide_send_notification_form(self):
        self.form_frame.pack_forget()

    def send_notification(self):
        user_id = self.user_id_entry.get()
        message = self.message_entry.get()
        notification_type = self.type_entry.get()
        if notification_type not in ['System Alert', 'Guest Notification', 'Payment Reminder']:
            messagebox.showerror("Error", "Invalid notification type")
            return
        self.controller.send_notification_to_user(user_id, message, notification_type)
        self.form_frame.pack_forget()  # Hide the form after sending the notification
        messagebox.showinfo("Notification Sent", "Notification has been sent successfully.")
        self.load_notifications()  # Reload notifications after sending

    def load_notifications(self):
        cursor = project_db.cursor()
        try:
            query = "SELECT NotificationID, Date, Message, Type FROM Notifications WHERE UserID = %s"
            print(f"Executing query: {query} with UserID = {self.controller.current_user_id}")
            cursor.execute(query, (self.controller.current_user_id,))
            notifications = cursor.fetchall()
            print(f"Fetched notifications: {notifications}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return
        finally:
            cursor.close()

        for row in self.notification_list.get_children():
            self.notification_list.delete(row)

        for notification in notifications:
            self.notification_list.insert("", "end", text=notification[0], values=(notification[1], notification[2], notification[3]))
            print(f"Inserted notification: {notification}")

        
# Guest Management Page
class GuestManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Guest Form
        tk.Label(self, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Email").grid(row=1, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1)

        tk.Label(self, text="Phone").grid(row=2, column=0)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(self, text="Preferences").grid(row=3, column=0)
        self.preferences_entry = tk.Entry(self)
        self.preferences_entry.grid(row=3, column=1)

        tk.Button(self, text="Add Guest", command=self.add_guest).grid(row=4, column=0, columnspan=2)

        # Guest List
        self.guest_list = ttk.Treeview(self, columns=("GuestID", "Name", "Email", "Phone", "Preferences"))
        self.guest_list.grid(row=5, column=0, columnspan=2)
        self.guest_list.heading("#0", text="Guest ID")
        self.guest_list.heading("#1", text="Name")
        self.guest_list.heading("#2", text="Email")
        self.guest_list.heading("#3", text="Phone")
        self.guest_list.heading("#4", text="Preferences")

        self.load_guests()

    def add_guest(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        preferences = self.preferences_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Guests (Name, Email, Phone, Preferences) VALUES (%s, %s, %s, %s)",
                       (name, email, phone, preferences))
        project_db.commit()
        cursor.close()

        self.load_guests()

    def load_guests(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT * FROM Guests")
        guests = cursor.fetchall()
        cursor.close()

        for row in self.guest_list.get_children():
            self.guest_list.delete(row)

        for guest in guests:
            self.guest_list.insert("", "end", text=guest[0], values=(guest[1], guest[2], guest[3], guest[4]))

# Housekeeping Management Page
class HousekeepingManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Housekeeping Form
        tk.Label(self, text="Room ID").grid(row=0, column=0)
        self.room_id_entry = tk.Entry(self)
        self.room_id_entry.grid(row=0, column=1)

        tk.Label(self, text="Task").grid(row=1, column=0)
        self.task_entry = tk.Entry(self)
        self.task_entry.grid(row=1, column=1)

        tk.Button(self, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2)

        # Housekeeping List
        self.housekeeping_list = ttk.Treeview(self, columns=("HousekeepingID", "RoomID", "Task", "Status"))
        self.housekeeping_list.grid(row=3, column=0, columnspan=2)
        self.housekeeping_list.heading("#0", text="Housekeeping ID")
        self.housekeeping_list.heading("#1", text="Room ID")
        self.housekeeping_list.heading("#2", text="Task")
        self.housekeeping_list.heading("#3", text="Status")

        self.load_tasks()

    def add_task(self):
        room_id = self.room_id_entry.get()
        task = self.task_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO HousekeepingTasks (RoomID, Task, Status) VALUES (%s, %s, 'Pending')", (room_id, task))
        project_db.commit()
        cursor.close()

        self.load_tasks()

    def load_tasks(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT * FROM HousekeepingTasks")
        tasks = cursor.fetchall()
        cursor.close()

        for row in self.housekeeping_list.get_children():
            self.housekeeping_list.delete(row)

        for task in tasks:
            self.housekeeping_list.insert("", "end", text=task[0], values=(task[1], task[2], task[3]))

class StaffManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        # Staff Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name", bg="#ECF0F1", font=("Verdana", 12)).grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.name_entry = tk.Entry(form_frame, bd=4)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Role", bg="#ECF0F1", font=("Verdana", 12)).grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.role_entry = tk.Entry(form_frame, bd=4)
        self.role_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Phone", bg="#ECF0F1", font=("Verdana", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.phone_entry = tk.Entry(form_frame, bd=4)
        self.phone_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Email", bg="#ECF0F1", font=("Verdana", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.email_entry = tk.Entry(form_frame, bd=4)
        self.email_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Shift", bg="#ECF0F1", font=("Verdana", 12)).grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.shift_entry = tk.Entry(form_frame, bd=4)
        self.shift_entry.grid(row=4, column=1, pady=5, padx=5)

        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Add Staff", command=self.add_staff, bg="#27AE60", fg="white", font=("Verdana", 12)).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Delete Staff", command=self.delete_staff, bg="#E74C3C", fg="white", font=("Verdana", 12)).grid(row=0, column=1, padx=10)

        # Staff List
        list_frame = tk.Frame(self, bg="#ECF0F1")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.staff_list = ttk.Treeview(list_frame, columns=("Name", "Role", "Phone", "Email", "Shift"))
        self.staff_list.pack(fill="both", expand=True)
        self.staff_list.heading("#0", text="Staff ID")
        self.staff_list.heading("#1", text="Name")
        self.staff_list.heading("#2", text="Role")
        self.staff_list.heading("#3", text="Phone")
        self.staff_list.heading("#4", text="Email")
        self.staff_list.heading("#5", text="Shift")

        self.load_staff()

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg="#ECF0F1")
        nav_frame.pack(pady=20)

        tk.Button(nav_frame, text="Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=0, column=0, pady=5)
        tk.Button(nav_frame, text="User Profile", command=lambda: controller.show_frame("UserProfilePage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=1, column=0, pady=5)
        tk.Button(nav_frame, text="Manage Reservations", command=lambda: controller.show_frame("ReservationManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=2, column=0, pady=5)
        tk.Button(nav_frame, text="Manage Billing", command=lambda: controller.show_frame("BillingManagementPage"), bg="#2980B9", fg="white", font=("Verdana", 12)).grid(row=3, column=0, pady=5)

    def add_staff(self):
        name = self.name_entry.get()
        role = self.role_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        shift = self.shift_entry.get()

        cursor = project_db.cursor()
        cursor.execute("INSERT INTO Staff (Name, Role, Phone, Email, Shift) VALUES (%s, %s, %s, %s, %s)",
                       (name, role, phone, email, shift))
        project_db.commit()
        cursor.close()

        self.load_staff()
        log_activity(self.controller.current_user_id, f"Added staff {name}", "System Alert")

    def load_staff(self):
        cursor = project_db.cursor()
        cursor.execute("SELECT * FROM Staff")
        staff = cursor.fetchall()
        cursor.close()

        for row in self.staff_list.get_children():
            self.staff_list.delete(row)

        for staff_member in staff:
            self.staff_list.insert("", "end", text=staff_member[0], values=(staff_member[1], staff_member[2], staff_member[3], staff_member[4], staff_member[5]))

    def delete_staff(self):
        selected_item = self.staff_list.selection()
        if selected_item:
            staff_id = self.staff_list.item(selected_item[0], 'text')
            cursor = project_db.cursor()
            cursor.execute("DELETE FROM Staff WHERE StaffID = %s", (staff_id,))
            project_db.commit()
            cursor.close()
            self.load_staff()
            log_activity(self.controller.current_user_id, f"Deleted staff {staff_id}", "System Alert")
        else:
            popupmsg("No staff selected.", "Delete Staff", "OK")

# Event Management Page
class EventManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="Event Management", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=20)

        # Event List
        self.event_list = ttk.Treeview(self, columns=("EventName", "EventDate", "EventDetails"))
        self.event_list.pack(fill="both", expand=True)
        self.event_list.heading("#0", text="Event ID")
        self.event_list.heading("#1", text="Event Name")
        self.event_list.heading("#2", text="Event Date")
        self.event_list.heading("#3", text="Event Details")

        # Add Event Button
        add_event_button = tk.Button(self, text="Add Event", command=self.show_add_event_form, bg="#27AE60", fg="white", font=("Verdana", 12))
        add_event_button.pack(pady=10)

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.pack(pady=10)

        # Form to add events (initially hidden)
        self.form_frame = tk.Frame(self, bg="#ECF0F1")
        tk.Label(self.form_frame, text="Add Event", font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=10)

        tk.Label(self.form_frame, text="Event Name", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.event_name_entry = tk.Entry(self.form_frame, bd=4)
        self.event_name_entry.pack(pady=5)

        tk.Label(self.form_frame, text="Event Date (YYYY-MM-DD)", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.event_date_entry = tk.Entry(self.form_frame, bd=4)
        self.event_date_entry.pack(pady=5)

        tk.Label(self.form_frame, text="Event Details", font=("Verdana", 12), bg="#ECF0F1").pack(pady=5)
        self.event_details_entry = tk.Entry(self.form_frame, bd=4)
        self.event_details_entry.pack(pady=5)

        save_button = tk.Button(self.form_frame, text="Save", command=self.add_event, bg="#27AE60", fg="white", font=("Verdana", 12))
        save_button.pack(pady=20)
        self.form_frame.pack_forget()  # Initially hide the form

        self.load_events()  # Load events when the page is initialized

    def show_add_event_form(self):
        self.form_frame.pack(pady=10)

    def add_event(self):
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_details = self.event_details_entry.get()

        cursor = project_db.cursor()
        try:
            cursor.execute(
                "INSERT INTO Events (EventName, EventDate, EventDetails) VALUES (%s, %s, %s)",
                (event_name, event_date, event_details)
            )
            project_db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

        self.form_frame.pack_forget()  # Hide the form after adding the event
        messagebox.showinfo("Event Added", "Event has been added successfully.")
        self.load_events()  # Reload events after adding

    def load_events(self):
        cursor = project_db.cursor()
        try:
            cursor.execute("SELECT EventID, EventName, EventDate, EventDetails FROM Events")
            events = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return
        finally:
            cursor.close()

        for row in self.event_list.get_children():
            self.event_list.delete(row)

        for event in events:
            self.event_list.insert("", "end", text=event[0], values=(event[1], event[2], event[3]))


class UserProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="User Profile", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=10)

        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Username", font=("Verdana", 12), bg="#ECF0F1").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.username_entry = tk.Entry(form_frame, bd=4)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Email", font=("Verdana", 12), bg="#ECF0F1").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.email_entry = tk.Entry(form_frame, bd=4)
        self.email_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Change Password", font=("Verdana", 12), bg="#ECF0F1").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.password_entry = tk.Entry(form_frame, show='*', bd=4)
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Update Profile", command=self.update_profile, bg="#27AE60", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cancel", command=lambda: controller.show_frame("DashboardPage"), bg="#E74C3C", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.pack(pady=10)

    def update_profile(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        cursor = project_db.cursor()
        cursor.execute("UPDATE Users SET Email=%s, Password=%s WHERE Username=%s", (email, password, username))
        project_db.commit()
        cursor.close()
        log_activity(self.controller.current_user_id, f"Updated profile for user {username}", "System Alert")
        popupmsg("Profile updated successfully.", "Update Profile", "OK")


class ReportingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="Reporting", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=20)

        # Buttons to generate reports
        reservation_stats_button = tk.Button(self, text="Reservation Statistics", command=self.show_reservation_stats, bg="#3498DB", fg="white", font=("Verdana", 12))
        reservation_stats_button.pack(pady=10)

        occupancy_rates_button = tk.Button(self, text="Occupancy Rates", command=self.show_occupancy_rates, bg="#3498DB", fg="white", font=("Verdana", 12))
        occupancy_rates_button.pack(pady=10)

        financial_summary_button = tk.Button(self, text="Financial Summary", command=self.show_financial_summary, bg="#3498DB", fg="white", font=("Verdana", 12))
        financial_summary_button.pack(pady=10)

        # Back to Dashboard Button
        back_button = tk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage"), bg="#2980B9", fg="white", font=("Verdana", 12))
        back_button.pack(pady=10)

        # Report display area
        self.report_area = tk.Text(self, wrap="word", width=80, height=20, bg="#ECF0F1", bd=4, relief="sunken")
        self.report_area.pack(pady=20)

    def show_reservation_stats(self):
        cursor = project_db.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_reservations,
                SUM(CASE WHEN Status = 'Confirmed' THEN 1 ELSE 0 END) AS confirmed_reservations,
                SUM(CASE WHEN Status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_reservations
            FROM Reservations;
        """)
        result = cursor.fetchone()
        cursor.close()

        report = f"""
        Reservation Statistics:
        -----------------------
        Total Reservations: {result[0]}
        Confirmed Reservations: {result[1]}
        Cancelled Reservations: {result[2]}
        """
        self.display_report(report)

    def show_occupancy_rates(self):
        cursor = project_db.cursor()
        cursor.execute("""
            SELECT 
                RoomID, 
                COUNT(*) AS total_nights,
                SUM(CASE WHEN Status = 'CheckedIn' THEN 1 ELSE 0 END) AS occupied_nights
            FROM Reservations
            WHERE CheckInDate <= CURDATE() AND CheckOutDate >= CURDATE()
            GROUP BY RoomID;
        """)
        results = cursor.fetchall()
        cursor.close()

        report = "Occupancy Rates:\n-----------------\n"
        for result in results:
            report += f"Room {result[0]}: {result[2]} out of {result[1]} nights occupied\n"
        self.display_report(report)

    def show_financial_summary(self):
        cursor = project_db.cursor()
        cursor.execute("""
            SELECT 
                SUM(Amount) AS total_income,
                SUM(CASE WHEN PaymentStatus = 'Paid' THEN Amount ELSE 0 END) AS paid_amount,
                SUM(CASE WHEN PaymentStatus = 'Pending' THEN Amount ELSE 0 END) AS pending_amount
            FROM Payments;
        """)
        result = cursor.fetchone()
        cursor.close()

        report = f"""
        Financial Summary:
        ------------------
        Total Income: ${result[0]:,.2f}
        Paid Amount: ${result[1]:,.2f}
        Pending Amount: ${result[2]:,.2f}
        """
        self.display_report(report)

    def display_report(self, report):
        self.report_area.delete(1.0, tk.END)
        self.report_area.insert(tk.END, report)

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ECF0F1")
        self.controller = controller

        tk.Label(self, text="Admin Dashboard", font=("Arial", 24, "bold"), bg="#ECF0F1").pack(pady=20)

        # Form to send notifications
        tk.Label(self, text="Send Notification", font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=10)
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="User ID", font=("Verdana", 12), bg="#ECF0F1").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.user_id_entry = tk.Entry(form_frame, bd=4)
        self.user_id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Message", font=("Verdana", 12), bg="#ECF0F1").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.message_entry = tk.Entry(form_frame, bd=4)
        self.message_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Type", font=("Verdana", 12), bg="#ECF0F1").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.type_entry = tk.Entry(form_frame, bd=4)
        self.type_entry.grid(row=2, column=1, pady=5, padx=5)

        send_button = tk.Button(form_frame, text="Send Notification", command=self.send_notification, bg="#27AE60", fg="white", font=("Verdana", 12))
        send_button.grid(row=3, column=0, columnspan=2, pady=20)

    def send_notification(self):
        user_id = self.user_id_entry.get()
        message = self.message_entry.get()
        notification_type = self.type_entry.get()
        self.controller.send_notification_to_user(user_id, message, notification_type)


# Run the Application
if __name__ == "__main__":
    app = HotelManagementApp()
    app.geometry('1200x800')
    app.mainloop()


