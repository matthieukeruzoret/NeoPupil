try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import main_plots as main
    import customtkinter
    from tkinter import filedialog, messagebox
    from PIL import Image
    import webbrowser
except ImportError as e:
    messagebox.showerror("Critical Error", f"Missing library: {e}. Make sure you have installed all requirements (e.g., pandas).")
    exit()

# Set the theme for the application
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    """
    Main application window for NeoPupil.

    Builds and organizes the user interface using multiple frames for:
    file selection, event selection, plot customization, and output generation.

    Attributes
    ----------
    Output_Frame : Output_Frame
        Frame for selecting the output folder.
    Input_Frame : Input_Frame
        Frame for selecting required input data files.
    Selected_Frame : Select_Events
        Frame for selecting start and end events from the events file.
    Col_Int_Frame : Col_Int_Frame
        Frame for selecting plot colors and time intervals.
    Generate_Frame : Generate_Frame
        Frame containing the button to generate plots.
    Credits_Frame : Credits_Frame
        Frame displaying credits and a GitHub link.
    Logo_Frame : Logo_Frame
        Frame displaying the NeoPupil logo.
    """
    def __init__(self):
        super().__init__()

        # Creating the graphical interface 
        self.title("NeoPupil")
        self.iconbitmap("NeoPupil.ico")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{w}x{h}")
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # First frame (Output)
        self.Output_Frame = Output_Frame(self)
        self.Output_Frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Second frame (Input) 
        self.Input_Frame = Input_Frame(self)
        self.Input_Frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Third frame (Event selection)
        self.Selected_Frame = Select_Events(self)
        self.Selected_Frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Fourth frame (Graph color and time interval)
        self.Col_Int_Frame = Col_Int_Frame(self)
        self.Col_Int_Frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Fifth frame (Generate plots)
        self.Generate_Frame = Generate_Frame(self)
        self.Generate_Frame.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Sixth frame (Credits)
        self.Credits_Frame = Credits_Frame(self)
        self.Credits_Frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nw")

        # Seventh frame (Logo)
        self.Logo_Frame = Logo_Frame(self)
        self.Logo_Frame.grid(row=1,column=1, padx=10, pady=(10, 0), sticky="nw")

class Output_Frame(customtkinter.CTkFrame):
    """
    Frame for selecting the output folder.

    Attributes
    ----------
    name_output : CTkLabel
        Label describing this frame.
    output_folder : CTkEntry
        Entry for displaying the selected folder path.
    select_folder_button : CTkButton
        Button for opening a folder selection dialog.
    selected_output_folder : str
        Path to the selected output folder.
    """
    def __init__(self, master):
        super().__init__(master)
        self.name_output = customtkinter.CTkLabel(self, text="1 - Output folder")
        self.name_output.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.output_folder = customtkinter.CTkEntry(self, placeholder_text="Select a folder")
        self.output_folder.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.select_folder_button = customtkinter.CTkButton(self, text="Browse", command=self.select_folder)
        self.select_folder_button.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

        self.selected_output_folder = ""  

    def select_folder(self):
        """
        Open a folder selection dialog.

        Updates both the entry field and `selected_output_folder` with the chosen path.
        """
        folder_path = filedialog.askdirectory()  
        if folder_path:  
            self.output_folder.delete(0, customtkinter.END)
            self.output_folder.insert(0, folder_path)
            self.selected_output_folder = folder_path
            print(f"Output folder selected: {self.selected_output_folder}")

