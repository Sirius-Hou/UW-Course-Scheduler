# import matplotlib.pyplot as plt
# import matplotlib.patches as patches

# def plot_schedule(events):
#     fig, ax = plt.subplots(figsize=(12, 14))
#     ax.set_xlim(0, 5)
#     ax.set_ylim(-28, 0)
#     #ax.invert_yaxis()

#     # Draw grid
#     for i in range(8):
#         ax.axvline(x=i, color='black', lw=1)
#     for i in range(-28, 0, 2):
#         ax.axhline(y=i, color='black', lw=1)

#     # Label days and hours
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     hours = ['10:00 PM', '9:00 PM', '8:00 PM', '7:00 PM', '6:00 PM', '5:00 PM', '4:00 PM', '3:00 PM', '2:00 PM', '1:00 PM', '12:00 PM', '11:00 AM', '10:00 AM', '9:00 AM', '8:00 AM']
#     ax.set_xticks(range(5))
#     ax.set_xticklabels(days, rotation=45, ha='center')

#     ax.set_yticks(range(-28, 2, 2))
#     ax.set_yticklabels(hours)

#     # Add events
#     for event in events:
#         day, start_time, end_time, subject = event
#         day_idx = days.index(day)
#         start_idx = -(start_time - 8) * 2
#         end_idx = -(end_time - 8) * 2
#         if start_time % 1 != 0:
#             start_idx -= 1
#         if end_time % 1 != 0:
#             end_idx -= 1
#         ax.add_patch(patches.Rectangle((day_idx, start_idx), 1, end_idx - start_idx, edgecolor='black', facecolor='blue', alpha=0.5))
#         plt.text(day_idx + 0.5, (start_idx + end_idx) / 2, subject, ha='center', va='center', color='white')

#     plt.show()

# # Define the event
# event = ('Monday', 9.5, 10.333, 'CS241')

# # Plot the schedule with the event
# plot_schedule([event])

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_schedule(events):
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 5)
    ax.set_ylim(0, -28)
    ax.invert_yaxis()

    # Draw grid
    for i in range(8):
        ax.axvline(x=i, color='black', lw=1)
    for i in range(0, -30, -2):
        ax.axhline(y=i, color='black', lw=1)

    # Label days and hours
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = ['8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM']
    ax.set_xticks(range(5))
    ax.set_xticklabels(days, rotation=45, ha='center')
    ax.xaxis.set_label_position('top')  # Move day labels to top of graph

    ax.set_yticks(range(0, -30, -2))
    ax.set_yticklabels(hours)

    # Add events
    for event in events:
        day, start_time, end_time, subject = event
        day_idx = days.index(day)
        start_idx = -(start_time - 8) * 2
        end_idx = -(end_time - 8) * 2
        if start_time % 1 != 0:
            start_idx -= 1
        if end_time % 1 != 0:
            end_idx -= 1
        ax.add_patch(patches.Rectangle((day_idx, start_idx), 1, end_idx - start_idx, edgecolor='black', facecolor='blue', alpha=0.5))
        plt.text(day_idx + 0.5, (start_idx + end_idx) / 2, subject, ha='center', va='center', color='white')

    plt.show()

# Define the event
event = ('Monday', 9.5, 10.333, 'CS241')

# Plot the schedule with the event
plot_schedule([event])