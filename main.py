from participant import TrialParticipant #imports just TrailParticipant as TrailParticipant inherites from both FlankerFileReader and FileReader

flanker_participant = TrialParticipant("rounds.txt") #initializes the class to flanker_participant, passes in first and last name
run_expr = True # runs with Flanker Task while True
completedTask = True # checks if the user completed the task or withdrew consent
restartChoice = True # restarts the Flanker Task until it becomes False
consentGiven = False # checks if user offered or withheld consent
wordChange = False # checks if user decides to change word stimulus
messageNotPrinted = True # checks if message informing user of their streak has yet to be printed

while restartChoice: #while loop that breaks if the user doesn't want ot restart the task, supporting reusability by making it so that the user does not have to re run to progam to complete the task again

    print("Welcome to the Flanker Task! Please input your first and last name.")
    fname = input("First name: ")
    lname = input("Last name: ")
    flanker_participant.set_name(fname, lname) # calls the class
    print(flanker_participant)
       
    print("Welcome", flanker_participant.get_name()+". This task is used to measure your selective attention and ability to inhibit irrelevant information.")
    print("You will be presented with a five letter string, e.g. vvxvv. Your objective is to identify the middle letter.")
    print("If the middle letter is 'x' or 'c', press 'a'.")
    print("If the middle letter is 'b' or 'v', press 'l'.")
    print("If you choose to undertake this task, your full name and the score your amount of correct and incorrect answers will be recorded.")
    while not consentGiven:
        consent = input("If you consent to continue with the experiment, please press 'y'. If you do not consent, please press 'n': ") #using while loop, gives the participant the option to either continue with the task, or withdraw the consent and terminate the task
        if consent.lower() == "y": 
            print("Thank you for choosing to participate! :)")
            start = input("Press enter to start the task: ")
            print("\n"*20)
            consentGiven = True #breaks loop
    
        elif consent.lower() == "n":
            print("Flanker Task terminated.")
            completedTask = False #shows participant didn't complete the task
            restartChoice = False #no option for restart as they never started
            run_expr = False #doesn't run the Flanker Task
            consentGiven = True #breaks loop
    
        else:
            print("Inavlid input. Please press 'y' to consent or 'n' to decline consent.") #doesn't break loop

    while run_expr: #runs until it runs out of rounds
        print("\n"*10)
        if messageNotPrinted == True: #so message is only printed once
            if flanker_participant.correct_amount_message_threshold() == True: #checks if correct guesses has met the threshold
                continue_game = input("YOU'RE ON FIRE. Time to spice things up.... Press enter to continue.")
                print("\n"*10)
                messageNotPrinted = False
        flanker_participant.choose_key() #chooses current key
        print(flanker_participant.print_location() + flanker_participant.get_word()) #prints the five letter word with the spaces from print location
        flanker_participant.check_selection(input()) #checks if input from the user matches the current key
        wordPos = flanker_participant.increment_wordpos() #increments the word position
        if wordPos == False: # checks if wordPos is False (greater than or equal to 6)
            flanker_participant.reset_wordpos() #resets word position
            if flanker_participant.get_round_num() == flanker_participant.get_half_of_rounds(): #checks if participant is halfway through the task
                while not wordChange:
                    word_change_choice = input("You are halfway through the task. Would you like to change the word stimulus? Please press 'y' to accept and 'n' to decline: ")
                    if word_change_choice.lower() == "y":
                        print("Words have been changed.")
                        flanker_participant.second_dict()
                        wordChange = True
                    elif word_change_choice.lower() == "n":
                        print("Words have not been changed.")
                        wordChange = True
                    else:
                        print("Inavlid input. Please press 'y' to accept or 'n' to decline the word change.")
                
            roundPos = flanker_participant.increment_round() #increments the round number
            #if roundPos == True: # if round number is True (less than or equal to amount of rounds), print message to acknowledge completion of round
                #roundBreak = input("You have completed a full round. Please press enter to start the next round when ready.") #takes input in order to move onto the next round
            if roundPos == False: #if round number is False (greater than 10), make run_expr equal to false, ending the flanker task
                run_expr = False

    if completedTask == True: # runs if the flanker task has been completed        
        print("\n"*5)
        print("Thank you for participating in the experiment!")
        print("Task has been completed.")
        print("All correct selections: ", flanker_participant.get_correct()) # presents amount of correct guesses
        print("All incorrect selections: ", flanker_participant.get_incorrect()) # presents amount of incorrect guesses
        flanker_participant.log_name_with_score() #logs participant name with score into the instance variable dictionary
        flanker_participant.log_participant() # logs participant number and and instance variable dictionary into the class variable dictionary
        print("Particpant logged: ", flanker_participant.get_particpant_log()) #prints participant log
        
        restart = input("If you would like to restart the task, please press enter. If not, please press 'n': ") #receives input from user
           
        if restart.lower() == "n":
            restartChoice = False #sets restartChoice to False to stop the while loop, terminating the program
            print("Flanker Task terminated.")
            
        else:
            flanker_participant.reset_rounds() #resets the round number
            flanker_participant.reset_wordpos() #resets the word position
            flanker_participant.reset_correct() #resets correct guesses
            flanker_participant.reset_incorrect() #resets incorrect guesses
            flanker_participant.reset_participant_dict() #recets participant dict
            flanker_participant.first_dict() #sets first dict as current dict
            flanker_participant.increment_participant_instances() #increments the participant instances
            run_expr = True # changes run_expr to True so the Flanker Task can run again
            consentGiven = False # re-initializes consent to False so the user is asked for consent again upon restarting
            wordChange = False # 
            messageNotPrinted = True # 
            print("\n"*20)
            