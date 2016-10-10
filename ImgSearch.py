# -*- coding:utf-8 -*-

import os;
import sys;
import urllib;
import urllib2;
import requests;

def CheckArgs():
    if(len(sys.argv) < 3):
        print 'Usage: python ImgSearch.py [Keyword] [DownloadDir] [Pages=1]';
        return False;
    return True;

def Download(url, filename):
    if(os.path.exists(sys.argv[2]) == False):
        os.mkdir(sys.argv[2]);
    filepath = os.path.join(sys.argv[2], '%s' % filename);
    urllib.urlretrieve(url, filepath);
    return ;

def Request(param):
    searchurl = 'http://image.baidu.com/search/avatarjson';
    response = requests.get(searchurl, params=param);
    json = response.json()['imgs'];

    for i in range(0, len(json)):
        filename = os.path.split(json[i]['objURL'])[1];
        print 'Downloading from %s' % json[i]['objURL'];
        Download(json[i]['objURL'], filename);
    
    return ;

def file_count(dirname,filter_types=[]):
     '''Count the files in a directory includes its subfolder's files
        You can set the filter types to count specific types of file'''
     count=0
     filter_is_on=False
     if filter_types!=[]: filter_is_on=True
     for item in os.listdir(dirname):
         abs_item=os.path.join(dirname,item)
         #print item
         if os.path.isdir(abs_item):
             #Iteration for dir
             count+=file_count(abs_item,filter_types)
         elif os.path.isfile(abs_item):
             if filter_is_on:
                 #Get file's extension name
                 extname=os.path.splitext(abs_item)[1]
                 if extname in filter_types:
                     count+=1
             else:
                 count+=1
     return count

def Search():
    params = {
        'tn' : 'resultjsonavatarnew',
        'ie' : 'utf-8',
        'cg' : '',
        'itg' : '',
        'z' : '0',
        'fr' : '',
        'width' : '',
        'height' : '',
        'lm' : '-1',
        'ic' : '0',
        's' : '0',
        'word' : sys.argv[1],
        'st' : '-1',
        'gsm' : '',
        'rn' : '30'
        };
    
    if(len(sys.argv) == 4):
        pages = int(sys.argv[3]);
    else:
        pages = 1;

    for i in range(0, pages):
        params['pn'] = '%d' % i;
        Request(params);
    return ;

if __name__ == '__main__':
    if(CheckArgs() == False):
        sys.exit(-1);
    Search();
    print 'Total Images:%d' % file_count(sys.argv[2]);
