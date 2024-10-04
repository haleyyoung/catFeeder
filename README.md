# The Evolution of the Automatic Cat Feeder

Meet OnePaw.

![OnePaw cat](https://github.com/user-attachments/assets/084a7f50-f7d2-4225-895c-174c5d6ed3a0)

## Once Upon a Time...

We moved into our house, blissfully unaware that it came with a cat. OnePaw socialized with us often and
we always wondered who she belonged to. Any time we'd leave the front door open, she would come waltzing
in to explore, but happily lived outdoors. One Winter, she decided to let us
know that she wasn't just visiting us to be friendly; she actually needed a place to stay. Eventually we got the message
and she very quickly convinced us to let her back into *her* house. 

_Before we get any further, to clear up a common question...she had four paws, but she always sat and lifted **one paw**
to ask for pets._

She enjoyed her fancy life, lounging on couches with food readily available, but we noticed her appetite diminish.
We took her to the vet, who informed us that she had
[Stomatitis](https://www.petmd.com/cat/conditions/mouth/stomatitis-in-cats). Stomatitis
is an auto-immune disease in cats that makes their gums overreact, swell and hurt.
To help OnePaw eat, we turned to hypo-allergenic rabbit wet food, and eventually had to add water and blend the food into an
oh-so-appetizing rabbit pâté smoothie.

_So why is this story being told on GitHub?_

We went camping (glamping) a lot. And with OnePaw's new need for special food, that meant she had to agree to being a camping
cat.

## The problem:
OnePaw was tired of going camping with us, but she needed freshly blended wet food and we still
wanted to go on our adventures.

## The solution:
We created an overly complicated [Rube Goldberg machine](https://en.wikipedia.org/wiki/Rube_Goldberg_machine)-style
contraption to serve OnePaw fresh rabbit smoothies while we were camping.

A basic breakdown of the machine's functions were:
1. Distribute a fresh bowl for every feeding
2. Mix the rabbit smoothie
3. Distribute the smoothie

_Yes, this is the result of presenting this problem to a mechanical engineer and a software developer._

tl;dr see the demo [here](https://github.com/haleyyoung/catFeeder/edit/master/README.md#the-rube-goldberg-machine).

We had a few known parameters going into this project:
- OnePaw needed fresh food twice a day
- We served her food in a bowl
- The food had to be of smoothie consistency
- The smoothie started to separate after being blended

With these parameters, we decided there were a few main pieces to the hardware:
- A place to store a large supply of pre-blended rabbit smoothie
- A stirring mechanism to keep the smoothie from separating
- A way to distribute the smoothie in reasonably sized portions
- A method of providing a clean bowl for every meal

## Hardware Features

### The Large Supply of Pre-Blended Rabbit Smoothie

We chose a simple plastic cereal container for the vat of smoothie, since it was food-safe,
sealed well, and was strong enough to support moving mechanisms.
The rabbit smoothie had to be refrigerated, so naturally, we decided to buy a nice, new mini fridge
and immediately drill a hole in the side.

_Why a hole in the side, you ask?_

The easiest way to get the smoothie out of the fridge was **not** by opening the door,
but rather with
- A hole in the cereal container
- A 12-volt ball valve
- PVC tubing

We connected all those pieces together and sent the PVC tubing through the freshly drilled hole in our new fridge.

### The Stirring Mechanism

As for keeping the smoothie from separating, we decided to attach a 3D-printed stirrer to a DC motor on the lid of the cereal container. This made removal and cleaning easy. We went through several stirrer designs to find one that effectively mixed the smoothie.

![Vat stirrer](https://github.com/user-attachments/assets/ebc3a5a4-72e8-4710-97c6-a6a7de702653)

### Reasonably Sized Portions

The ball valve connecting the cereal container and PVC tubing could be controlled in two ways:
- The diameter of the opening
- The amount of time open

This meant that we could control the flow of the smoothie pretty well. We had a few too many incidents of
rabbit smoothie splashing out of a bowl, making a huge mess, because it was traveling too fast! So we opted for enough
flow to push the smoothie all the way down the PVC tube, but not so much that it was barreling along.

Another caveat to this whole flow ordeal was that we had to be consistent with the viscosity of the smoothie. All of our
testing would be for naught if the smoothie was thicker or thinner than the one we tested with. So we ultimately
followed a very precise blending recipe.

### A Clean Bowl for Every Meal

This was the most complicated part of the mechanics of this build. There were two main components to this step of the
feeding process:
1. Get rid of the old dirty bowl
2. Distribute a new clean bowl

#### 1. Get Rid of the Old Dirty Bowl
We came up with the idea of putting Onepaw's whole feeding area on top of a large, shallow storage bin. This way, we could
put a platform on top of the bin with a trap door so that we could dispose of used bowls by dropping them in the bin.

We then attached the trap door to a [linear actuator](https://en.wikipedia.org/wiki/Linear_actuator). We originally used a timer to stop the door motor, but we found difficulty in estimating the right duration. This was due to things like...
- The linear actuator slipping because there was too much weight on the trap door (_aka OnePaw didn't eat her food_)
- The motor providing inconsistent quantities of power output

So we decided to install limit switches on either side of the door. This way, we would know if the door hit the
"open" switch or the "close" switch and we didn't need to care about timing at all!

#### 2. Distribute a New Clean Bowl
The clean bowl distribution was much harder. We decided to use paper bowls, since they're very light. We couldn't
just have a stack of bowls, because only very intricate (expensive) robot hands could separate a pile of
paper bowls. This is how the Bike Chain Bowl Ferris Wheel was born! We made a 3-foot tall rectangular frame
out of [aluminum extrusions](https://eagle-aluminum.com/what-is-extruded-aluminum/) to be used as vertical storage for the bowls. We attached several old bike chains to yet another DC motor with 3D-printed gears. Then we 3D printed some plastic tabs to clip onto the chain links. These stuck out just enough to
balance a paper bowl. Each chain link provided the separation we needed between the bowls so that one could be distributed 
at a time.

https://github.com/user-attachments/assets/69a49a43-0766-4bde-a067-7a570d82723e

Once a bowl reached the bottom of the bicycle chain loop, the holding tabs would start to rotate down, and the bowl would free-fall.
We needed the bowl to precisely land on the trap door every time. To accomplish this, we did two things:
- Added an acrylic ~ramp~ slide between the Bike Chain Bowl Ferris Wheel and the trap door
- Figured out that the most reliable way to place the bowl precisely was to put a magnet under the trap door, and
tape a washer to the bottom of each bowl. This made each bowl snap into place!

## The Completed Rube Goldberg Machine

_Is your imagination having a hard time visualizing how all these pieces fit together? Here's a demo!_

https://github.com/user-attachments/assets/4978f9fc-1669-4e4d-9709-1a42cf4cffd2

[The code](https://github.com/haleyyoung/catFeeder/blob/master/feedOnepaw.py#L7-L10) was broken down into the following tasks:
1. Clear the old bowl by using the trap door
2. Drop a new bowl using the Bike Chain Bowl Ferris Wheel and ramp
3. Mix the food
4. Send some food down the tube, landing in the bowl

_Tada!_ 🥳

This was all repeated twice a day.

## Software Features

_Note: The commit messages accurately describe a messy at-home project. We'll clean them up eventually._

All of these mechanical features were controlled with a Raspberry Pi and some
simple Python scripts. Those scripts were then run with `tmux`, allowing
us to control them from different SSH sessions without interrupting the schedule
of the feeder itself.

## Things That Went Wrong

_Here is where the comedy ensues..._

As with most projects like this, it was like playing a never-ending game of Whack-a-Mole.
Some of the more ridiculous features on this build came from unpredicted fiascos.

We caught some of the bugs by using the cat feeder while we were at home,
but still ran into some issues while we were away camping. To mitigate an actual emergency,
resulting in a call to a family member to feed OnePaw, we had:
- Several live cameras pointed at the more problematic parts of the build
- A way to remotely log into the Raspberry Pi
- Emergency scripts containing fixes to our most common hardware bugs

### The Clogged Drain

The original build stirred the food right before distribution. This worked great during all of our prototype tests, but
didn't work as well in reality. Why? The separation of the smoothie was much more exaggerated when the food was left
sitting for the entire time between morning and evening feedings. This meant that the 30 seconds of stirring right before
distribution wasn't enough to fully remix the smoothie. The food at the bottom of the container was so thick that it clogged
the drain leading to the ball valve. Although our system functioned properly on a mechanical level, no food was coming out!

We tried stirring for 1 minute instead of 30 seconds, then 2 minutes, then we added a second stirrer. Nothing helped except
for making sure the smoothie never separated to that point, which meant that we added a Cron job to stir the food once every
hour.

This resolved the issue of food not coming out of the tube, until...

### A Vacuum Effect

Well, it turns out cereal bins are air tight. And rightly so, because who likes stale cereal?

After about 2 days of feeding, food was barely dribbling down the tube, despite the fact that there
was plenty of food in the vat. It took us a while to figure this one out because there were no obvious
visual or logical clues for us to latch onto.
- The food was properly stirred
- The drain wasn't clogged
- The food had been distributing properly for a couple days

Since we were taking advantage of gravity to push the food out of the tube, we knew that the flow
of smoothie would slow as the days went on without a smoothie refill. But we finally realized that the flow
was slowing down too much for the amount of smoothie that was still effectively being used for gravitational
purposes. And this was when we realized there was a vacuum effect occurring in the cereal container.

This was one of those "oh I found a typo" moments. Finding the problem took forever, but the solution was so
simple: pop open the pour spout at the top of the container.

The system was now able to reliably feed OnePaw for about 4 or 5 days! The longer trips were the ones 
that OnePaw particularly didn't like to go on, because she was stuck "indoors" in our camper for days on end. At home
she had a cat door, so she could go explore outside whenever she wanted. So this increased duration of food
supply was a game-changer for all three of us.

### A Dirty Bowl Traffic Jam

Now that we were able to go on slightly longer camping trips, the next whack-a-mole challenge surfaced: the discarded
bowls were piling high enough to block the trap door from closing properly.

Not only did this result in us being unable to use the system at all, because the fresh bowl's platform
wasn't available, but it also caused us to burn out the trap door motor every time this happened!

_Why did the motor burn out?_

[The code](https://github.com/haleyyoung/catFeeder/blob/master/catFeeder.py#L95) relied on two limit switches
to determine if the door was closed or open. Otherwise, the code was just sitting in a `while` loop,
waiting for a signal from the limit switch. So when the door failed to hit the limit switch, the motor
indefinitely tried to push a door that wasn't moving, ultimately causing it to overheat.

The bowls stacked very nicely in their discard bin if OnePaw ate all of her food, but if she didn't, they'd often land
in the discard bin tilted or sometimes completely flipped over. This meant that the pile of bowls got tall enough to block
the door at an unpredictable rate.

We decided to steal an idea from the automatic cat box cleaners to solve this one. We added a bar, driven by a linear
actuator, across the discard bin that could push all the bowls to the other end of the bin, thus clearing out the
space just under the trap door.

We also added [a caveat](https://github.com/haleyyoung/catFeeder/blob/master/catFeeder.py#L123) in the code.
We knew the door could consistently close in under 10 seconds. If it didn't,
we would cancel the door closing procedure and log that it had failed. Finally we stopped burning out motors!

### A Picky Kitty

We got this whole overly-engineered machine working well, and then OnePaw decided to throw us for a loop. She only wanted
to eat the food if it was freshly distributed from the fridge. She was enjoying her time at home,
going outside and exploring all day, so she was often not present right when the timed feedings occurred.

Enter motion sensors.

With the addition of motion sensors, we were able to feed Onepaw whenever she was ready to eat. We put two sensors
facing the feeding platform. Because we were getting a lot of false positives, both sensors had to [receive movement
for 3 seconds](https://github.com/haleyyoung/catFeeder/blob/master/feedCatOnMotion.py#L21)
before the system would consider the signal "real movement".

OnePaw loved this! She could eat whenever she wanted to, receiving the freshest food! Her original apprehension of
all the noises caused by the motors and solenoid even turned into excitement.

https://github.com/user-attachments/assets/b4ccf8ba-8002-4642-9a11-a0bc712ac172

### A Feature for the Humans

OnePaw was finally happy with the latest iteration of the system, which gave us some time to focus on our
own feature requests. We were often camping in places where we had no cell service. We'd routinely wander, searching
for service, so that we could:
1. Check the cameras for system failures
2. Remotely log into the Raspberry Pi
3. Sift through the overly-verbose logs to find out when OnePaw had last been fed

So we set up the ability to
[send ourselves text messages](https://github.com/haleyyoung/catFeeder/blob/844cfe772c6602eacbb2cb7ac7ffa48a7099bd8a/catFeeder.py#L203)
for the two most important types of events:
- When OnePaw got fed
- Alerting us when the trap door got stuck

This feature was still limited by whether or not we had cell service, but we could receive text messages with much less service than
was required to SSH into the Raspberry Pi.

### The Last Mole...or a Moose?

Enter our new dog! Moose.

![Moose dog](https://github.com/user-attachments/assets/7bf7cbd0-37b2-4c15-99f7-16a1c63e1a60)

Very predictably, he found the rabbit smoothie even more appetizing than OnePaw did.
Which meant we needed to implement anti-dog measures. We had the cat feeder in a cubby, so we put a board over
the entrance to the cubby and cut a OnePaw-sized hole in it, so only she could get in there.

Unfortunately, Moose found his way around this fix...

https://github.com/user-attachments/assets/b0c6633f-e072-4dbe-8ec9-8f4d0b76f3c1


Fortunately, he wasn't often successful in stealing OnePaw's food because it was very obvious when he was about
to do something mischievous. So we took the low-tech approach of being more attentive to taking her food bowl
as soon as she was done eating.

## The End

If you've made it this far, you must have a strong interest in overly-complex projects, or a love for cats...or maybe both!
Thank you for listening to our ridiculous story, please let us know if you have any suggestions or questions, we'd
love to hear them!

Unfortunately, this story doesn't have a happy ending for OnePaw. She succumbed to her health problems after we
all fought them together for about 2 years. But she lived a free-spirited life for as long as she could. RIP Onepaw. ❤️
