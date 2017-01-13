# PyMKFGame

This repo houses a code library I've written that helps me make games in Python 2, with Pygame.

## What's In A Name?
PYMKFGame is the Python version of MKFGame.  MKFGame is a game code library I wrote in college, in C++.  By "game code library", I mean "jumble of code files I slapped together one semester in a graphics programming course, so I could finish my semester projects/assignments."  The C++ version of MKFGame is not available online; it exists solely in my backup hard drives. :-D

## About The Library
The motivation for this library was to see if I could write a generic library that could be used in a wide range of games.  Of course, I wanted to keep the games simple, to prevent attempting to write a library that rivals everything that a Unity/Unreal (or other) engine can do much better.  As a result, this library is extremely barebones.  It is developed with a bottom-up approach:  I have added functionality to as the need has arisen (and I have tried to avoid giving rise to many needs).

**NOTE**:  This library is not meant to be used by developers to make games, though I would like to reach the point where I write a library robust enough for community use.  It is missing many components that a full-fledged library would have, it contains code that is experimental and/or unused, and it is generally not user-friendly.  This repository is provided as a learning tool, and as a dependency for any of my Python+Pygame games that use it.

Note also that if you want to run a game that depends on this library, you will likely need to set up your Python environment to be able to find it.  On Linux (and also Mac, I think), this means setting your PYTHONPATH environment variable to include the location on your file system where you clone this repository.  On Windows, this means adding/updating a PythonPath environment variable to point to the location where you clone this repo (something like Computer -> Properties -> Advanced System Settings -> Environment Variables).

