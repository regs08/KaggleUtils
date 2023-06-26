import os

def replace_first_element_in_folder(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file in the folder
    for file_name in files:
        # Check if the file is a text file
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            # Read the contents of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the lines by replacing the first element with 0
            modified_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) > 0:
                    elements[0] = '0'
                modified_line = ' '.join(elements) + '\n'
                modified_lines.append(modified_line)

            # Save the changes back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)

            print(f"Modified and saved changes to '{file_path}' successfully!")

    print("Modification of all files in the folder is complete.")


folder ="/Users/cole/Desktop/Chardonnay/labels"
replace_first_element_in_folder(folder)

