
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

#alpha1
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
process=0
# url = "https://search.azlyrics.com/search.php?q=eminem"
response = requests.get("https://search.azlyrics.com", timeout=10, headers=headers)

data11 = response.text
soup1 = BeautifulSoup(data11, 'lxml')
# print(soup1)
hh=soup1.find_all("a")
# print(hh)
wep=[]
tre=[]
for v1 in hh:
    wep.append(v1.get("href"))
# print(wep)
for c1 in wep:
    tre.append(c1.lstrip("//"))
# print(tre)

del tre[28:]
del tre[0]

for x1 in tre:
    print(x1)


if process == 0:

    # alpha2
    for alphabets in tre:

        alphabets="https://"+alphabets
        # url = "https://search.azlyrics.com/search.php?q=eminem"

        response1 = requests.get(alphabets, timeout=10, headers=headers)

        data22 = response1.text
        soup2 = BeautifulSoup(data22, 'lxml')

        ttf=soup2.find_all('div',{"class":"col-sm-6 text-center artist-col"})

        row1=ttf[0].text.split("\n")
        row2=ttf[1].text.split("\n")
        del row1[0],row1[-1]
        del row2[0:4],row2[-1]

        row3 = row1 + row2
        print(row3)
        print(len(row3))

        time.sleep(2)

        for artistname in row3:

            full_query = "https://search.azlyrics.com/search.php?q=" + artistname
            response4 = requests.get(full_query, timeout=10, headers=headers)

            data33 = response4.text
            soup3 = BeautifulSoup(data33, 'lxml')

            boldtag = soup3.find_all("b")

            boldtagstr = str(boldtag)

            boldtaglist = boldtagstr.split("<b>")

            if "Artist results:</b>, " in boldtaglist:

                # code logic main

                tt = soup3.find_all("table", {"class": "table table-condensed"})[0]

                # links of artist

                pp = tt.find_all('a')

                l22 = []
                for x2 in pp:
                    l22.append(x2.get('href'))

                l3 = []
                for y1 in l22:
                    if y1.endswith(".html"):
                        l3.append(y1)
                # print(l3)

                print(l3[0])  # i need this only..


                # link of artist++++++++++
                time.sleep(2)

                response2 = requests.get(l3[0], timeout=10, headers=headers)
                data44 = response2.text
                soup4 = BeautifulSoup(data44, 'lxml')

                tags1 = soup4.find_all("div", {"id": "listAlbum"})[0].text
                # print(tags1)
                kk = str(tags1)
                # print(kk)

                c2 = kk.count("{s:\"")
                pos11 = 0
                t2 = []

                while c2 > 0:
                    startpos1 = kk.find('{s:\"', pos11, len(kk))
                    endpos1 = kk.find('\",', startpos1, len(kk))
                    startpos1 = startpos1 + 4
                    mydata1 = kk[startpos1:endpos1]
                    pos11 = endpos1
                    c2 -= 1
                    t2.append(mydata1)
                # names of artist
                # print(t2+"by"+artistname)

                time.sleep(2)

                for getlyrics in t2:

                    query_str = getlyrics+" "+"by"+" "+artistname

                    url = "https://search.azlyrics.com/search.php?q=" + query_str

                    try:
                        response3 = requests.get(url, timeout=10, headers=headers)

                    except requests.ConnectionError as err:
                        print("<<<<<< PLEASE CHECK YOUR INTERNET CONNECTION >>>>")
                    except requests.Timeout as err:
                        print("OOPS!! Timeout Error")
                    except requests.RequestException as err:
                        print("OOPS!! UNEXPECTED Error")

                    else:

                        data55 = response3.text

                        soup5 = BeautifulSoup(data55, 'lxml')
                        # boldtag = soup5.find_all("td", {"class": "text-left visitedlyr"})

                        tags = soup5.find_all('a')

                        l2 = []
                        for x3 in tags:
                            l2.append(x3.get('href'))
                        song_url = []


                        for y2 in l2:
                            if "www.azlyrics.com/lyrics/" in y2:
                                song_url.append(y2)

                        print(song_url[0])   # take only first element


                        time.sleep(2)

                        req = requests.get(song_url[0], timeout=10, headers=headers)

                        soup6 = BeautifulSoup(req.content, "lxml")
                        mm = str(soup6)

                        c3 = mm.count("<div>")
                        pos = 0

                        while c3 > 0:
                            startpos = mm.find('<div>', pos, len(mm))
                            endpos = mm.find('</div>', startpos, len(mm))
                            startpos = startpos + 5
                            mydata = mm[startpos:endpos]
                            pos = endpos
                            c3 -= 1
                            print(mydata)

                        time.sleep(2)

                        conn = sqlite3.connect('rishabh.db')

                        c4 = conn.cursor()

                        # Create table
                        # c4.execute("DROP TABLE Lyrika")

                        c4.execute("""CREATE TABLE IF NOT EXISTS Lyrika(
                        SONG_NAME TEXT NOT NULL,
                        ARTIST_NAME TEXT NOT NULL,
                        LYRICS TEXT NOT NULL
                        )
                        """)

                        # Insert a row of data
                        # c4.execute("INSERT INTO Lyrika VALUES (?,?,?)",(song[0],),song[0],),song[0],),)

                        c4.execute(f'INSERT INTO Lyrika VALUES ("{getlyrics}","{artistname}","{mydata}")')

                        # Save (commit) the changes
                        conn.commit()

                        # We can also close the connection if we are done with it.
                        # Just be sure any changes have been committed or they will be lost.
                        conn.close()

    process += 1

else:
    print("All data FINISHED")