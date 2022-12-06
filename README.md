# Genshin Wish Statistics

# CURRENTLY NOT WORKING ON THIS VERSION ANYMORE PLEASE GO TO THE THIS NEW GITHUB
[link to the new github repo](https://github.com/charliedilorenzo/GenshinWishOracle)

## Index

- [What is this project](/README.md#what-is-this-project)
- [How to use this project](/README.md#how-to-use-this-project)
- [Informing Data](/README.md#informing-data)

## What is this project

If you have ever asked youself "I wonder if this many primos is enough to get Baizhu, my favorite character", then this tool was produced in the hopes of accurately answering that question.

## Immediately Caveats

### Usability

&ensp;&ensp; I have yet to implement any that gives usability to people who aren't familiar with command line. There is no Graphical User Interface, no cursor usage, no automatically saving of data. The features are currently limited and centered around how I personally have been using the tool and the way I personally think about statistics. While graphs can be show to try and convey data, I have yet to add any of that and it is all textual.

### Statistics

&ensp;&ensp; Statistics can tell you certains things about random events with a certain degrees of *CONFIDENCE*. This means that even if I were to know exactly the probabilities behind wishing in Genshin Impact, that does not mean that we should overrely on the outcome. I don't support gambling so I only advocate using these statistics to inform when you have overwhelming high odds for a certain outcome. I've gotten back to back 5 stars and my friend has taken 170 total wishes to get a rateup. Both of these are unlikely and of course one is much more preferrable to another.

If you want a 50% chance, use the scale of 90% chance instead; if you want a 90% change use the scale of 99.4% chance.

### Data

&ensp;&ensp; Above I mentioned knowing the probabilities exactly, however even with that I'm not sure! We enter a degree of metastatistics where the estimates I produce are also relying on a certain degree of confidence in other sources' estimates of probabilities. I use [paimon.moe](https://paimon.moe) to estimate the rising probability of 5 stars that starts at 74ish wishes. However that data probably isn't fully conforming to what I need; caveats are listed by it [here](/README#paimonmoe) below.

### My Skills

&ensp;&ensp; While I do have a fairly robust background in mathematics, I have my limitations in statistics. Additionally, I am not a very well-practiced coder, I don't know coding conventions, and I am ignorant of many of the possibilities in both this language in others. My lack of knowledge of python impacts the code I have already written, and my lack of knowledge of other languages limits my ability to implement certain features.

## How to use this project

### Files for general use

- [main.py](/README.md#mainpy)
- [userinput.py](/README.md#userinputpy)
- [project_execute.py](/README.md#projectexecutepy)
- [daily_record.py](/README.md#dailyrecordpy)
- [/primo_record_files](/README.md#primorecordfiles)

### Executing a .py file

&ensp;&ensp; If you don't know how to set up an environment like this, then I don't think I can help you. Things you would need/might look up would be:

- python
- command line
- python PATH
- pip
- python versions
- python --help

&ensp;&ensp; For those who don't know how to execute a .py file, but can setup the environment, you can use:

```
python ./main.py
python3 ./main.py
```

or something similar with whatever python version you have. There are no command line arguments, however there is command line input required from `main.py`. For a different .file you are interested simply replace the name.

### main.py

&ensp;&ensp; This is the most important file for most people. It uses interaction with the command line in order to give certain information for a breadth of functions. For all of them you may need to input data to command line. If you look at the messages printed on the command line, they should be relatively clear on how to input your data. In theory if you give a completely invalid answer then it should allow you to try and answer again (incorrect but valid answers still pass). Here are the options:

&ensp; 1. Wish Statistics - for this option given the amount of wishes you have available and the amount of trials you want to do, it simulates doing that many trials with that amount of wishes. For example with 10000 trials, it would collect all the data (for example number of constellations obtained) from 10000 different randomized possibilities with your initial amount of wishes. The most interesting statistics it gives is probably the percentage constellation breakdown last. This gives percentages amongst those trials what portion of them got N constellations or no copies of the rateup.

&ensp; 2. Wish Simulator - for this option a stream of 4 star and 5 star characters are generated and printed to the command line. It will stop if you achieve the number of rateups you want (possibly just 1 or whatever). However, it will also stop if it 'runs out of wishes' based on the amount of wishes you gave. At the end it will tell you if you got as many rateups as you wanted and will give a bunch of statistics that might be interesting. Scroll up if you want to look at the simulation output to see what 4 stars and 5 stars you got.

&ensp; 3. Wish Projection - for this option you will provide the date that you want to get a projection for the number of primogems you will have on that date. This is only a prediction and relies on a lot of inference to reach these conclusions. Additionally, it also relies on the fact that you mostly complete all the primogem-providing actions till that date. In general this should undershoot the amount of wishes that you get from events by a 2-5 wishes dependent on how generous the update is.

### userinput.py

&ensp;&ensp; This file is the closest you can get to saving data currently. If you want to try and use this file, simply alter the left side of the equal sign per intuition/instructions. Some abbreviations that you can reference to help understand what to put:

- num -> number
- ru -> rate up
- primos -> primogems

While it is probably good to do this if you plan to use any of these programs a lot, it isnt necessary.

### project_execute.py

&ensp;&ensp; This file gives a projection for a statistical percentage breakdown of constellations for the current time and a date in the future. The date isn't currently alterable and is based on around when I think 3.0 will come out.

### daily_record.py

&ensp;&ensp; Adds the projection for number of primogems in month from the date the program is run to a file and prints it out. Adds the projection for number of primogrems based on some date/version in the future to a file. The latter part is far less accurate likely.

### /primo_record_files

&ensp;&ensp; This is the folder where the output of daily_record.py is stored. The file with "one_month" is much better organized and can probably be well viewed if loaded into Excel or Google Sheets or something. For the file with "over_time" in the name its a bit of a mess and isn't working super well right now. However, below text is the number of primogems for the version number (might need to be updated based on what version is currently out)

## Informing Data

### paimon.moe

&ensp;&ensp; [paimon.moe](https://paimon.moe/wish/tally) is great for all sorts of things and I highly recommend it. First I want to use the caveats that exist with me using it for data :

- initial pity level might not be uniform or predictable across banners
- pity level might not be accurately represented since wish data can expire for in game storage (this happened to me)
- people may accidentally mess up with automatic input
- people may accidentally mess up with manual input
- people can input false data to the database if they want
- etc

As I said I love this side it performs pretty much all of its functions very well. I use it to:

- store my wish data - with the Wish Counter
- make sure that I have enough materials for a character - with the Calculator
- keep track of which characters I am building - with the Todo List
- keep track of my achievements (this one I use a *TON*) - with the Database/Achievements

### Patch Primo Income

&ensp;&ensp; I use [this spreadsheet](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQ29M_-mbMbNgJl5c1ZWJwqgd1sFR6NW8A1Wwy85BUHCZHGtKwfrw_Jy68wd1OOyE6h7jQfEbOckjaM/pubhtml) to estimate how many wishes will be given per update. I estimate around 1500 primogems from events per update. This should be undershooting the data from here for all updates.
