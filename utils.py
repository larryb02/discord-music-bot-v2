import ffmpeg, time, yt_dlp

#TODO:
# >:)


def getTimeMilis(): #seems uneccessary now
    return time.time() * 1000

def stream(song):
    infile = song #just pass the wp_url from resolveLink()
    out, err = (ffmpeg
    .input(infile)
    .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
    .overwrite_output()
    .run(capture_stdout=True)
    )
    return out, err

def resolveLink(query: str): 
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'pcm_s16le',
            'preferredquality': '192',
        }],
        'verbose': True
    }
    #need to append ytsearch to strings
    formattedQuery = f"ytsearch:{query}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(formattedQuery, download=False)
    print(f"Webpage URL: {results['entries'][0]['webpage_url']}\n")
    #parts that i may want:
    title = results['entries'][0]['title']
    extractedUrl = results['entries'][0]['webpage_url']
    returnedUrl = results['entries'][0]['url']
    info = {
        'title': title,
        'extractedUrl': extractedUrl,
        'returnedUrl': returnedUrl
    }
    return info
    

if __name__ == "__main__":
    song = "BBL Drizzy"
    resolveLink(song)