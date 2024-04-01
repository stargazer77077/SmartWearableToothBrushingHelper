import matplotlib.pyplot as plt
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip

''' ============================================================ '''
import socket
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind((host, port))
mySocket.setblocking(0)
''' ============================================================ '''
addr = None

class Toothbrushing:
    image_paths = []
    current_image_index = 0

    def __init__(self):
        self.image_paths = ["GUI_Resource/0_start.png", "GUI_Resource/1_cm1.mp4", "GUI_Resource/2_horizontal1.mp4", "GUI_Resource/3_cm2.mp4", "GUI_Resource/4_horizontal2.mp4", "GUI_Resource/5_tongue.png", "GUI_Resource/6_rinse.png"]
        self.current_image_index = 0  

    def show_image_or_video(self):
        if (self.current_image_index == 0 or self.current_image_index == 5 or self.current_image_index == 6):
            #if (self.current_image_index == 5):
            #    clip.close()
        # open the image file
            img = Image.open(self.image_paths[self.current_image_index])

            # show the image
            plt.imshow(img)
            plt.axis('off')  # turn off axis
            plt.show()  
        else:
            video_path = self.image_paths[self.current_image_index]
            clip = VideoFileClip(video_path)
            clip = clip.resize((1200, 1200))
            clip.preview()
            clip.close()

    def run(self):
        # show initial image
        self.show_image_or_video()
        #input("Ready to brush your teeth? Press [ENTER] to begin.\n")
        self.current_image_index += 1
        self.show_image_or_video()
        
        while True:
            try: 
                data, addr = mySocket.recvfrom(1024)
                if (data != None):
                    data = data.decode('UTF-8')
                    if "next" in data: 
                        self.current_image_index += 1
                        if (self.current_image_index == 5): 
                            self.show_image_or_video()
                            self.current_image_index += 1
                            self.show_image_or_video()
                            break
                        else: 
                            self.show_image_or_video()
             
            except BlockingIOError:
                pass

            
if __name__ == '__main__':
    toothbrushing = Toothbrushing()
    try:
        toothbrushing.run()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
    finally:
        print("Exiting the toothbrushing program")
        mySocket.close()


