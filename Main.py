import os
from mutagen.mp3 import MP3
import heapq

audio_folders = ["Audios1", "Audios2", "Audios3"]

for folder in audio_folders:
    folder_path = os.path.join(os.getcwd(), folder)
    print(f"\n{folder}")

    for root, _, files in os.walk(folder_path):
        for file in files:
            mp3_file = os.path.join(root, file)
            audio = MP3(mp3_file)
            duration = audio.info.length
            print(f"{file}: {duration:.2f} seconds")

def savedurations(folder):
    file_durations = []
    folder_path = os.path.join(os.getcwd(), folder)

    for root, _, files in os.walk(folder_path):
        for file in files:
                mp3_file = os.path.join(root, file)
                audio = MP3(mp3_file)
                duration = round(audio.info.length, 2)
                file_durations.append((file, duration))
    return file_durations


def worstfitlinear(file_durations, folder_capacity=100):
    folders = []
    folder_metadata = []

    for file, duration in file_durations:
        maxsize = -999
        maxindex = -999

        for i, folder in enumerate(folders):
            remaining_space = folder_capacity - sum(duration for _, duration in folder)  # calculate the remaining space
            if remaining_space >= duration and remaining_space > maxsize:
                maxsize = remaining_space
                maxindex = i

        # If file fits into an existing folder, update its remaining space
        if maxindex != -999:
            folders[maxindex].append((file, duration))
        else:
            folders.append([(file, duration)])  # Create a new folder with the file

    print("\nFolders with Audio Files:")
    for i, folder in enumerate(folders, 1):
        print(f"Folder {i}:")
        total_duration = sum(duration for _, duration in folder)
        for file, duration in folder:
            print(f"  {file}: {duration}s")
        print(f"  Total Duration: {total_duration}s\8n")

    #metadata
    with open('worstfitlinear.txt', 'w') as f:
        for i, folder in enumerate(folders, 1):
            total_duration = sum(duration for _, duration in folder)
            f.write(f"Folder {i}:\n")
            for file, duration in folder:
                f.write(f"  {file}: {duration}s\n")
            f.write(f"  Total Duration: {total_duration}s\n\n")



def worstfitqueue(file_durations, folder_capacity=100):
    folders = []

    for file, duration in file_durations:
        if folders and -folders[0] >= duration:
            remaining = heapq.heappop(folders)
            newremaining = -remaining - duration
            heapq.heappush(folders, -newremaining)
        else:
            heapq.heappush(folders, -(folder_capacity - duration))

    newfolder = [folder_capacity - (-capacity) for capacity in folders]
    print("\nWorst fit (Priority Queue):")
    for i, elfolder in enumerate(newfolder, 1):
        print(f"Folder {i}: {elfolder}s")

    metadata_file_path = 'worstfitqueue.txt'
    with open(metadata_file_path, 'w') as f:
        for i, folder in enumerate(newfolder, 1):
            f.write(f"Folder {i}: {folder}s\n")

def first_fit (file_durations, folder_capacity=100):
    folders = [] #initiate a list of folders to store files
    file_durations.sort(key=lambda x: x[1], reverse = True) #sort the files in descending order
    for file, duration in file_durations :#for loop that lookds through FOLDERS
        placed = False #not placed yet
        for folder in folders: #for loop that looks through FILES
            remaining_space = folder_capacity - sum(d for _, d in folder) #calculate the remaining space for the folder on this iteration
            if remaining_space >= duration: #if there's space in the folder & it fits the file
                folder.append((file, duration)) #adding file to folder
                placed = True #turn placed flag to true
                break
        if not placed:
            folders.append([(file, duration)]) #create a new folder

    print("\nFirst Fit Decreasing Algorithm:")
    for i, folder in enumerate(folders, 1):
        total_duration = sum(duration for _, duration in folder)
        print(f"Folder {i}:")
        for file, duration in folder:
            print(f"  {file}: {duration}s")
        print(f"  Total Duration: {total_duration}s\n")

    # Save metadata to a file
    metadata_file_path = 'firstfitdecreasing.txt'
    with open(metadata_file_path, 'w') as f:
        for i, folder in enumerate(folders, 1):
            total_duration = sum(duration for _, duration in folder)
            f.write(f"Folder {i}:\n")
            for file, duration in folder:
                f.write(f"  {file}: {duration}s\n")
            f.write(f"  Total Duration: {total_duration}s\n\n")


def folder_filling (file_durations, folder_capacity = 100):

    remaining_files = file_durations[:]  # Copy of the file durations
    folders = []  # List to store folders

    while remaining_files:
        current_folder = []
        current_capacity = folder_capacity

        for file, duration in remaining_files[:]:  # Iterate through remaining files
            if duration <= current_capacity:
                current_folder.append((file, duration))  # Add file to the current folder
                current_capacity -= duration  # Update remaining capacity
                remaining_files.remove((file, duration))  # Remove the file from remaining files

        folders.append(current_folder)  # Add the filled folder to the list

    print("\nFolder Filling Algorithm (Greedy):")
    for i, folder in enumerate(folders, 1):
        total_duration = sum(duration for _, duration in folder)
        print(f"Folder {i}:")
        for file, duration in folder:
            print(f"  {file}: {duration}s")
        print(f"  Total Duration: {total_duration}s\n")

    # Save metadata to a file
    metadata_file_path = 'folderfilling_greedy.txt'
    with open(metadata_file_path, 'w') as f:
        for i, folder in enumerate(folders, 1):
            total_duration = sum(duration for _, duration in folder)
            f.write(f"Folder {i}:\n")
            for file, duration in folder:
                f.write(f"  {file}: {duration}s\n")
            f.write(f"  Total Duration: {total_duration}s\n\n")


#mn awl hena el main
def main():
    print("Hello world!")

    while True:
        print("\nCurrent folders:")
        for i, folder in enumerate(audio_folders, 1):
            print(f"{i}. {folder}")

        folder_choice = int(input("Enter a number to choose a folder: "))
        chosen_folder = audio_folders[folder_choice - 1]
        print(f"\nYou selected: {chosen_folder}")

        file_durations = savedurations(chosen_folder)

        while True:
            print("\nChoose an Algorithm to run:")
            print("1. Worst fit linear search")
            print("2. Worst fit priority queue")
            print("3. First fit")
            print("4. Folder Filling")
            choice = int(input("Enter your choice: "))
            folder_capacity = 100

            if choice == 1:
                worstfitlinear(file_durations, folder_capacity)
            elif choice == 2:
                worstfitqueue(file_durations, folder_capacity)
            elif choice == 3:
                first_fit(file_durations, folder_capacity)
            elif choice == 4:
                folder_filling(file_durations, folder_capacity)


            another_algo = input("\nDo you want to use another algorithm? (yes/no): ").lower()
            if another_algo != "yes":
                break

        try_another_folder = input("\nDo you want to try another folder? (yes/no): ").lower()
        if try_another_folder != "yes":
            break

    print("Goodbye!")


main()

#Apply oop: put into classes and configure the main
#Output The Result Into Folders
#Optional: Exception Handling, Bonus Best-Fit