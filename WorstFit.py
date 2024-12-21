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
        print(f"  Total Duration: {total_duration}s\n")

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

            choice = int(input("Enter your choice (1 or 2): "))
            folder_capacity = 100

            if choice == 1:
                worstfitlinear(file_durations, folder_capacity)
            elif choice == 2:
                worstfitqueue(file_durations, folder_capacity)

            another_algo = input("\nDo you want to use another algorithm? (yes/no): ").lower()
            if another_algo != "yes":
                break

        try_another_folder = input("\nDo you want to try another folder? (yes/no): ").lower()
        if try_another_folder != "yes":
            break

    print("Goodbye!")


main()
