import customtkinter
import os
import json
import webbrowser
import logging
from tkinter import messagebox

# Set up logging
log_path = os.path.join("dat", "app.log")
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load settings
def load_settings():
    logging.info("Loading settings...")
    settings_path = os.path.join("dat", "settings.json")
    with open(settings_path, "r") as f:
        settings = json.load(f)
    logging.info("Settings loaded successfully.")
    return settings

# Load language file for settings
def load_settings_language(language_code):
    logging.info(f"Loading language file for: {language_code}")
    lang_path = os.path.join("lang", f"{language_code}_settings.json")
    with open(lang_path, "r") as f:
        language = json.load(f)
    logging.info("Language file loaded successfully.")
    return language

# Load settings and language
settings = load_settings()
settings_language = load_settings_language(settings["language"])

# Get list of available languages
def get_available_languages():
    logging.info("Getting available languages...")
    lang_dir = "lang"
    languages = [f.split("_")[0] for f in os.listdir(lang_dir) if f.endswith("_settings.json")]
    logging.info(f"Available languages: {languages}")
    return languages

# Save settings back to settings.json
def save_settings():
    try:
        logging.info("Saving settings...")
        settings_path = os.path.join("dat", "settings.json")
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)
        messagebox.showinfo(settings_language["settings_save_title"], settings_language["settings_save_message"])
        logging.info("Settings saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save settings: {e}")
        messagebox.showerror(settings_language["settings_error_title"], f"{settings_language['settings_save_error']}: {e}")

# Function to change the language
def change_language(new_language):
    logging.info(f"Changing language to: {new_language}")
    settings["language"] = new_language
    save_settings()

# Function to send an email with log content as the body
def send_report_issue():
    try:
        logging.info("Preparing to report issue via email...")
        email = "samuellabant@gmail.com"  # Your email address
        subject = settings_language["settings_email_subject"]

        # Read the content of the log file
        log_path = os.path.join("dat", "app.log")
        if os.path.exists(log_path):
            with open(log_path, 'r') as log_file:
                log_content = log_file.read()
        else:
            log_content = settings_language["settings_log_file_not_found"]

        # Prepare the mailto link with the log content as the email body
        body = f"{settings_language['settings_email_body']}\n\n{log_content}"
        mailto_link = f"mailto:{email}?subject={subject}&body={body}"

        # Open the default email client with the mailto link
        webbrowser.open(mailto_link)
        messagebox.showinfo(settings_language["report_issue_title"], settings_language["report_issue_message"])
        logging.info("Issue report email prepared with log content.")
    except Exception as e:
        logging.error(f"Failed to prepare the email: {e}")
        messagebox.showerror(settings_language["settings_error_title"], f"{settings_language['settings_email_send_error']}: {e}")

# Initialize the UI
logging.info("Initializing UI...")
app = customtkinter.CTk()
app.geometry("400x300")
app.title(settings_language["settings_title"])

# Label for language selection
language_label = customtkinter.CTkLabel(master=app, text=settings_language["settings_select_language"])
language_label.pack(pady=10)

# Dropdown for selecting language
available_languages = get_available_languages()
language_var = customtkinter.StringVar(value=settings["language"])
language_dropdown = customtkinter.CTkOptionMenu(master=app, variable=language_var, values=available_languages, command=change_language)
language_dropdown.pack(pady=10)

# Button to save settings
save_button = customtkinter.CTkButton(master=app, text=settings_language["settings_save_button"], command=lambda: save_settings())
save_button.pack(pady=10)

# Button to report an issue (send email with log content)
report_issue_button = customtkinter.CTkButton(master=app, text=settings_language["settings_report_issue_button"], command=send_report_issue)
report_issue_button.pack(pady=10)

# Button to view the app.log file
def view_log_file():
    log_path = os.path.join("dat", "app.log")
    if os.path.exists(log_path):
        os.system(f'open "{log_path}"')  # Use 'start' on Windows, 'open' on macOS, and 'xdg-open' on Linux
        logging.info("Log file opened successfully.")
    else:
        logging.error("Log file not found.")
        messagebox.showerror(settings_language["settings_error_title"], settings_language["settings_log_file_not_found"])

view_log_button = customtkinter.CTkButton(master=app, text=settings_language["settings_view_log_button"], command=view_log_file)
view_log_button.pack(pady=10)

logging.info("Starting the settings application...")
app.mainloop()
logging.info("Settings application closed.")
