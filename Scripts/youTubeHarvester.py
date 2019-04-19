##Youtube Stripper

import pafy
import vlc
import os
import time
import argparse



class youTubeHarvester():

    def __init__(self, url, skipTime, imgDir):        
        video = pafy.new(url)
        self.videoId = str.split(url, "=")[1] + "_"
        best = video.getbest()
        self.url = best.url
        self.skipTime = int(skipTime)*1000
        self.imgDir = imgDir
        print(self.imgDir)

        self.recordTime = 0
        self.harvesting = False
        self.waitForBuffer = False

    def callbackBuffering(self, arg):
        if(self.recordTime + self.skipTime < arg.u.new_time and self.harvesting):
            self.waitForBuffer = False

    def harvestVideo(self):
        try:
            os.mkdir(imgDir)
        except:
            pass

        Instance = vlc.Instance()
        player = Instance.media_player_new()
        eventManager = player.event_manager()
        eventManager.event_attach(vlc.EventType.MediaPlayerBuffering, callback = self.callbackBuffering)
        Media = Instance.media_new(self.url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        time.sleep(5) # wait till the window appears
        player.pause()
        self.harvesting = True

        while(player.get_time() < player.get_length()):
            self.waitForBuffer = True
            path = self.imgDir + self.videoId + str(player.get_time() )
            print("image will be taken at " + str(player.get_time() ) + "ms at path "+ path )   
            time.sleep(0.5)
            self.recordTime = player.get_time()
            player.video_take_snapshot(0,  self.imgDir + self.videoId + str(self.recordTime) ,i_width=player.video_get_width(), i_height=player.video_get_height())
            player.set_time(self.recordTime + self.skipTime)

            while(self.waitForBuffer):
                print("waiting for buffering")
                time.sleep(0.1)

    def reNameFiles(self):
        for f in os.listdir(self.imgDir):
            if f[-4:] != ".jpg":
                s = f.split('.')
                if len(s) > 1:
                    if s[1] == "jpeg":
                        os.rename(self.imgDir + s[0], self.imgDir + s[0] + ".jpg")
                    else:
                        print("file: %s is of another extention, please convert." % f)
                else:
                    os.rename(self.imgDir + f, self.imgDir + f + ".jpg")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, help="YouTube url for video to harvest from")
    parser.add_argument('-s', type=int, help="time interval in seconds to harvest screenshot. Default 10")
    parser.add_argument('-o', type=str, help="folder to output image files. Default images/")
    parser.add_argument('-r', action='store_true', help="rename files to .jpg after finishing")
    args = parser.parse_args()
    if args.s is None:
        args.s = 10
    if args.o is None:
        args.o = 'images/'

    harvester = youTubeHarvester(args.u, args.s, args.o)
    harvester.harvestVideo()
    if args.r:
        harvester.reNameFiles()

if __name__ == '__main__':
    main()