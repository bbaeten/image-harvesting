##Youtube Stripper

import pafy
import vlc
import os
import time
import argparse



class youTubeHarvester():

    def __init__(self, url, skipTime, imgDir, verbose):        
        video = pafy.new(url)
        if verbose:
            print('Video loaded: %s' % video.title)
        self.videoId = str.split(url, "=")[1] + "_"
        best = video.getbest()
        self.url = best.url
        self.skipTime = int(skipTime)*1000
        self.imgDir = imgDir
        self.verbose = verbose

        self.recordTime = 0
        self.harvesting = False
        self.waitForBuffer = False

    def callbackBuffering(self, arg):
        if(self.recordTime + self.skipTime < arg.u.new_time and self.harvesting):
            self.waitForBuffer = False

    def harvestVideo(self):
        try:
            os.mkdir(self.imgDir)
            if self.verbose:
                print('Created Directory: %s' % self.imgDir)
        except FileExistsError:
            if self.verbose:
                print('Directory: %s already exists' % self.imgDir)

        Instance = vlc.Instance()
        player = Instance.media_player_new()
        eventManager = player.event_manager()
        eventManager.event_attach(vlc.EventType.MediaPlayerBuffering, callback = self.callbackBuffering)
        Media = Instance.media_new(self.url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        time.sleep(.5) # wait till the window appears
        player.pause()
        self.harvesting = True

        if self.verbose:
            print("Begin Harvesting...")
        while(player.get_time() < player.get_length()):            
            self.waitForBuffer = True
            self.recordTime = player.get_time()
            filename = '{}{}_{}'.format(self.imgDir, self.videoId, str(self.recordTime))
            player.video_take_snapshot(0, filename ,i_width=player.video_get_width(), i_height=player.video_get_height())
            if self.verbose:
                print('image saved to: %s\t\t' % filename)
            player.set_time(self.recordTime + self.skipTime)

            while(self.waitForBuffer):
                if self.verbose:
                    print(".", end="")
                time.sleep(0.1)
            time.sleep(0.5)

        if self.verbose:
            print("Harvesting complete\n\n")

    def reNameFiles(self):
        for f in os.listdir(self.imgDir):
            if f[-4:] != ".jpg":
                s = f.split('.')
                if len(s) > 1:
                    if s[1] == "jpeg":
                        filename = self.imgDir + s[0]
                        newname =  self.imgDir + s[0] + ".jpg"
                        os.rename(filename, newname)
                    else:
                        print("file: %s is of another extention, please convert." % f)
                        continue
                else:
                    filename = self.imgDir + s[0]
                    newname =  self.imgDir + s[0] + ".jpg"

            os.rename(filename, newname)
            if self.verbose:
                print("file: {}\trenamed to: {}".format(self.imgDir + s[0], self.imgDir + s[0]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, required=True, help="YouTube url for video to harvest from")
    parser.add_argument('-s', type=int, default=10, help="time interval in seconds to harvest screenshot. Default 10")
    parser.add_argument('-o', type=str, default='images/', help="folder to output image files. Default images/")
    parser.add_argument('-r', action='store_true', default=False, help="rename files to .jpg after finishing")
    parser.add_argument('-v', action='store_true', default=False, help="Verbose")
    args = parser.parse_args()

    harvester = youTubeHarvester(args.u, args.s, args.o, args.v)
    harvester.harvestVideo()
    if args.r:
        harvester.reNameFiles()

if __name__ == '__main__':
    main()