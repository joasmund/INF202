import os

""" file_list = []
file_names = str(file_list)

for file in file_list():

os.mkdir(file_names)


output = "src/results/"

if not os.path.exists(output):
    os.mkdir(output)
else:
    pass

results_folder = os.mkdir
 """

def create_subfolder_from_file(file_path):

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    

    subfolder_path = os.path.join(os.getcwd(), file_name)
    
    try:

        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path)
            print(f"Subfolder '{file_name}' created at: {subfolder_path}")
        else:
            print(f"Subfolder '{file_name}' already exists.")
    except Exception as e:
        print(f"Error creating subfolder: {e}")


file_path = "results/example_file.txt" 
create_subfolder_from_file(file_path)


for file in file_list:

    create_subfolder_from_file(file)
    print(file)