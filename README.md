# Network Security Final Project: Exploring Common Website Vulnerabilities
Georgia Tech Spring 2021 CS6262/ECE6612 Network Security

Group Members:

Collin Avidano (cavidano3@gatech.edu)

Joshua Dierberger (jdierberger3@gatech.edu)

Abigail Drun (adrun3@gatech.edu)

Eric Hsieh (hsieh.eric@gatech.edu)

Tara Poteat (tpoteat3@gatech.edu)

## Project Overview
We aimed to perform big data analysis on popular websites and check for common vulnerabilities. Our initial dataset (`top-1m.csv`) contains the top 1 million most popular sites from 2014, which was too large to run in a feasible amount of time. Thus, we took a random subset of 10,000 websites as our main dataset and wrote code to explore the following aspects of these websites:

* DNS Records
* Open Ports
* Cipher Suites
* Certificates
* Traceroutes
* Forms and Templates
* Operating Systems

Running our program was very time consuming, so we opted to run it for several days on a server.
## Running Instructions

Run from thread_launcher.py, making sure to change the "8" in Line 127:
>  while len(running) < 8 and idx < min(len(url_list), start_index + number)
with the number of cores/threads you would like to run with.
## Packages
