# Coders Strike Back - Racing Pod

![alt text](https://www.dropbox.com/s/iz2oatmels4mt8a/racer.png?raw=1 "Pod in action")


[in action](https://www.dropbox.com/s/0h75f55m5z2kag4/2020-06-14%2016-11-12.mkv?dl=0)  
[in action](https://www.dropbox.com/s/t2olmx2y5zd2n48/2020-06-14%2016-12-40.mkv?dl=0)  

[losing due to collisions](https://www.dropbox.com/s/j8n49asq2xnlyfu/2020-06-14%2016-13-54.mkv?dl=0)  
[losing due to sub optimal cornering](https://www.dropbox.com/s/njes5bnblwdefgl/2020-06-14%2016-14-44.mkv?dl=0)  

Ranked in the top 1% worldwide.

Due to the nature of the competition code is limited to a single file.

## The approach

This code does not implement genetic algorithms as many have done and instead uses physics and trigonometry to calculate angles, compensations and headings.

The pod will initially head towards its next checkpoint. At a certain distance it will make a small adjustment to its course so as to maximise its angle to the next checkpoint. It is like swerving out before taking a corner so that speed can be maintained.

As the pod approaches the checkpoint, based on the angle to the following checkpoint it will choose a pre-defined cornering sequence. If, for example, it is a very tight turn, such as a hairpin turn, it will shut off the engine and turn to face the next checkpoint. After a delay it will begin thrusting again. This allows cornering to be tight, making the pod just skim the checkpoint.

The code calculates the heading required to compensate for its momentum. In earlier revisions, it would just head towards the centre of the next checkpoint. If there was a lot of sideward momentum on the pod, it sometimes led to the pod orbiting the checkpoint. To remedy this the algorithm calculates a compensated heading.

## Areas for improvement

Short of implementing a genetic algorithm, with some tweaking of the parameters for corners, how much compensation is made to side to side momentum and how much the pod prepares for cornering, that it may be possible to rise up in the league a little more.

Or, implementing a way for my second pod to act as a 'blocker' and actively seek to collide with the enemy that is in first position.

Another way is to try and detect a collision before it happens, and try and avoid it. However, this would involve trying to predict the positions of the pods many ticks in advance.



