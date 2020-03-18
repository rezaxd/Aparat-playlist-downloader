import requests as req 
import inquirer as inq
from clint.textui import progress
from bs4 import BeautifulSoup as bs4

BASE_URL = 'https://www.aparat.com'

def videoDetail(videoUrl):
    try:
        itemPage = bs4(req.get(videoUrl).text, 'html.parser')
    except expression as e:
        # print(e)
        print('=====> request failed/ check network connection!')
    choices = [i['aria-label'].split(' ')[-1] for i in itemPage.select('.menu-list .link a')]
    downloadLinks = {}
    for itemLink in itemPage.select('.menu-list .link a'):
        downloadLinks[itemLink['aria-label'].split(' ')[-1]] = itemLink['href']
    questions = [
    inq.List('quality',
                message="\U0001F914  Select quality",
                choices=choices,
            ),
    ]
    answer = inq.prompt(questions)
    itemPageDownloadLink = downloadLinks[answer['quality']]
    itemTitle = f"{itemPage.select('#videoTitle')[0].text}-{answer['quality']}"
    return itemTitle, itemPageDownloadLink

def videoDownloader(title, url):
    try:
        videoDownload = req.get(url, stream=True)
    except expression as identifier:
        # print(e)
        print('=====> request failed/ check network connection!')
        print('=====> Download failed!')
    path = './%s.mp4'%title
    print('[*] \U0001F4E9  Downloading...')
    with open(path, 'wb') as f:
        total_length = int(videoDownload.headers.get('content-length'))
        for chunk in progress.bar(videoDownload.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
    print('[*] %s Downloaded!'%title)


def main(url):
    try:
        requestToGetPlayListPage = req.get(url)
    except expression as e:
        # print(e)
        print('=====> request failed/ check network connection!')
    playlist = bs4(requestToGetPlayListPage.text, 'html.parser')
    playListItems = playlist.select('.playlist-body div div div .thumb-title a')
    counter = 1
    for item in playListItems:
        itemUrl = BASE_URL + item['href']
        title, url = videoDetail(itemUrl)
        print(f"[*] {counter}/{len(playListItems)} - title: {title}")
        videoDownloader(title, url)
        counter += 1

if __name__ == "__main__":
    questions = [
        inq.Text('url', message="What's your playlist url [example: 'https://www.aparat.com/v/fAZSV']",)
    ]
    playListUrl = inq.prompt(questions)['url']
    # playListUrl = 'https://www.aparat.com/v/fAZSV' # Its jadi's last playlist at 18 march 2020 :D
    main(playListUrl)
