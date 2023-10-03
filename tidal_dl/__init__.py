#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import random
import sys
import getopt

from tidal_dl.events import *
from tidal_dl.settings import *

def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hpvl:o:q:r:", 
                                   ["help", "process" "version", "link=", "output=", "quality", "resolution"])
    except getopt.GetoptError as errmsg:
        Printf.err(vars(errmsg)['msg'] + ". Use 'tidal-dl -h' for useage.")
        return

    link = None
    process = False
    for opt, val in opts:
        if opt in ('-h', '--help'):
            Printf.usage()
            return
        if opt in ('-p', '--process'):
            process = True
            continue
        if opt in ('-v', '--version'):
            Printf.logo()
            return
        if opt in ('-l', '--link'):
            link = val
            continue
        if opt in ('-o', '--output'):
            SETTINGS.downloadPath = val
            SETTINGS.save()
            continue
        if opt in ('-q', '--quality'):
            SETTINGS.audioQuality = SETTINGS.getAudioQuality(val)
            SETTINGS.save()
            continue
        if opt in ('-r', '--resolution'):
            SETTINGS.videoQuality = SETTINGS.getVideoQuality(val)
            SETTINGS.save()
            continue
    
    if not aigpy.path.mkdirs(SETTINGS.downloadPath):
        Printf.err(LANG.select.MSG_PATH_ERR + SETTINGS.downloadPath)
        return


    if link is not None:
        if not loginByConfig():
            loginByWeb()
        Printf.info(LANG.select.SETTING_DOWNLOAD_PATH + ':' + SETTINGS.downloadPath)
        start(link)

    if process is not None:
        if not loginByConfig():
            loginByWeb()
        while True:
            processArtists()
            secs = random.randrange(200, 400)
            Printf.info("FINISHED PROCESSING ARTISTS! SLEEPING FOR: " + secs + " SECONDS")
            time.sleep(secs)

def main():
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())
    
    if len(sys.argv) > 1:
        mainCommand()
        return
    
    Printf.logo()
    Printf.settings()
    
    if not apiKey.isItemValid(SETTINGS.apiKeyIndex):
        changeApiKey()
        loginByWeb()
    elif not loginByConfig():
        loginByWeb()
    
    Printf.checkVersion()
    
    while True:
        Printf.choices()
        choice = Printf.enter(LANG.select.PRINT_ENTER_CHOICE)
        if choice == "0":
            return
        elif choice == "1":
            if not loginByConfig():
                loginByWeb()
        elif choice == "2":
            loginByWeb()
        elif choice == "3":
            loginByAccessToken()
        elif choice == "4":
            changePathSettings()
        elif choice == "5":
            changeQualitySettings()
        elif choice == "6":
            changeSettings()
        elif choice == "7":
            if changeApiKey():
                loginByWeb()
        else:
            start(choice)


def test():
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())
    
    if not loginByConfig():
        loginByWeb()
        
    SETTINGS.audioQuality = AudioQuality.Normal
    SETTINGS.videoFileFormat = VideoQuality.P240
    SETTINGS.checkExist = False
    SETTINGS.includeEP = True
    SETTINGS.saveCovers = True
    SETTINGS.lyricFile = True
    SETTINGS.showProgress = True
    SETTINGS.showTrackInfo = True
    SETTINGS.saveAlbumInfo = True
    SETTINGS.downloadPath = "./download/"
    SETTINGS.usePlaylistFolder = True
    SETTINGS.albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    SETTINGS.trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    SETTINGS.videoFileFormat = R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"
    SETTINGS.multiThread = True

    Printf.settings()
    # test example
    # https://tidal.com/browse/track/70973230
    # track 70973230  77798028 212657
    # start('70973230')
    # album 58138532  77803199  21993753   79151897  56288918
    # start('58138532')
    # playlist 98235845-13e8-43b4-94e2-d9f8e603cee7
    start('98235845-13e8-43b4-94e2-d9f8e603cee7')
    # video 155608351 188932980
    # start("155608351")


if __name__ == '__main__':
    # test()
    main()
