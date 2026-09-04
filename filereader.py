import random

class FileReader:

    def __init__(self, filename):
        self.__filename = None
        self.set_filename(filename)
        print("instance of FileReader class created!")
    
    def read_all(self):
        try:
            file_1 = open(self.__filename)
            lines = file_1.readlines()
            file_1.close()
            return lines
        except:
            print("file not opened. Terminating method")
            return False
        
    def read_all_reversed(self):
        try:
            file_1 = open(self.__filename).read()
            file_1_rev = file_1[::-1]
            lines = file_1_rev.split("\n")
            lines.pop(0)
            return lines 
        except:
            print("file not opened. Terminating method")
            return False

    def line_count(self):
        lines = self.read_all()
        line_amount = len(lines)
        return line_amount
    
    def line_count_reversed(self):
        lines = self.read_all_reversed()
        line_amount = len(lines)
        return line_amount

    def get_filename(self):
        return self.__filename

    def set_filename(self, new_filename):
        if type(new_filename) == str:
            self.__filename = new_filename 



class FlankerFileReader(FileReader):
    
    def __str__(self):
        desc = "Filename: %s. This class converts rounds from a file into an embedded dictionary, usable for the Flanker Task." %(self.get_filename())
        return desc
    
    #def __init__(self, filename):
        #super().__init__(filename)
        #self.current_dict = ""

    #Converts the raw text lines into a dictionary of rounds.
    def create_dict(self, lines):
        rounds_dict = {}
        for i in range(0, len(lines), 2): #since each round takes up 2 lines in the text file, loop through list in steps of 2
            line_a = lines[i].strip().split(",") #remove whitespace with strip, split into a list at each comma
            line_l = lines[i+1].strip().split(",") #does the same but index i+1 to get line_l

            round_number = int(line_a[0]) #gets the round number which is at first position in the line_a list, converts it to integer
            words_a = line_a[2:]   #skip first two values to just get the words
            words_l = line_l[2:] 

            #Embeds the dictionary with the words for rounds "a" and "l" into the rounds_dict dictionary, with the key of the round number
            rounds_dict[round_number] = {line_a[1]: words_a, line_l[1]: words_l} 
        return rounds_dict

    def create_dict_reversed(self, lines):
        rounds_dict = {}
        rounds_count = 1      
        for i in range(0, len(lines), 2): #since each round takes up 2 lines in the text file, loop through list in steps of 2
            line_l = lines[i].split(",") #remove whitespace with strip, split into a list at each comma
            line_a = lines[i+1].split(",") #does the same but index i+1 to get line_l

            round_number = rounds_count #gets the round number which is at first position in the line_a list, converts it to integer
            words_l = line_a[:6]   #skip first two values to just get the words
            words_a = line_l[:6]
            rounds_count+=1

            #Embeds the dictionary with the words for rounds "a" and "l" into the rounds_dict dictionary, with the key of the round number
            rounds_dict[round_number] = {line_a[6]: words_a, line_l[6]: words_l} 
        return rounds_dict
    
    def first_dict(self): #sets current dict as first dict/orginal dict
        self.current_dict = self.all_rounds()
        return self.current_dict

    def second_dict(self): #sets current dict as second dict/reversed dict
        self.current_dict =  self.all_rounds_reversed()
        return self.current_dict
    
    def get_current_dict(self): #returns current dict
        return self.current_dict
    
    #Calls the create_dict method, returns all rounds in dictionary form
    def all_rounds(self):
        lines = self.read_all()           
        return self.create_dict(lines) #passes in the lines from the file from read_all to create_dict
    
    def all_rounds_reversed(self):
        lines = self.read_all_reversed()           
        return self.create_dict_reversed(lines)


    #Only returns the rounds listed in round_num_list, re-names the rounds starting at round 1
    def get_rounds_at(self, round_num_list):
        all_data = self.get_current_dict()
        selected = {}
        new_round_number = 1 #starts at round 1

        for original_round in round_num_list:
            selected[new_round_number] = all_data[original_round] #adds round to 'selected' dictionary with the index of new_round_number
            new_round_number += 1 #increases new round number

        return selected


    #Returns all the rounds between the start and end value
    def get_round_range(self, round_range):
        all_data = self.get_current_dict()

        #Check if range is in correct format
        if (len(round_range) != 2 or round_range[0] <= 0 or round_range[1] > len(all_data) or round_range[0] > round_range[1]):
            raise ValueError("Invalid round range format.")

        start, end = round_range
        selected = {}
        new_round_number = 1

        #Loops through the range, adding the rounds within it into the dictionary
        for i in range(start, end + 1):
            selected[new_round_number] = all_data[i]
            new_round_number += 1

        return selected


    #Randomizes the order of rounds in the given dictionary and adds it to a new one
    def random_rounds(self):
        all_data = self.get_current_dict()
        total_rounds = len(all_data)
        selected = {}
        new_round_number = 1




    #Selects a random range of rounds from the round file
    def random_round_range(self):
        all_data = self.get_current_dict()
        total_rounds = len(all_data)

        #Chooses random start and end values
        start = random.randint(1, total_rounds)
        stop = random.randint(start, total_rounds)

        selected = {}
        new_round_number = 1

        for i in range(start, stop + 1):
            selected[new_round_number] = all_data[i]
            new_round_number += 1

        return selected


    #Returns all rounds except the ones listed
    def exclude_rounds_at(self, round_num_list):
        all_data = self.all_rounds()

        selected = {}
        new_round_number = 1

        for i in all_data:
            if i not in round_num_list: #only include rounds not passed in in round_num_list
                selected[new_round_number] = all_data[i]
                new_round_number += 1

        return selected


    #Returns all rounds except the rounds in the given range
    def exclude_round_range(self, round_range):
        all_data = self.get_current_dict()

        #Check if range is in correct format
        if (len(round_range) != 2 or round_range[0] <= 0 or round_range[1] > len(all_data) or round_range[0] > round_range[1]):
            raise ValueError("Invalid round range format.")

        start, end = round_range

        selected = {}
        new_round_number = 1

        #Only include the rounds not in the range
        for i in all_data:
            if not (start <= i <= end):
                selected[new_round_number] = all_data[i]
                new_round_number += 1

        return selected
