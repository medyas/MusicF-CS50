import youtube_dl

def parse(v_id, v_title):

    title = v_title.replace(' ', '-') +'.mp3'
    #title = title.replace('&', '-')
    
    class MyLogger(object):
        def debug(self, msg):
            pass
    
        def warning(self, msg):
            pass
    
        def error(self, msg):
            print(msg)
    
    
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    
    
    ydl_opts = {
        'format': 'bestaudio/best', 
        'extractaudio' : True,      
        'audioformat' : 'mp3',      
        'outtmpl': 'static/uploads/'+title,       
        'noplaylist' : True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v='+v_id])
    
    return title