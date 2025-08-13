import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox

def format_time(sec):
    """
    Format seconds into a string representing minutes and seconds.

    Parameters
    ----------
    sec : float or int
        Time duration in seconds.

    Returns
    -------
    str
        Formatted time string in "XmYs" or "Xs" format.
    """
    if sec < 60:
        return f"{int(sec)}s"
    else:
        m, s = int(sec // 60), int(sec % 60)
        return f"{m}m{s}s" if s else f"{m}m"

def generate_mean_std_plot_between_events(df, events_df, start_ts, end_ts, label, output_folder, colour):
    """
    Generate bar plot of mean and standard deviation of event durations between pairs of events.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing event durations and timestamps.
    events_df : pandas.DataFrame
        DataFrame containing event timestamps and names.
    start_ts : int
        Start timestamp in nanoseconds for filtering events.
    end_ts : int
        End timestamp in nanoseconds for filtering events.
    label : str
        Label for the type of events (e.g., 'blinks', 'fixations').
    output_folder : str
        Folder path to save the plot image.
    colour : str
        Color used for plotting bars.

    Returns
    -------
    None
    """
    interval_events = events_df[(events_df["timestamp [ns]"] >= start_ts) &
                                (events_df["timestamp [ns]"] <= end_ts)].reset_index(drop=True)
    results = []

    for i in range(len(interval_events) - 1):
        e1, e2 = interval_events.iloc[i], interval_events.iloc[i + 1]
        mask = (df["start timestamp [ns]"] >= e1["timestamp [ns]"]) & (df["start timestamp [ns]"] < e2["timestamp [ns]"])
        subset = df[mask]

        results.append({
            "label": f"{e1['name']} ➝ {e2['name']}",
            "mean": subset["duration [ms]"].mean(),
            "std": subset["duration [ms]"].std(),
        })

    if results:
        plot_df = pd.DataFrame(results)
        plt.figure(figsize=(12, 6))
        plt.bar(plot_df["label"], plot_df["mean"], yerr=plot_df["std"], capsize=5, color=colour, alpha=0.8)
        plt.xticks(rotation=90)
        plt.ylabel(f"Mean duration of {label} (ms)")
        plt.title(f"{label.capitalize()} between events")
        plt.tight_layout()
        path = os.path.join(output_folder, f"{label}_means_per_event.png")
        plt.savefig(path)
        plt.close()
    else:
        print(f"⚠️ No {label} detected between events.")

def generate_frequency_plot_between_events(df, events_df, start_ts, end_ts, label, output_folder, colour):
    """
    Generate a line plot showing frequency (occurrences per second) of events between pairs of events.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing event durations and timestamps.
    events_df : pandas.DataFrame
        DataFrame containing event timestamps and names.
    start_ts : int
        Start timestamp in nanoseconds for filtering events.
    end_ts : int
        End timestamp in nanoseconds for filtering events.
    label : str
        Label for the type of events (e.g., 'blinks', 'fixations').
    output_folder : str
        Folder path to save the plot image.
    colour : str
        Color used for plotting lines.

    Returns
    -------
    None
    """
    interval_events = events_df[(events_df["timestamp [ns]"] >= start_ts) &
                                (events_df["timestamp [ns]"] <= end_ts)].reset_index(drop=True)
    results = []

    for i in range(len(interval_events) - 1):
        e1, e2 = interval_events.iloc[i], interval_events.iloc[i + 1]
        mask = (df["start timestamp [ns]"] >= e1["timestamp [ns]"]) & (df["start timestamp [ns]"] < e2["timestamp [ns]"])
        subset = df[mask]

        delta_s = (e2["timestamp [ns]"] - e1["timestamp [ns]"]) / 1_000_000_000
        freq = subset["duration [ms]"].count() / delta_s

        results.append({
            "label": f"{e1['name']} ➝ {e2['name']}",
            "freq": freq
        })

    if results:
        plot_df = pd.DataFrame(results)
        plt.figure(figsize=(12, 6))
        plt.plot(plot_df["label"], plot_df["freq"], color=colour)
        plt.xticks(rotation=90)
        plt.ylabel(f"Frequency of {label} (occurrences/second)")
        plt.title(f"{label.capitalize()} between events")
        plt.tight_layout()
        path= os.path.join(output_folder, f"{label}_frequency_per_event.png")
        plt.savefig(path)
        plt.close()
    else:
        print(f"⚠️ No {label} detected between events.")

def generate_time_binned_plots(df, label, start_ts, end_ts, output_folder, colour, time):
    """
    Generate bar plots of mean duration and count of events over time bins within a specified interval.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing event durations and timestamps.
    label : str
        Label for the type of events (e.g., 'blink', 'fixation').
    start_ts : int
        Start timestamp in nanoseconds.
    end_ts : int
        End timestamp in nanoseconds.
    output_folder : str
        Folder path to save the plots.
    colour : str
        Color used for plotting bars.
    time : int or str
        Duration of each time bin in seconds.

    Returns
    -------
    None
    """
    interval_ns = int(time) * 1_000_000_000
    results = []
    current_start = start_ts

    while current_start < end_ts:
        current_end = min(current_start + interval_ns, end_ts)
        mask = (df["start timestamp [ns]"] >= current_start) & (df["start timestamp [ns]"] < current_end)
        subset = df[mask]

        start_sec = (current_start - start_ts) / 1_000_000_000
        end_sec = (current_end - start_ts) / 1_000_000_000
        label_interval = f"{format_time(start_sec)}–{format_time(end_sec)}"

        results.append({
            "interval": label_interval,
            "mean_duration": subset["duration [ms]"].mean(),
            "count": subset["duration [ms]"].count()
        })
        current_start = current_end

    if results:
        plot_df = pd.DataFrame(results)

        plt.figure(figsize=(14, 6))
        plt.bar(plot_df["interval"], plot_df["mean_duration"], color=colour, alpha=0.8)
        plt.xticks(rotation=90)
        plt.ylabel(f"Mean duration of {label} (ms)")
        plt.title(f"{label.capitalize()} means by tranches of {time}s")
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{label}_means_{time}s.png"))
        plt.close()

        plt.figure(figsize=(14, 6))
        plt.bar(plot_df["interval"], plot_df["count"], color=colour, alpha=0.8)
        plt.xticks(rotation=90)
        plt.ylabel(f"Number of {label}")
        plt.title(f"Number of {label} per {time}s increments")
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{label}_count_{time}s.png"))
        plt.close()
    else:
        print(f"⚠️ No {label} detected in the interval.")

def gaze_plot(df, events_df, start_ts, end_ts, label, output_folder, colour):
    """
    Generate gaze path plots between pairs of events and aggregate gaze plot over the entire interval.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing gaze data with timestamps and coordinates.
    events_df : pandas.DataFrame
        DataFrame containing event timestamps and names.
    start_ts : int
        Start timestamp in nanoseconds.
    end_ts : int
        End timestamp in nanoseconds.
    label : str
        Label used for naming plots.
    output_folder : str
        Folder path to save gaze plots.
    colour : str
        Color used for plotting gaze paths.

    Returns
    -------
    None
    """
    interval_events = events_df[(events_df["timestamp [ns]"] >= start_ts) &
                                (events_df["timestamp [ns]"] <= end_ts)].reset_index(drop=True)

    all_points = []

    gaze_plots_folder = os.path.join(output_folder, f"gaze_plots_{label}")
    os.makedirs(gaze_plots_folder, exist_ok=True)

    for i in range(len(interval_events) - 1):
        e1, e2 = interval_events.iloc[i], interval_events.iloc[i + 1]
        mask = (df["timestamp [ns]"] >= e1["timestamp [ns]"]) & (df["timestamp [ns]"] < e2["timestamp [ns]"])
        subset = df[mask][["gaze x [px]", "gaze y [px]"]].dropna()

        if not subset.empty:
            all_points.append(subset)

            fig_i, ax_i = plt.subplots()
            ax_i.plot(subset["gaze x [px]"], subset["gaze y [px]"], alpha=0.7, linewidth=1,color=colour)
            ax_i.set_title(f"Gaze Path between {e1['name']} and {e2['name']}")
            ax_i.set_xlabel("Gaze X [px]")
            ax_i.set_ylabel("Gaze Y [px]")
            ax_i.set_xlim(subset["gaze x [px]"].min(), subset["gaze x [px]"].max())
            ax_i.set_ylim(subset["gaze y [px]"].min(), subset["gaze y [px]"].max())
            ax_i.invert_yaxis()

            path_fig = os.path.join(gaze_plots_folder, f"gaze_path_{e1['name']} ➝ {e2['name']}.png")
            fig_i.savefig(path_fig)
            plt.close(fig_i)

    if all_points:
        fig, ax = plt.subplots()
        for subset in all_points:
            ax.plot(subset["gaze x [px]"], subset["gaze y [px]"], alpha=0.6, linewidth=1)

        plot_df = pd.concat(all_points, ignore_index=True)
        ax.set_title(f"Gaze plot - {label}")
        ax.set_xlabel("Gaze X [px]")
        ax.set_ylabel("Gaze Y [px]")
        ax.set_xlim(plot_df["gaze x [px]"].min(), plot_df["gaze x [px]"].max())
        ax.set_ylim(plot_df["gaze y [px]"].min(), plot_df["gaze y [px]"].max())
        ax.invert_yaxis()

        os.makedirs(output_folder, exist_ok=True)
        fig_path = os.path.join(output_folder, f"gaze_plot_{label}.png")
        fig.savefig(fig_path)
        plt.close(fig)
    else:
        print(f"⚠️ No gaze point detected between events ({label}).")

def pupils_diameter_time_binned_plot(df, events_df, start_ts, end_ts, label, output_folder, colour, time):
    """
    Generate bar plot of mean pupil diameter over time bins within a specified interval.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing pupil diameter data and timestamps.
    events_df : pandas.DataFrame
        DataFrame containing event timestamps.
    start_ts : int
        Start timestamp in nanoseconds.
    end_ts : int
        End timestamp in nanoseconds.
    label : str
        Label for the pupil data.
    output_folder : str
        Folder path to save the plot.
    colour : str
        Color used for plotting bars.
    time : int or str
        Duration of each time bin in seconds.

    Returns
    -------
    None
    """
    interval_ns = int(time) * 1_000_000_000
    results = []
    current_start = start_ts

    while current_start < end_ts:
        current_end = min(current_start + interval_ns, end_ts)
        mask = (df["timestamp [ns]"] >= current_start) & (df["timestamp [ns]"] < current_end)
        subset = df[mask]

        start_sec = (current_start - start_ts) / 1_000_000_000
        end_sec = (current_end - start_ts) / 1_000_000_000
        label_interval = f"{format_time(start_sec)}–{format_time(end_sec)}"

        results.append({
            "interval": label_interval,
            "mean_diameter": ((subset["pupil diameter left [mm]"] + subset["pupil diameter right [mm]"]) / 2).mean(),
        })
        current_start = current_end

    if results:
        plot_df = pd.DataFrame(results)

        plt.figure(figsize=(14, 6))
        plt.bar(plot_df["interval"], plot_df["mean_diameter"], color=colour, alpha=0.8)
        plt.xticks(rotation=90)
        plt.ylabel(f"Mean diameter of {label} (mm)")
        plt.title(f"Mean {label} diameter over time ({time}s bins)")
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{label}_diameter_means_{time}s.png"))
        plt.close()
    else:
        print(f"⚠️ No {label} detected in the interval.")

def pupils_diameter_plot_between_events(df, events_df, start_ts, end_ts, label, output_folder, colour):
    """
    Plot mean pupil diameter between consecutive events.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing pupil diameter data with columns
        'timestamp [ns]', 'pupil diameter left [mm]', and 'pupil diameter right [mm]'.
    events_df : pandas.DataFrame
        DataFrame with events including 'timestamp [ns]' and 'name' columns.
    start_ts : int
        Start timestamp in nanoseconds for the interval.
    end_ts : int
        End timestamp in nanoseconds for the interval.
    label : str
        Label describing the data type (used for plot titles and filenames).
    output_folder : str
        Path to folder where the plot image will be saved.
    colour : str
        Color to be used in the plot.

    Returns
    -------
    None
        Saves a bar plot of mean pupil diameters per event interval to disk.
        Prints a warning if no data is detected between events.
    """
    interval_events = events_df[(events_df["timestamp [ns]"] >= start_ts) &
                                (events_df["timestamp [ns]"] <= end_ts)].reset_index(drop=True)
    results = []

    for i in range(len(interval_events) - 1):
        e1, e2 = interval_events.iloc[i], interval_events.iloc[i + 1]
        mask = (df["timestamp [ns]"] >= e1["timestamp [ns]"]) & (df["timestamp [ns]"] < e2["timestamp [ns]"])
        subset = df[mask]

        results.append({
            "label": f"{e1['name']} ➝ {e2['name']}",
            "mean_diameter": ((subset["pupil diameter left [mm]"] + subset["pupil diameter right [mm]"]) / 2).mean(),
        })

    if results:
        plot_df = pd.DataFrame(results)

        plt.figure(figsize=(14, 6))
        plt.bar(plot_df["label"], plot_df["mean_diameter"], color=colour, alpha=0.8)
        plt.xticks(rotation=90)
        plt.ylabel(f"Mean diameter of {label} (mm)")
        plt.title(f"Mean {label} diameter between events")
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{label}_diameter_means_per_event.png"))
        plt.close()
    else:
        print(f"⚠️ No {label} detected between events.")

def generate_plots(blinks_file, pupil_file, events_file, fixations_file, gaze_file, saccades_file, output_folder, start_event=None, end_event=None, colour=None, time=None):
    """
    Generate various plots from eye-tracking data files and save them to an output folder.

    Parameters
    ----------
    blinks_file : str
        Path to CSV file containing blink data.
    pupil_file : str
        Path to CSV file containing pupil diameter data.
    events_file : str
        Path to CSV file containing event timestamps and names.
    fixations_file : str
        Path to CSV file containing fixation data.
    gaze_file : str
        Path to CSV file containing gaze point data.
    saccades_file : str
        Path to CSV file containing saccade data.
    output_folder : str
        Directory path where generated plots will be saved.
    start_event : str, optional
        Name of the starting event for interval-based analyses (default is None).
    end_event : str, optional
        Name of the ending event for interval-based analyses (default is None).
    colour : str, optional
        Color used in plotting (default is None). Must be provided to generate plots.
    time : int or float, optional
        Time bin size in seconds for binned plots (default is None).

    Returns
    -------
    None
        Saves multiple plots as PNG files in the specified output folder.
        Displays message boxes on successful plot generation or errors.
        Prints warnings if data or parameters are missing.
    """
    try:
        print("📥 Uploading files...")
        blinks_df = pd.read_csv(blinks_file)
        events_df = pd.read_csv(events_file)
        fixations_df = pd.read_csv(fixations_file)
        gaze_df = pd.read_csv(gaze_file)
        saccades_df = pd.read_csv(saccades_file)
        pupil_df = pd.read_csv(pupil_file)

        os.makedirs(output_folder, exist_ok=True)
        print("📁 Output folder ready.")

        if colour :
            # Blink plots
            plt.figure(figsize=(15, 7))
            plt.plot(blinks_df["start timestamp [ns]"], blinks_df["duration [ms]"], "x-",color = colour)
            plt.title("Blink duration over time")
            plt.xlabel("Events")
            plt.ylabel("Duration (ms)")
            plt.grid(True)

            unique_event_labels = events_df.drop_duplicates(subset=["timestamp [ns]"])
            plt.xticks(
                ticks=unique_event_labels["timestamp [ns]"],
                labels=unique_event_labels["name"],
                rotation=90,
                ha="center"
            )
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, "blinks_duration_per_event.png"))
            plt.close()

            plt.figure(figsize=(8, 5))
            plt.hist(
                blinks_df["duration [ms]"],
                bins=range(int(blinks_df["duration [ms]"].min()) - 10, int(blinks_df["duration [ms]"].max()) + 10, 10),
                color=colour,
                edgecolor='black'
            )
            plt.title("Distribution of blink durations")
            plt.xlabel("Duration (ms)")
            plt.ylabel("Count")
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, "blink_duration_histogram.png"))
            plt.close()
            messagebox.showinfo("Success","Blink Plots generated successfully.")
        else :
            raise NameError("You have not entered a color.")

        if start_event and end_event and colour and time:
            print(f"⏱ Analyzing data between '{start_event}' and '{end_event}'...")

            start_row = events_df[events_df["name"] == start_event]
            end_row = events_df[events_df["name"] == end_event]

            if start_row.empty or end_row.empty:
                print("⚠️ One of the start or end events does not exist.")
                return

            start_ts = start_row["timestamp [ns]"].iloc[0]
            end_ts = end_row["timestamp [ns]"].iloc[0]

            if start_ts >= end_ts:
                raise ValueError("The start event is after the end event.")

            # Plots between pairs of events
            generate_mean_std_plot_between_events(blinks_df, events_df, start_ts, end_ts, "blinks", output_folder,colour)
            generate_mean_std_plot_between_events(fixations_df, events_df, start_ts, end_ts, "fixations", output_folder,colour)
            generate_mean_std_plot_between_events(saccades_df, events_df, start_ts, end_ts, "saccades", output_folder,colour)

            generate_frequency_plot_between_events(blinks_df, events_df, start_ts, end_ts, "blinks", output_folder,colour)
            generate_frequency_plot_between_events(fixations_df, events_df, start_ts, end_ts, "fixations", output_folder,colour)
            generate_frequency_plot_between_events(saccades_df, events_df, start_ts, end_ts, "saccades", output_folder,colour)

            for df, label in [
                (fixations_df, "fixation"),
                (blinks_df, "blink"),
                (saccades_df, "saccade")
            ]:
                generate_time_binned_plots(df, label, start_ts, end_ts, output_folder,colour,time)

            # Gaze plot
            gaze_plot(gaze_df,events_df,start_ts, end_ts, "gaze", output_folder,colour)

            # Pupil plots
            pupils_diameter_time_binned_plot(pupil_df,events_df,start_ts, end_ts, "pupils", output_folder,colour,time)
            pupils_diameter_plot_between_events(pupil_df,events_df,start_ts, end_ts, "pupils", output_folder,colour)

            print("✅ All plots have been generated successfully.")
            messagebox.showinfo("Success", "Plots generated successfully.")
        else :
            raise NameError("You have not provided the following variable(s): start_event, end_event, colour, time.")

    except Exception as e:
        print(f"❌ Error : {e}")