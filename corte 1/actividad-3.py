import requests
import threading
import psycopg2
from pytube import YouTube

#this function connects the database
def connect_db():
    conn = psycopg2.connect(dbname="concurrentTest", user="postgres", password="aam23082002") 
    return conn

#declaring an array 
videos=['https://youtu.be/FqC2lO3Yy_4','https://youtu.be/d6gBu2Zd7Bc','https://youtu.be/mKHK55eALtM','https://www.youtube.com/watch?v=xFxMx7DsqP0','https://www.youtube.com/watch?v=xmPtVflvLh0']

#this function gets an API
def get_api():
    url = requests.get('https://randomuser.me/api/')
    if url.status_code == 200:
        result = url.json().get('results')
        title = result[0].get('name').get('title')
        return title
    else:
        return 'error data not obtained from url'


#This function inserts data into my database
def insert_in_db(conn,dato):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO photos (title) VALUES ('"+dato+"')")
        print (f'Thread DB: ({dato})')
    except Exception as err:
        print(err)
    else:
        conn.commit()

#this function download_video
def download_video(dato,link):
    print(f'Downloading video({dato+1})')
    yt = YouTube(link)
    yt.streams.first().download()
    print(f'Download ({dato+1}) complete')

#ITERATES FUNCTIONS 
#this function iterates video 
def iterate_videos():
    print('iterating videos')
    print('Downloading videos...')
    for x in range (0,5):
        th1 = threading.Thread(target=download_video, args=[x,videos[x]]) 
        th1.start()
    print('Done')

#this function iterates data
def iterate_database(db):
    print('iterating database')
    for x in range (0,2000):
        dato=get_api()
        insert_in_db(db, dato)
    print('Thread done')

#this function iterates API
def iterate_api():
    print('iterating API')
    for x in range (0,50):
        print ('Thread API: Data obtained from API',get_api())
    print('Thread api done')

#THIS IS THE MAIN FUNCTION
def main():
    db = connect_db()
    th_videos= threading.Thread(target=iterate_videos())
    th_videos.start() 
    th_db= threading.Thread(target=iterate_database,args=[db])
    th_db.start()
    th_api = threading.Thread(target=iterate_api)
    th_api.start()

if __name__ == '__main__':
    main()