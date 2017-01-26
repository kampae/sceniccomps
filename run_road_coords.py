
def run_road_coords():
    
    keys = ['AIzaSyBEQ0xXnvLUr_tA3qSvk62XKjsLtpZKLyw', 'AIzaSyB1eAbxLePfsBKeszxFtc3g4wRNwnWwuzA', 'AIzaSyCS4cJEpYt-1u6xRkJmqsiBKV1LHnYB0Mg', 'AIzaSyARnHNVEx6TYAc0m9eRxuH0sLPy_pzpAac', 'AIzaSyAns9sLJaIPkyKwcDxWiOCwAgOVCmvn7yw', 'AIzaSyBRamX0tFH2PitoYtFJQpzePC66a4Ijs4g', 'AIzaSyB6hGD2MtGOmQ8oo2dXta6SU8aZWL4-s24']
    
    for i in range(0, len(keys)):
        file_num = 105600 + i*2400
        read_file = 'outputFileNum' + str(file_num)
        write_file = 'roadFile' + str(file_num)
        
        print("read_file: ", read_file)
        print("write_file: ", write_file)
        
run_road_coords()
    
    
    