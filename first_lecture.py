import pytube

link = input("Paste the link")
ddd = pytube.YouTube(link)
ddd.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
print('Video has been downloaded', link)