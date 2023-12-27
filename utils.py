import ffmpeg, time, requests, youtube_dl 

#TODO:
#Resolve link function, i.e. take the query from discord "$play 'my favorite song'" get the link for that query
#Stream function i.e. stream the source returned from ^
#Pause...?
#Store song queue -> probably better to make a class for streaming/management


def getTimeMilis(): 
    return time.time() * 1000

def stream(infile, song):
    infile = resolveLink(song)
    out, err = (ffmpeg
    .input(infile)
    .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
    .overwrite_output()
    .run(capture_stdout=True)
    )
    return out, err

def resolveLink(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'pcm_s16le',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        url = info_dict['url']
    
    return url

class Queue: 
    name = ""
    q = []

    #create constructor?

    def add(song):
        
        pass

