import customtkinter
import os
import json
import datetime
import subprocess
import webbrowser
import logging  # Import logging module for logging
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing, Line

# Set up logging
log_path = os.path.join("dat", "app.log")
logging.basicConfig(filename=log_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load settings
def load_settings():
    try:
        logging.info("Loading settings...")
        settings_path = os.path.join("dat", "settings.json")
        with open(settings_path, "r") as f:
            settings = json.load(f)
        logging.info("Settings loaded successfully.")
        return settings
    except Exception as e:
        logging.error(f"Failed to load settings: {e}")
        raise

def load_language(language_code):
    try:
        logging.info(f"Loading language file for: {language_code}")
        lang_path = os.path.join("lang", f"{language_code}.json")
        with open(lang_path, "r") as f:
            language = json.load(f)
        logging.info("Language file loaded successfully.")
        return language
    except Exception as e:
        logging.error(f"Failed to load language file: {e}")
        raise


# Load the settings and language
settings = load_settings()
language = load_language(settings["language"])

# Initialize the UI
logging.info("Initializing UI...")
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1100x800")
app.title(language["title"])
app.resizable(False, False)
logging.info("UI initialized successfully.")

# Create the sidebar menu with additional features
side_bar_frame = customtkinter.CTkFrame(master=app, width=160, height=780, corner_radius=10)
side_bar_frame.place(x=10, y=10)

# Title of the Menu
menu_title_label = customtkinter.CTkLabel(master=side_bar_frame, text=language["menu_title"], font=("Arial", 18, "bold"))
menu_title_label.place(x=55, y=10)

# Button to Open GitHub
github_button = customtkinter.CTkButton(master=side_bar_frame, text=language["github_button"], command=lambda: open_github())
github_button.place(x=10, y=60)

# Button to send an email
email_button = customtkinter.CTkButton(master=side_bar_frame, text=language["email_button"], command=lambda: send_email())
email_button.place(x=10, y=100)

# Button to Open Settings
settings_button = customtkinter.CTkButton(master=side_bar_frame, text=language["settings_button"], command=lambda: open_settings())
settings_button.place(x=10, y=140)

# Label for Author Information
author_label = customtkinter.CTkLabel(master=side_bar_frame, text=language["author_info"], font=("Arial", 13, "italic"))
author_label.place(x=30, y=710)

# Function to open GitHub in the web browser
def open_github():
    logging.info("Opening GitHub...")
    webbrowser.open("https://github.com/samuel-lab")  # Replace with your actual GitHub URL
    logging.info("GitHub opened successfully.")

# Function to open the settings.py file

def open_settings():
    try:
        logging.info("Opening settings...")
        # Get the current Python interpreter
        python_executable = sys.executable
        # Get the absolute path to the settings.py script
        script_path = os.path.abspath("settings.py")
        # Run the settings.py script using the current Python interpreter
        subprocess.run([python_executable, script_path], check=True)
        logging.info("Settings opened successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to open settings: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Function to open the user's email client with a pre-filled email
def send_email():
    logging.info("Preparing to send email...")
    email = "samuellabant@gmail.com"  # Replace with your actual email address
    subject = language["email_subject"]
    body = language["email_body"]
    mailto_link = f"mailto:{email}?subject={subject}&body={body}"
    webbrowser.open(mailto_link)
    logging.info("Email client opened successfully.")

# Main Segment Frame (Header)
header_frame = customtkinter.CTkFrame(master=app, width=910, height=130)
header_frame.place(x=180, y=10)

# Title in the middle
title_label = customtkinter.CTkLabel(master=header_frame, text=language["app_title"], font=("Arial", 24, "bold"))
title_label.place(relx=0.5, y=20, anchor="center")

# File Name Entry
file_name_label = customtkinter.CTkLabel(master=header_frame, text=language["file_name"])
file_name_label.place(x=10, y=60)
file_name_entry = customtkinter.CTkEntry(master=header_frame, width=250)
file_name_entry.place(x=120, y=60)

# Controller Name Entry
controller_name_label = customtkinter.CTkLabel(master=header_frame, text=language["controller_name"])
controller_name_label.place(x=10, y=90)
controller_name_entry = customtkinter.CTkEntry(master=header_frame, width=250)
controller_name_entry.place(x=120, y=90)

# Current Date (Automatically populated)
current_date_label = customtkinter.CTkLabel(master=header_frame, text=language["current_date"])
current_date_label.place(x=400, y=60)
current_date_value = customtkinter.CTkLabel(master=header_frame, text=datetime.datetime.now().strftime("%Y-%m-%d"))
current_date_value.place(x=520, y=60)

# File Type Dropdown (Additional Feature)
file_type_label = customtkinter.CTkLabel(master=header_frame, text=language["file_type"])
file_type_label.place(x=400, y=90)
file_type_options = ["Python", "JavaScript", "HTML", "CSS", "Other"]
file_type_var = customtkinter.StringVar(value=file_type_options[0])
file_type_dropdown = customtkinter.CTkOptionMenu(master=header_frame, variable=file_type_var, values=file_type_options)
file_type_dropdown.place(x=520, y=90)

# Complete Button to generate PDF
complete_button = customtkinter.CTkButton(master=header_frame, text=language["complete_button"], command=lambda: generate_pdf_from_form())
complete_button.place(x=760, y=75)

# Scrollable frame for segments
segments_frame_main = customtkinter.CTkScrollableFrame(master=app, width=890, height=570)
segments_frame_main.place(x=180, y=150)

segments = []

# Function to delete a segment
def delete_segment(frame, segment_index):
    logging.info(f"Deleting segment {segment_index + 1}...")
    frame.destroy()
    segments.pop(segment_index)
    update_segment_numbers()
    logging.info(f"Segment {segment_index + 1} deleted.")

# Function to update segment numbers after deletion
def update_segment_numbers():
    logging.info("Updating segment numbers...")
    for index, segment in enumerate(segments):
        segment['number_label'].configure(text=f"{language['segment_title_main']} {index + 1}")
    logging.info("Segment numbers updated.")

# Function to add a new segment
def add_segment():
    logging.info("Adding new segment...")
    segment_index = len(segments)
    segments_frame = customtkinter.CTkFrame(master=segments_frame_main, width=880, height=180, fg_color="#404040")
    segments_frame.pack(pady=10, padx=10)
    
    # Number Label
    number_label = customtkinter.CTkLabel(master=segments_frame, text=f"{language['segment_title_main']} {segment_index + 1}")
    number_label.place(x=10, y=10)
    
    # "Line From" Entry
    line_from_label = customtkinter.CTkLabel(master=segments_frame, text=language["line_from"])
    line_from_label.place(x=10, y=40)
    line_from_entry = customtkinter.CTkEntry(master=segments_frame, width=100)
    line_from_entry.place(x=100, y=40)
    
    # "Line To" Entry
    line_to_label = customtkinter.CTkLabel(master=segments_frame, text=language["line_to"])
    line_to_label.place(x=10, y=70)
    line_to_entry = customtkinter.CTkEntry(master=segments_frame, width=100)
    line_to_entry.place(x=100, y=70)
    
    # "Description" Entry with scrolling and wrapping
    description_label = customtkinter.CTkLabel(master=segments_frame, text=language["description"])
    description_label.place(x=220, y=10)
    description_textbox = customtkinter.CTkTextbox(master=segments_frame, width=620, height=100, wrap="word")
    description_textbox.place(x=220, y=40)
    
    # Setting scrolling to top-right corner and starting cursor at the top
    description_textbox.insert("1.0", "")  # To ensure the cursor starts at the top
    description_textbox.yview_moveto(0)  # Move the scrollbar to the top
    description_textbox.xview_moveto(0)  # Move the scrollbar to the far left
    
    # Dropdown Menu for segment type
    menu_label = customtkinter.CTkLabel(master=segments_frame, text=language["menu_label"])
    menu_label.place(x=10, y=110)
    menu_options = [language["menu_option_note"], language["menu_option_possible_problem"], language["menu_option_error"]]
    menu_var = customtkinter.StringVar(value=menu_options[0])
    menu_dropdown = customtkinter.CTkOptionMenu(master=segments_frame, variable=menu_var, values=menu_options)
    menu_dropdown.place(x=10, y=140)

    # Delete Button to remove a segment
    delete_button = customtkinter.CTkButton(master=segments_frame, text=language["delete_button"], command=lambda: delete_segment(segments_frame, segment_index))
    delete_button.place(x=720, y=145)
    
    segments.append({"frame": segments_frame, "number_label": number_label, "line_from_entry": line_from_entry, "line_to_entry": line_to_entry, "description_textbox": description_textbox, "menu_var": menu_var})
    update_segment_numbers()
    logging.info(f"Segment {segment_index + 1} added.")

# Function to display information in a pop-up window
def show_information():
    logging.info("Displaying information window...")
    info_window = customtkinter.CTkToplevel(app)
    info_window.title(language["information_title"])
    info_window.geometry("500x450")
    
    # Create a frame to hold the information content
    content_frame = customtkinter.CTkFrame(master=info_window, width=480, height=360, corner_radius=10)
    content_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Add a title label
    info_title_label = customtkinter.CTkLabel(master=content_frame, text=language["information_title"], font=("Arial", 18, "bold"))
    info_title_label.pack(pady=(10, 20))
    
    # Add the information text with sections
    info_text = (
        f"{language['info_intro']}\n\n"
        f"1. {language['info_step1_title']}\n   {language['info_step1_text']}\n\n"
        f"2. {language['info_step2_title']}\n   {language['info_step2_text']}\n\n"
        f"3. {language['info_step3_title']}\n   {language['info_step3_text']}\n\n"
        f"4. {language['info_step4_title']}\n   {language['info_step4_text']}\n\n"
        f"{language['info_outro']}"
    )

    # Use a Textbox or Label for the text to allow wrapping
    info_label = customtkinter.CTkTextbox(master=content_frame, wrap="word", height=250, border_width=0, corner_radius=10)
    info_label.insert("1.0", info_text)
    info_label.configure(state="disabled")  # Disable editing
    info_label.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Close button
    close_button = customtkinter.CTkButton(master=info_window, text=language["close_button"], command=info_window.destroy)
    close_button.pack(pady=(10, 20))
    logging.info("Information window displayed.")

# Function to generate PDF from form data
def generate_pdf_from_form():
    logging.info("Generating PDF from form data...")
    # Gather data from the form
    app_data = {
        'app_title': language["app_title"],
        'file_name_label': language["file_name"],
        'file_name': file_name_entry.get(),
        'controller_name_label': language["controller_name"],
        'controller_name': controller_name_entry.get(),
        'current_date_label': language["current_date"],
        'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'file_type_label': language["file_type"],
        'file_type': file_type_var.get()
    }
    
    segments_data = []
    for segment in segments:
        line_from = segment["line_from_entry"].get()
        line_to = segment["line_to_entry"].get() or line_from  # Use line_from if line_to is empty
        description = segment["description_textbox"].get("1.0", "end").strip()
        menu_option = segment["menu_var"].get()
        
        segment_data = {
            'segment_title_main': language["segment_title_main"],
            'line_from_label': language["line_from"],
            'line_from': line_from,
            'line_to_label': language["line_to"],
            'line_to': line_to,
            'description_label': language["description"],
            'description': description,
            'menu_label': language["menu_label"],
            'menu_option': menu_option
        }
        segments_data.append(segment_data)
    
    # Always save the PDF as output.pdf
    output_path = 'output.pdf'
    
    # Generate the PDF
    generate_pdf(output_path, app_data, segments_data)
    logging.info(f"PDF generated and saved to {output_path}")

# Function to generate the actual PDF
def generate_pdf(output_path, app_data, segments_data):
    logging.info(f"Creating PDF document at {output_path}...")
    # Create a PDF document
    pdf = SimpleDocTemplate(output_path, pagesize=A4, title=app_data['app_title'], author="Your App")
    
    # Use sample stylesheet from reportlab
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B8BBE"),
        fontName="Helvetica-Bold"
    )

    header_style = ParagraphStyle(
        name="HeaderStyle",
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#306998"),
        fontName="Helvetica-Bold"
    )

    normal_style = ParagraphStyle(
        name="NormalStyle",
        fontSize=12,
        leading=15,
        alignment=TA_LEFT,
        textColor=colors.black,
        fontName="Helvetica"
    )

    # Elements to be added to the PDF
    elements = []

    # Add title
    title = Paragraph(f"{app_data['app_title']}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Add file and controller name info
    elements.append(Paragraph(f"<strong>{app_data['file_name_label']}:</strong> {app_data['file_name']}", normal_style))
    elements.append(Paragraph(f"<strong>{app_data['controller_name_label']}:</strong> {app_data['controller_name']}", normal_style))
    elements.append(Paragraph(f"<strong>{app_data['current_date_label']}:</strong> {app_data['current_date']}", normal_style))
    elements.append(Paragraph(f"<strong>{app_data['file_type_label']}:</strong> {app_data['file_type']}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Iterate over each segment and add its data
    for index, segment in enumerate(segments_data):
        # Segment Title
        segment_title = Paragraph(f"{segment['segment_title_main']} {index + 1}", header_style)
        elements.append(segment_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Line Info
        line_info = Paragraph(f"{segment['line_from_label']} {segment['line_from']} - {segment['line_to_label']} {segment['line_to']}", normal_style)
        elements.append(line_info)
        elements.append(Spacer(1, 0.05 * inch))
        
        # Description
        description = Paragraph(f"<strong>{segment['description_label']}:</strong> {segment['description']}", normal_style)
        elements.append(description)
        elements.append(Spacer(1, 0.05 * inch))
        
        # Menu Option
        menu_option = Paragraph(f"<strong>{segment['menu_label']}:</strong> {segment['menu_option']}", normal_style)
        elements.append(menu_option)
        
        # Add a thin line to separate segments
        elements.append(Spacer(1, 0.2 * inch))
        d = Drawing(500, 1)
        d.add(Line(0, 0, 500, 0))
        elements.append(d)
        elements.append(Spacer(1, 0.2 * inch))

    # Build the PDF
    pdf.build(elements)
    logging.info(f"PDF built successfully and saved to {output_path}.")

# Add the initial 2 segments when the application starts
for _ in range(2):
    add_segment()

# Add Segment Button
add_segment_button = customtkinter.CTkButton(master=app, text=language["add_segment_button"], command=add_segment, width=800)
add_segment_button.place(x=180, y=760)

# Information Button
info_button = customtkinter.CTkButton(master=app, text=language["information_button"], command=show_information, width=100)
info_button.place(x=990, y=760)

# Start the Tkinter event loop
logging.info("Starting the application...")
app.mainloop()
logging.info("Application closed.")
