import ffmpeg #not sure whats it called but you get what im doing here
import time


#TODO:
#Resolve link function, i.e. take the query from discord "$play 'my favorite song'" get the link for that query
#Stream function i.e. stream the source returned from ^
#Pause...?
#Store queue -> probably better to make a class for streaming/management



def getTimeMilis(): 
    return time.time() * 1000
