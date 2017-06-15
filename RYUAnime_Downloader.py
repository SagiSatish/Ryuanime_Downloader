#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author  : "Satish Sagi"
# Version : "0.1"
# Status  : "Beta"

import argparse
import requests
from bs4 import BeautifulSoup
import re
import os
import jsbeautifier.unpackers.packer as packer
from itertools import izip_longest

base_url = "http://www.ryuanime.com"
anime_name = ''
download_cmd = 'aria2c -s16 -j16 -x16 ##URL## -d ##OPDIR## -o ##OPFILE## --auto-file-renaming=false'


def make_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res
    else:
        return False


def js_unpack(packed_code):
    unpack = packer.unpack(packed_code)
    return unpack


def grouper(n, iterable, fillvalue=None):
    arguments = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *arguments)


def episode_download(urls_list, start, end):
    if start and end is None:
        # end = len(urls_list)
        end = int(urls_list[-1].split('-')[-1])
    elif end and start is None:
        start = 1
    last_ep_num = int(urls_list[-1].split('-')[-1])
    episode_count = len(urls_list)
    if last_ep_num != episode_count:
        print 'Total episodes count(%s) not matched with last episode number(%s). ' % (episode_count, last_ep_num)
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    for ep in xrange(start - 1, end):
        opfile_name = urls_list[ep].split('/')[-1]
        res = make_request(urls_list[ep])
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            ep_iframe = soup.find("iframe", {'src': True, 'height': True, 'width': True})
            ep_iframe_url = ep_iframe['src']
            ep_stream_url_re = r'https?://(?:www\.)?(?P<site_name>myvidstream|mp4upload)\.(?:net|com)/(?P<file_name>[^/?#&]+)'
            match = re.search(ep_stream_url_re, ep_iframe_url)
            if match:
                stream_site_name = match.group('site_name')
                if stream_site_name == "myvidstream":
                    res = make_request(ep_iframe_url)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    player_div = soup.find('div', {'id': 'player_code'})
                    for script_tag in player_div.find_all("script", {'type': 'text/javascript'}):
                        if script_tag.text.startswith('eval'):
                            unpacked_js = js_unpack(script_tag.text)
                            for line in unpacked_js.replace('\\', '').split(';'):
                                if line.startswith('s1.addVariable(\'file\''):
                                    url = line.replace('s1.addVariable(\'file\',\'', '').replace('\')', '')
                                    opfile_ext = url.split('.')[-1]
                                    opfile = opfile_name + '.' + opfile_ext
                                    final_dl_cmd = download_cmd.replace('##URL##', url).replace('##OPDIR##',
                                                                                                args.output).replace(
                                        '##OPFILE##', opfile)
                                    os.system(final_dl_cmd)

                            break
                elif stream_site_name == "mp4upload":
                    pass
            else:
                print "Not supported streaming URL!!"
        else:
            print "Received empty response from server when try to download episode :("


def main_url_download(url, ep_type, start, end):
    res = make_request(url)
    if res:
        soup = BeautifulSoup(res.content, 'html.parser')
        if ep_type == 'sub':
            soup_url_ul = soup.find("ul", {'id': 'anime-episode-list-sub'})
        elif ep_type == 'dub':
            soup_url_ul = soup.find("ul", {'id': 'anime-episode-list-dub'})
        else:
            print "Invalid type!!"
            exit(-1)
        soup_urls = [base_url + li.a['href'] for li in soup_url_ul.find_all("li")]
        episode_download(soup_urls, start, end)
    else:
        print "Received empty response from server :("


def check_url(url):
    ryunaime_url_re = r'https?://(?:www\.)?ryuanime\.com/series-info/(?P<display_name>[^/?#&]+)'
    match = re.search(ryunaime_url_re, url)
    if match:
        global anime_name
        anime_name = match.group('display_name')
        return True
    else:
        return False


def main():
    global args
    parser = argparse.ArgumentParser(description='Ryuanime Downloader')
    required_args = parser.add_argument_group('Required arguments')
    optional_args = parser.add_argument_group('Optional arguments')
    required_args.add_argument("-u", "--url", help="URL to download", required=True)
    required_args.add_argument("-t", "--type", type=str, choices=["dub", "sub"], help="Download type: dub or sub",
                               required=True)
    required_args.add_argument("-o", "--output", help="Output folder", required=True)
    optional_args.add_argument("-s", "--start", help="Starting episode number", type=int)
    optional_args.add_argument("-e", "--end", help="Ending episode number", type=int)
    args = parser.parse_args()
    if check_url(args.url):
        if args.start and args.end:
            if not args.start <= args.end:
                print "Enter valid episode range!!"
                exit(-1)
        main_url_download(args.url, args.type, args.start, args.end)
    else:
        print "Please enter valid URL!!"


if __name__ == '__main__':
    main()
