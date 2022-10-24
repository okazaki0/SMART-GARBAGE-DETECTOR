# SMART-GARBAGE-DETECTOR #

The main idea is to build a deep learning model CNN to detect images and classify them into three types of garbage or classify them as not garbage using python programming language and its machine learning libraries. The model is then downloaded into the raspberry. 


<img width="351" alt="image" src="https://user-images.githubusercontent.com/12214522/197517569-de3b865c-d886-4400-aead-2b759ca70790.png">


## How does function ##

SMART GARBAGE DETECTOR is a sufficient and smart robot, once the program on the Raspberry is launched, the robot will start moving and exploring the area, it is capable of avoiding obstacles via a threshold that can be updated, this means that the robot with the use of ultrasonic sensor won’t stop or crash and keep moving and discovering the regions until a potentially garbage image is found.
When the robot makes a temporary stop, there is two possible options. The first one, is that the robot detected a wall or an obstacle, if that’s the case it will change direction and continue his search for garbage. The second one, which is the most interesting one is that the robot will take a picture, use the model to classify it. Then return the result alongside with the accuracy.
The output will be communicated to the user on his phone as a notification using MQTT protocol which is a machine to machine “internet of things” connectivity protocol. It was designed as an extremely lightweight publish/subscribe messaging transport. It is useful for connections with remote locations where a small code footprint is required and/or network bandwidth is at a premium. This makes it the perfect choice for our case.

## Robot movement ##

We implemented an algorithm with python to make the robot move freely making him avoid obstacles. The use of ultrasonic sensor is handy in the movement, we set a threshold on which the Grillo will stop and make a decision based on the captured image, if it is just an obstacle the robot will change direction and continue on its way, otherwise it will classify the object in the image with a certain level of accuracy.

## CNN model ##

We built the neural network model from scratch since we are familiar with computer vision that is image classification and object detection, the first step was to collect data, we had to assemble objects that we usually found thrown on the floor. We made short videos for those objects with different backgrounds to avoid overfitting the model so that the model can perform and classify new data or images without making huge mistakes. 
We extracted images from these videos using python codes. We made three positive classes labeled biscuit_garbage, bottle and pape_related_garbage such Kleenex and balled up paper …etc, on the same context, a negative class was also made to classify non-garbage objects.
We used Convolutional neural network which is a class of deep neural networks in deep learning, they are commonly used and applied for analyzing visual imagery which makes them perfect for this case study.
After getting the data ready, we build the model and add layers to it, for the activation function, relu has proven better performance in our case. Next the model is fitted on the train data through 5 epochs. This step takes time since it needs important GPU capacity because of the massive size of training data we extracted from the videos we take of different garbage types. 
We used Kaggle platform since it offers a good amount of GPU capacity to run the training phase, we got a very satisfying results with an accuracy of 98%. This a very encouraging percentage since our model is almost capable of classifying everything on the training dataset, thus, there will be no collision and robot will keep moving.
The next step is to save the model to download it later on Raspberry and combine it with the robot movement code for automatization.  

## Mqtt Protocol ##

This is an added feature to our project which is the notifications service using Mqtt protocol. The first obvious step is to establish some sort of connection between the Raspberry Pi and the user phone, to do this we used the Mqtt Dashboard application.
Next the Raspberry Pi create a topic so that the user can subscribe to it, once this is done the user start getting notifications from the raspberry using a loop, so every time the Pi captures a signal, the user gets a notification.