class Input_Frame(customtkinter.CTkFrame):
    """
    Frame for selecting input CSV files.

    Attributes
    ----------
    selected_pupil_file : str
        Path to the pupil data file.
    selected_blinks_file : str
        Path to the blinks data file.
    selected_events_file : str
        Path to the events data file.
    selected_fixations_file : str
        Path to the fixations data file.
    selected_gaze_file : str
        Path to the gaze data file.
    selected_saccades_file : str
        Path to the saccades data file.
    """
    def __init__(self, master):
        super().__init__(master)

        self.name_input = customtkinter.CTkLabel(self, text="2 - Input files")
        self.name_input.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # Pupil file
        self.pupil_file = customtkinter.CTkEntry(self, placeholder_text="Select the 3d_eye_states file")
        self.pupil_file.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_pupil_button = customtkinter.CTkButton(self, text="Browse", command=self.select_pupil)
        self.select_pupil_button.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_pupil_file = ""

        # Blinks file
        self.blinks_file = customtkinter.CTkEntry(self, placeholder_text="Select the blinks file")
        self.blinks_file.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_blinks_button = customtkinter.CTkButton(self, text="Browse", command=self.select_blinks)
        self.select_blinks_button.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_blinks_file = ""

        # Events file
        self.events_file = customtkinter.CTkEntry(self, placeholder_text="Select the events file")
        self.events_file.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_events_button = customtkinter.CTkButton(self, text="Browse", command=self.select_events)
        self.select_events_button.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_events_file = ""

        # Fixations file
        self.fixations_file = customtkinter.CTkEntry(self, placeholder_text="Select the fixations file")
        self.fixations_file.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_fixations_button = customtkinter.CTkButton(self, text="Browse", command=self.select_fixations)
        self.select_fixations_button.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_fixations_file = ""

        # Gaze file
        self.gaze_file = customtkinter.CTkEntry(self, placeholder_text="Select the gaze file")
        self.gaze_file.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_gaze_button = customtkinter.CTkButton(self, text="Browse", command=self.select_gaze)
        self.select_gaze_button.grid(row=5, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_gaze_file = ""

        # Saccades file
        self.saccades_file = customtkinter.CTkEntry(self, placeholder_text="Select the saccades file")
        self.saccades_file.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.select_saccades_button = customtkinter.CTkButton(self, text="Browse", command=self.select_saccades)
        self.select_saccades_button.grid(row=6, column=1, padx=10, pady=(10, 0), sticky="w")
        self.selected_saccades_file = ""

    def select_pupil(self):
        """
        Select the pupil data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.pupil_file.delete(0, customtkinter.END)
            self.pupil_file.insert(0, file_path)
        self.selected_pupil_file = file_path
        print(f"Pupil file: {self.selected_pupil_file}")

    def select_blinks(self):
        """
        Select the blinks data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.blinks_file.delete(0, customtkinter.END)
            self.blinks_file.insert(0, file_path)
        self.selected_blinks_file = file_path
        print(f"Blinks file: {self.selected_blinks_file}")

    def select_events(self):
        """
        Select the events data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.events_file.delete(0, customtkinter.END)
            self.events_file.insert(0, file_path)
        self.selected_events_file = file_path
        print(f"Events file: {self.selected_events_file}")

    def select_fixations(self):
        """
        Select the fixations data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.fixations_file.delete(0, customtkinter.END)
            self.fixations_file.insert(0, file_path)
        self.selected_fixations_file = file_path
        print(f"Fixations file: {self.selected_fixations_file}")

    def select_gaze(self):
        """
        Select the gaze data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.gaze_file.delete(0, customtkinter.END)
            self.gaze_file.insert(0, file_path)
        self.selected_gaze_file = file_path
        print(f"Gaze file: {self.selected_gaze_file}")

    def select_saccades(self):
        """
        Select the saccades data file.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.saccades_file.delete(0, customtkinter.END)
            self.saccades_file.insert(0, file_path)
        self.selected_saccades_file = file_path
        print(f"Saccades file: {self.selected_saccades_file}")
        
class Select_Events(customtkinter.CTkFrame):
    """
    Frame for selecting start and end events from the events file.

    Attributes
    ----------
    start_event : str
        Name of the event to mark the start of the analysis period.
    end_event : str
        Name of the event to mark the end of the analysis period.
    """
    def __init__(self, master):
        super().__init__(master)
        self.name_selected = customtkinter.CTkLabel(self, text="3 - Select Events")
        self.name_selected.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.explanation = customtkinter.CTkLabel(self, text="Select start and end events to define an interval.")
        self.explanation.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.event_names = ["-- No events loaded --"]
        self.start_menu = customtkinter.CTkOptionMenu(self, values=self.event_names)
        self.start_menu.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.end_menu = customtkinter.CTkOptionMenu(self, values=self.event_names)
        self.end_menu.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.load_button = customtkinter.CTkButton(self, text="Load Events", command=self.load_events)
        self.load_button.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")

    def load_events(self):
        """
        Load events from the selected events CSV file into the dropdown menus.

        Reads the events file, extracts the unique event names, and populates
        the start and end event selection menus with these values.

        Requires that the user has selected an events file in the `Input_Frame`.

        Raises
        ------
        FileNotFoundError
            If no events file has been selected.
        ValueError
            If the events file does not contain a 'name' column.
        Exception
            For any other errors during file reading or menu population.

        See Also
        --------
        get_selected_events : Retrieve the currently selected start and end events.
        """
        events_path = self.master.Input_Frame.selected_events_file
        if not events_path:
            messagebox.showwarning("Missing file", "Please select an events file first.")
            return
        try:
            df = pd.read_csv(events_path)
            if "name" not in df.columns:
                raise ValueError("Missing 'name' column in events file.")

            unique_events = df["name"].dropna().unique().tolist()

            self.start_menu.configure(values=unique_events)
            self.start_menu.set(unique_events[0])

            self.end_menu.configure(values=unique_events)
            self.end_menu.set(unique_events[-1])

            print("✅ Events loaded in dropdowns.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load events: {e}")

    def get_selected_events(self):
        """
        Get the currently selected start and end events.

        Returns
        -------
        tuple of str
            The start event and end event currently selected in the dropdown menus.

        See Also
        --------
        load_events : Populate the dropdown menus with available events.
        """
        return self.start_menu.get(), self.end_menu.get()


class Col_Int_Frame(customtkinter.CTkFrame):
    """
    Frame for selecting a color and time interval for plots.

    This frame loads available colors from `colours.csv` and time intervals
    from `time.csv`, populating two dropdown menus for user selection.

    Parameters
    ----------
    master : customtkinter.CTk or customtkinter.CTkFrame
        The parent widget in which this frame is placed.

    Attributes
    ----------
    name_col_int : CTkLabel
        Label displaying the frame title.
    explanation : CTkLabel
        Label explaining the color and time interval selection.
    colour_name : str
        Default text for the color menu when no color is selected.
    colour_menu : CTkOptionMenu
        Dropdown menu containing available color options.
    time : str
        Default text for the time menu when no time is selected.
    time_menu : CTkOptionMenu
        Dropdown menu containing available time interval options.

    Raises
    ------
    ValueError
        If the `colours.csv` file is missing the "colour" column,
        or if the `time.csv` file is missing the "time" column.
    Exception
        For any other error during CSV loading or menu population.
    """
    def __init__(self, master):
        super().__init__(master)

        self.name_col_int = customtkinter.CTkLabel(self, text="4 - Colour and Time interval")
        self.name_col_int.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.explanation = customtkinter.CTkLabel(
            self,
            text="Select a colour for your graphics and a time interval (<=60s)."
        )
        self.explanation.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.colour_name = "-- No colour selected --"
        self.colour_menu = customtkinter.CTkOptionMenu(self, values=[self.colour_name])
        self.colour_menu.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.time = "-- No time selected --"
        self.time_menu = customtkinter.CTkOptionMenu(self, values=[self.time])
        self.time_menu.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")

        try:
            df_colours = pd.read_csv("colours.csv")
            if "colour" not in df_colours.columns:
                raise ValueError("Missing 'colour' column in colours file.")

            unique_colour = df_colours["colour"].dropna().unique().tolist()
            self.colour_menu.configure(values=unique_colour)
            self.colour_menu.set(self.colour_name)

        except Exception as e:
            messagebox.showerror("Error", f"Could not show colours: {e}")

        try:
            df_time = pd.read_csv("time.csv")
            if "time" not in df_time.columns:
                raise ValueError("Missing 'time' column in time file.")

            unique_times = [str(t) for t in df_time["time"].dropna().unique().tolist()]
            self.time_menu.configure(values=unique_times)
            self.time_menu.set(self.time)

        except Exception as e:
            messagebox.showerror("Error", f"Could not show time: {e}")

    def get_colour(self):
        """
        Get the currently selected color.

        Returns
        -------
        str
            The selected color from the dropdown menu.
        """
        return self.colour_menu.get()
        
    def get_time(self):
        """
        Get the currently selected time interval.

        Returns
        -------
        str
            The selected time interval (in seconds) from the dropdown menu.
        """
        return self.time_menu.get()

class Generate_Frame(customtkinter.CTkFrame):
    """
    Frame containing the plot generation button.
    """
    def __init__(self, master):
        super().__init__(master)
        self.name_generate = customtkinter.CTkLabel(self, text="5 - Generate plots")
        self.name_generate.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.generate_button = customtkinter.CTkButton(self, text="Generate", command=self.generate_plots)
        self.generate_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

    def generate_plots(self):
        """
        Generate plots based on the provided input files and settings.

        Raises
        ------
        FileNotFoundError
            If any required input file is missing.
        ValueError
            If start or end events are not specified.
        """
        try:
            output_folder = self.master.Output_Frame.selected_output_folder
            pupil_file = self.master.Input_Frame.selected_pupil_file
            blinks_file = self.master.Input_Frame.selected_blinks_file
            events_file = self.master.Input_Frame.selected_events_file
            fixations_file = self.master.Input_Frame.selected_fixations_file
            gaze_file = self.master.Input_Frame.selected_gaze_file
            saccades_file = self.master.Input_Frame.selected_saccades_file
            start_event, end_event = self.master.Selected_Frame.get_selected_events()
            color = self.master.Col_Int_Frame.get_colour()
            time = self.master.Col_Int_Frame.get_time()

            if not all([output_folder, pupil_file, events_file, blinks_file, fixations_file, gaze_file, saccades_file]):
                raise FileNotFoundError("Missing required file(s).")

            if not start_event or not end_event:
                raise ValueError("Start and end events must be specified.")
            
            if not color:
                raise ValueError("No color selected.")
            
            if not time:
                raise ValueError("No time selected.")

            # Call the main plotting function
            main.generate_plots(
                blinks_file=blinks_file,
                pupil_file=pupil_file,
                events_file=events_file,
                fixations_file=fixations_file,
                gaze_file=gaze_file,
                saccades_file=saccades_file,
                output_folder=output_folder,
                start_event=start_event,
                end_event=end_event,
                colour=color,
                time=time
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class Credits_Frame(customtkinter.CTkFrame):
    """
    Frame displaying application credits and GitHub link.
    """
    def __init__(self,master):
        super().__init__(master)

        self.title_credits = customtkinter.CTkLabel(self,text=" Credits")
        self.title_credits.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.credits = customtkinter.CTkLabel(self,text="Matthieu KÉRUZORET")
        self.credits.grid(row=1, column=0, padx=10, sticky="w")

        self.github = customtkinter.CTkLabel(
            self,
            text="🔧GitHub",
            cursor="hand2",
            font=customtkinter.CTkFont(underline=True)
        )
        self.github.grid(row=2, column=0, padx=10, sticky="w")
        self.github.bind("<Button-1>", lambda e: self.open_link())

    def open_link(self):
        webbrowser.open("https://github.com/matthieukeruzoret")

class Logo_Frame(customtkinter.CTkFrame):
    """
    Frame for displaying the application logo.
    """
    def __init__(self, master):
        super().__init__(master)
        try:
            image_path = "NeoPupil.png"
            image = Image.open(image_path)
            self.logo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(80, 80))
            self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
            self.logo_label.grid(row=0, column=1, rowspan=2, padx=20, pady=10)
        except FileNotFoundError:
            self.logo_label = customtkinter.CTkLabel(self, text="[Logo Missing]")
            self.logo_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

if __name__ == "__main__":
    app = App()
    app.mainloop()
