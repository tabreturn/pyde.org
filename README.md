# Processing Python Mode Resources

*A collection of examples, cheatsheets, and other Processing Python Mode / Processing.py resources*

This repository hosts the source files for pyde.tabreturn.com -- which includes Python Mode ports of the Java examples on the official [Processing wesbite](https://processing.org/examples/) presented in format resembling the [Generative Design website](http://www.generative-gestaltung.de/2/).

<!-- You can view the [live website here](http://pyde.tabreturn.com). -->

## Instructions

This is a hand-rolled static site generator. Run *generate.py* to generate the website files (*_site* directory).

## Todo

- [ ] integrate pyp5js
  - [x] refactor generate.py
  - [x] generate example directories from md (then compile and move them into _site)
  - [ ] replace p5js functions in transcrypted code to processing.py -- i.e. `createCanvas()` to `size()`
  - [ ] ...
- [ ] style website
  - [ ] define colors and fonts with inspiration from the processing.org website
  - [ ] define layout with inspiration from generative design (new book) website
  - [ ] ...
- [ ] design cheetsheat
  - [ ] see oc/temp files
  - [ ] ...
- [ ] other ...
