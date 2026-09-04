'''
References:
http://sixthresearcher.com/wp-content/uploads/2016/12/Python3_reference_cheat_sheet.pdf
https://stackoverflow.com/questions/10399614/accessing-value-inside-nested-dictionaries
https://stackoverflow.com/questions/35282222/in-python-how-do-i-cast-a-class-object-to-a-dict
https://stackabuse.com/bytes/handling-yes-no-user-input-in-python/
https://www.w3schools.com/python/trypython.asp?filename=demo_ref_random_choice2

'''
import random # importing random for later use

from filereader import FlankerFileReader
#file_1 = FlankerFileReader("rounds.txt")

class TrialParticipant(FlankerFileReader): # capitalized class name as per standard

    instances_of_participants = 0 # integer class variable used to store the number of participants
    logged_participants = {} # dictionary class variable used log multiple participants' info, supporting reusability
    
    def __init__(self, filename): # initializing the class, adding in positional arguement of filename from FlankerFileReader
        super().__init__(filename) # inheriting the methods and properties from FlankerFileReader
        self.first_dict() #sets current dict as first dict
        TrialParticipant.instances_of_participants += 1 #incrementing the instances of participants each time the class is ran
        self.participant_num = TrialParticipant.instances_of_participants # setting the particpant num to the current participant instance num
        self.logged_name_with_score = {} # creating an instance variable dictionary that will be embedded into the global dictionary in order to log each participant's data
        self.round = 1 
        self.current_key = "a"
        self.word_pos = 0
        self.correct = 0
        self.incorrect = 0

    def __str__(self): # string representation
        desc = "Flanker Task. Participant name: %s %s, participant number: %s." %(self.first_name,self.last_name, self.participant_num)
        return desc
    
    def log_name_with_score(self): #stores participant's amount of correct guesses to the key of their full name, in the instance variable dictionary
        self.logged_name_with_score[self.first_name + ' ' + self.last_name] = self.correct
        
    def increment_participant_instances(self):
        TrialParticipant.instances_of_participants += 1 #incrementing the instances of participants each time the class is ran
        self.participant_num = TrialParticipant.instances_of_participants # setting the particpant num to the current participant instance num
        return self.participant_num
        
    def get_name(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name
    
    def set_name(self, fname_in, lname_in):
        self.first_name = fname_in
        self.last_name = lname_in
        return self.first_name, self.last_name
    
    def log_participant(self): #stores the participant's number to the key of the instance variable dictionary storing their name and amount of correct guesses, embedding it within the class variable dictionary
        self.logged_participants[self.participant_num] = self.logged_name_with_score
        
    def get_particpant_log(self): #getter that returns the particpant log dictionary
        return self.logged_participants
    
    def increment_round(self): 
        self.round = self.round + 1 #increments the round number
        if self.round > (len(self.current_dict)): #if loop, returning False if the round number is greater than the amount of rounds (10), True if it is less than or equal the amount of rounds (10)
            return False
        return True
    
    def get_round_num(self):
        return self.round

    def get_half_of_rounds(self): #gets half of rounds
        halfway = len(self.current_dict) - len(self.current_dict)/2
        return halfway    
        
    def increment_wordpos(self): #increments the word position (position in the list within the embedded stimuli dictionary class varaible)
        self.word_pos += 1 #if loop, returning False if the word position is greater or equal the amount of words per round (6), True if it is less than the amount of words per round (6)
        if self.word_pos >= len(self.current_dict[self.round][self.current_key]):  
            return False
        return True

    def choose_key(self): #uses random to randomly select between "a" and "l" each time it is called, sets the result as the new current key
        self.current_key = random.choice(["a","l"])
        return self.current_key
    
    def get_key(self):
        return self.current_dict[self.round][self.current_key]
    
    def check_selection(self, selection):
        if selection.lower() == self.current_key: #checks if selection input from the user is the same as the current key, .lower() automatically makes the input lowercase to remove case sensitivity
            self.increment_correct() #calls the inrement_correct function if the two letters match
        else:
            self.increment_incorrect() #calls the increment_incorrect function if they letters don't match
        
    def increment_correct(self): #increments to self.correct
        self.correct += 1
        return self.correct

    def increment_incorrect(self): #increments to self.incorrect
        self.incorrect += 1
        return self.incorrect
    
    def correct_amount_game_threshold(self):
        if self.correct >= self.get_all_words()//4: # if greater than or equal to threshold of all the words in the dcitionary divided by 4, return True
            return True
        else:
            return False
    
    def correct_amount_message_threshold(self):
        if self.correct == self.get_all_words()//4: # if correct amount is exactly the threshold, return True
            return True
        else:
            return False
        
    def print_location(self):
        no_space = "" #no space
        space = " " #one space
        space_amount = random.randint(1, 100)
        if self.correct_amount_game_threshold() == True:
            self.print_spaces = space * space_amount # if threshold met start printing in random locations
        else:
            self.print_spaces = no_space #default position if threshold has yet to be met
        return self.print_spaces

    def reset_wordpos(self): #sets the word position to 0
        self.word_pos = 0
        
    def reset_rounds(self): #sets the round number to 1
        self.round = 1
    
    def get_round(self): #getter that returns the information (embedded dictionary of "a" and "l" and all the words associated with them) that is associated with the key of round number in the stimuli dictionary
        return self.current_dict[self.round]
    
    def get_word(self): #getter that returns the information (word) that is associated with the key of the word position, which is information that is associated with the current key (either "a" or "l") in the stimuli dictionary
        return self.current_dict[self.round][self.current_key][self.word_pos]
    
    def get_correct(self): #getter that returns the amount of correct answers
        return self.correct
    
    def get_incorrect(self): #getter that returns the amount of incorrect answers
        return self.incorrect
    
    def reset_correct(self): #sets correct answers to 0
        self.correct = 0
        return self.correct
    
    def reset_incorrect(self): #sets incorrect answers to 0
        self.incorrect = 0
        return self.incorrect
    
    def reset_participant_dict(self): #resets participant dic
        self.logged_name_with_score = {}
        return self.logged_name_with_score
    
    def get_all_words(self): #gets the amount of words in the entire dictionary by multiplying the amount of rounds by the amount of words per round
        word_amount = self.get_round_count() * self.get_word_count()
        return word_amount
    
    def get_word_count(self): #getter that returns the amount of words in a within the embedded dictionary in the stimuli dictionary
        return len(self.current_dict[self.round][self.current_key]) #fosters reusability as the word amount in the stimuli can be altered, and the code will still work
    
    def get_round_count(self): #getter that returns the amount of rounds in the stimuli dictionary
        return len(self.current_dict) #fosters reusability as the amount of rounds in the stimuli can be altered, and the code will still work

