# Coders Strike Back - Racing Pod

![alt text](https://www.dropbox.com/s/iz2oatmels4mt8a/racer.png?raw=1 "Pod in action")


[in action](https://www.codingame.com/replay/460363234)  
[in action](https://www.codingame.com/share-replay/464712489)  

[losing due to boshing](https://www.codingame.com/share-replay/464682726)  
[losing due to sub optimal cornering](https://www.codingame.com/share-replay/464451296)

Currently around 100th position in the "gold league".


## The approach

I have not implemented genetic algorithms as many have done and used lots of trigonometry to calculate angles, compensations and headings.  
The pod will initially head towards its next checkpoint. At a certain distance it will make a small adjustment to its course so as to maximise the angle to the next checkpoint. It is like swerving out before taking a corner so that speed can be maintained.  
As the pod approaches the checkpoint, based on the angle to the following checkpoint it will choose an appropriate cornering sequence. If, for example, it is a very tight turn, such as a hairpin turn, it will shut off the engine and turn to face the next checkpoint. At the right moment it will begin thusting again towards the next checkpoint. This allows cornering to be tight, making the pod just skim the checkpoint.  
The code calculates the heading required to compensate for its momentum. In earlier revisions, it would just head towards the center of the next checkpoint. If there was a lot of sideward momentum on the pod, it sometimes led to the pod circling the checkpoint, sometimes even establishing a stable orbit around the checkpoint. To remedy this the code calculates a heading so as to compensate for this sideward momentum. This I believe has been the main success in this code.

## The code

I have a few classes, a point class with basic x and y properties and a few methods to add, subtract etc. A vector class which is similar to the point class except it has a few methods that are for vectors and not for points. The main classes are the pod class and the checkpoint relation class. These calculate the angles, positions, compensations etc for each turn.

The pod class has a get_heading method which contains the main algorithm for racing, and outputs an x and y coordinate for the pod to aim for.

The last thing I added was simple collision detection, which activates the shield if a strong collision with the enemy is going to take place.

## Areas for improvement

Short of implementing a genetic algorithm, I believe that with some tweaking of the parameters for corners, how much compensation is made to side to side momentum and how much the pod prepares for cornering, that it may be possible to get into the "legendary" league.

Or implementing a way for my second pod to act as a 'blocker' and actively seek to collide with the enemy that is in first position.

Another way is to try and detect that a collision will happen way before it does, and to try and avoid that collision. Which would involve predicting the positions of the pods many turns in advance.


