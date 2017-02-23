def combine_files():
    
    combined_file = open("subset.csv", "w")
    combined_file_string = ""
    
    for i in range(1,11):
        f_name = "classified_points" + str((i*2400)) +".csv"
        f = open(f_name, "r")
        print(f_name)
        file_string = ""
        for line in f:
            file_string += line
        
        combined_file_string += file_string
        f.close()
        
    combined_file.write(combined_file_string)
    combined_file.close()
        

        
combine_files()