Ryuanime_Downloader
========
Quick and dirty script to download Anime from ryuanime.com . This script can download entire series or range of episodes.
I haven't tested it properly. Try at your own risk. This script depends on the [aria2c](https://github.com/aria2/aria2).
Make sure to install all the dependencies before running the script.


Installation
============
* `git clone https://github.com/SagiSatish/Ryuanime_Downloader.git`
* `pip install -r requirements.txt`

Usage
=====
```
usage: python RYUAnime_Downloader.py [-h] -u URL -t {dub,sub} -o OUTPUT [-s START]
                              [-e END]

Ryuanime Downloader

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -u URL, --url URL     URL to download
  -t {dub,sub}, --type {dub,sub}
                        Download type: dub or sub
  -o OUTPUT, --output OUTPUT
                        Output folder

Optional arguments:
  -s START, --start START
                        Starting episode number
  -e END, --end END     Ending episode number
```
Example
=====
`python RYUAnime_Downloader.py -u http://www.ryuanime.com/series-info/one-piece -t sub -o /root/Desktop -s 1 -e 4
`

Disclaimer
=====
Downloading copyrighted material may be illegal in your country. Use at your own risk. 
This script is just download the content from the web and are believed to be in the "**Public Domain**". 
I neither promotes the illegal content nor affiliated with the ryuanime in any manner.

