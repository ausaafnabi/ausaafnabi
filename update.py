import mechanize
from bs4 import BeautifulSoup
import requests

username = "ausaafnabi" 
resUrl = "https://api.github.com/users/"+ username +"/repos?sort=updated"
gifUrl = "http://wigflip.com/signbot"

def getCurrentWorkingRepo(resUrl):
    try:
        response = requests.get(resUrl)
        repo = response.json()
        reponame = repo[0]['name']        
        if reponame == username:
            reponame = repo[1]['name']
        print("[ Fetched Repo Name : " +str(reponame)+ " ]")
    except HTTPError:
        print("Error while fetching the repository")

    return reponame


# Section to scrape the gif 

def _requestGif(gifUrl,message):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open(gifUrl)
    br.select_form(nr=0)
    br['T'] = message
    br['S'] = ['L',]
    response = br.submit()
    print("[ Successfully Sent response..... ]")
    return response

def fetchGif(gifUrl,sourceLoc,message):
    page = _requestGif(gifUrl,message).read()

    soup = BeautifulSoup(page,'html.parser')
    result = soup.find(id='output')

    img_elem = result.findAll('img')
    for img in img_elem:
        gifLink = img['src']
        print("[ Image Source : " + img['src'] + " ]")
    # Downloading the image......
    #

    readmeGif = requests.get(gifLink)

    with open(sourceLoc,"wb") as file:
        file.write(readmeGif.content)
        print("[ Gif Sucessfully Overwritten......... ]")



def main():
    username = "ausaafnabi" 
    resUrl = "https://api.github.com/users/"+ username +"/repos?sort=updated"
    gifUrl = "http://wigflip.com/signbot"
    print(resUrl)

    sourceLoc = "Assets/signbot.gif"

    #message to be configured using github api
    message  = " Last worked on : " + getCurrentWorkingRepo(resUrl) 
    print(message)
    fetchGif(gifUrl,sourceLoc,message)
    
if __name__ == "__main__":
    main()
