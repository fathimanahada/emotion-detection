import time

# set the starting time of the session
start_time = time.time()

# set the active time of the session in seconds
active_time = 60  # session will be active for 60 seconds

# loop until the session is expired
while time.time() < start_time + active_time:
    # perform your session tasks here
    # for example, check if the user is recognized
    if user_recognized():
        # continue with the session
        print("User recognized, continuing session...")
    else:
        # end the session if user is not recognized
        print("User not recognized, ending session...")
        break
    
    # sleep for a short time to reduce CPU usage
    time.sleep(0.1)

# session is expired
print("Session expired.")

emp,c_time,exp_time = faces,current_time,exp_time