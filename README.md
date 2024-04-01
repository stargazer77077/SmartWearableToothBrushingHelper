### Design Challenge
<li>Finding the Need</li>

The use case my teammates and I are trying to address is to teach and guide young kids to brush their teeth correctly. After doing some research online and from personal experience, we came to the conclusion that ensuring children maintain good oral hygiene is crucial.

According to the Center of Disease Prevention and Control (CDC), statistical data shows that "More than half of children aged 6 to 8 have had a cavity in at least one of their baby (primary) teeth" while "more than half of adolescents aged 12 to 19 have had a cavity in at least one of their permanent teeth". Moreover, one can also see that untreated cavities can lead to "problems with eating, speaking, playing, and learning" and more serious outcomes such as "severe infection under the gums which can spread to other parts of the body, and in rare cases fatal, results". Thus, we intend to prevent cavities by guiding the tooth brushing process of children.

Our solution consists of two parts, the first part is a user interface that displays an animated tooth brushing instruction. The second part is a smart wearable that monitors the movement of the hand and checks if the user is correctly following the instructions. Additionally, the hardware is able to communicate with the GUI and send feedback to guide the user.

<li>Solution Design</li>

To implement the design, the hardware components we chose are the ESP-32 micro processor, ADXL335 accelerometer, and 3 LEDs. The microprocessor serves as the unit for data communication that sends the data collected in the accelerometer and receives the commands from the python software to control the LEDs. On the software side, to distinguish circular motion from back and forth movement of the hand, we used the L1 norm of the acceleration on the three dimensions. To implement this, we used various python libraries, such as <i>socket</i> and <i>scipy</i> for data communication and signal processing. We also instantiated a Tooth Brushing Helper class that includes methods to process the data and determine movement.

The thought process and reason we chose the above method came from analyzing the different motions of the hand when following the tutorial. We inferred that when the hand is in circular motion, acceleration on three axes will fluctuate, while in back and forth motion, only two axes will experience significant change in acceleration. Thus, evaluating the motion in terms of the L1 norm, circular motion will have a larger L1. Following this reasoning, we tested the data by performing the above two motions and the result confirmed our understanding. Therefore, we chose the accelerometer to collect data, and the L1 norm to distinguish motion. To reduce the noise in the data we collected, we first took the moving average and then low-passed the input signal using a butterworth filter.

<li>Link To Video</li>

The link containing the video to this challenge can be found here: https://youtu.be/UJkyIZsGFeI.

### Division of Work

My teammates and I distributed the workload in a reasonable manner so that we both are able to benefit from this project. The detailed work division is as follows.

<li> Space Invaders Controller </li>

| Item  | Person |
| ------------ | ----------- |
| Arduino Code for smoother movement | W.H. |
| Arduino Code for decoupling firing and movement| X.H. |
| Realization of speed control    | X.H. |
| Arduino & Python code for quitting game via Photo-detector |W.H. |
| Arduino & Python Code for LED feedback | Team |
| Python Code for displaying current score | Team |

<li> Design Challenge </li>

| Item  | Person |
| ------------ | ----------- |
| Project idea | Team|
| Signal processing components in Tooth Brushing Helper Class | W.H. |
| User Interface | Team |
| Python code of communication between client and server program | X.H. |
| Python code of distinguishing motion of hand | W.H. |
| Arduino code for sending and receiving data | X.H. |
| Python code for main program | Team |
