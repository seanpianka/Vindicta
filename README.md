# Vindicta

A Python 3 script making heavy use of selenium, paired with LXML and regular 
expressions, which attempts to automate the course enrollment process. 

It is very effective at combatting the tedious nature that is trying to create the
perfect class schedule.

 Did someone take your class and leave you stuck with an 8am Calculus II class for four days a week over twelve weeks of the Summer college session? Vindicta is here to help.

## Installation

*Only Python3.5+ compatible!*

To use the script, first clone the repository:

```bash
git clone https://github.com/seanpianka/Vindicta.git
```

Install library dependencies using your system's package manager (required for `lxml`):

```bash
$ [sudo] apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
```

Install the Python libraries, using pip, located within the requirements.txt file.

```bash
$ [sudo] pip install -r requirements.txt
```

Then, make sure you have the most up-to-date `chromedriver` downloaded (`geckodriver` support is spotty at the moment). You will use the path to the `chromedriver` (or `geckodriver`) with the `--executable-path` argument to `vindicta.py`.

Additionally, ensure that you specify `--browser` with either `firefox` or `chrome` as an argument to `vindicta.py`. This will eventually be deprecated, but is required at the moment.

* Downloads:
    * [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)
    * [geckodriver](https://github.com/mozilla/geckodriver/releases)

## Usage

##### Standard Usage

Vindicta works by updating the page at a varied interval to check for a change
in the availabity status of the classes located in the student's cart. While it
is currently unable to perform class swapping, Vindicta is able to recognize
when a class has an available slot to enroll and will attempt enrollment of
said class.

To run Vindicta (after the necessary dependencies have been installed):
```bash
$ python vindicta.py --browser chrome --executable-path ../drivers/chromedriver --xxx-id 'abc123' --password 'hunter2'
```

The student will be asked to provide their student ID and the password to their
account.

##### Command-Line Arguments

Alternatively, the command-line arguments may be specified:

```
usage: vindicta.py [-h] [-f XXX_ID] [-p PASSWORD] [-n NOTIFY] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -f XXX_ID, --xxx-id XXX_ID
                        Username for the student's MyXXX account.
  -p PASSWORD, --password PASSWORD
                        Password for the student's MyXXX account.
  -n NOTIFY, --notify NOTIFY
                        Enable e-mail notification successful course
                        enrollment.
  -e, --enroll          Enable course enrollment upon class availability.
```

However, `-e` or `--enroll` is a deprecrated flag as it is now the default behavior.

###### Example usage of the command-line arguments:

Start a virtual display server using Xvfb (check below for explanation):

```bash
$ Xvfb -ac :99
```

Then, start Vindicta for direct enrollment to a course when it becomes available, and to continually try if there are errors: 

```bash
$ while true; do DISPLAY=:99 python vindicta.py --browser chrome --executable-path ../drivers/chromedriver --xxx-id 'abc123' --password 'hunter2'; done
```


##### Assumptions

There are a few standard assumptions that Vindicta makes when attempting to
automate the enrollment process:
* The semester you wish to automate the enrollment of is the second semester
listed on the `Select Term` page.
* The time slot that you wish to fill with the classes within your enrollment
cart do not conflict with any existing (enrolled) classes.


##### Headless Motivation

Since I wanted to have Vindicta run headlessly, I needed a way to circumvent
Selenium's necessity to have a valid X11 display to open a browser window
within. This would allow me not only to avoid having a stray Firefox window
open at all times, but also allow me to use have the script be managed over ssh
and have the script run on an entirely different machine.

##### Headless Usage

Firstly, install Xvfb, the tool used to run the Xvfb display server which will
host our headless X11 display (the following will vary by your choice of
distribution and package manager):

* `[sudo] [package-manager] [install] Xvfb`

or

* `[sudo] pacman -S Xvfb`

or

* `[sudo] apt-get install Xvfb`

Then, start the Xvfb server and tell it to host display ":99" (with the -ac flags):

`Xvfb :99 -ac`

Finally, start Vindicta, providing it the display that the Xvfb was started with:

`DISPLAY=:99 python vindicta.py`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

Available for personal-use only. Do not reproduce, re-use, re-purpose, or sell
Vindicta. Contributions may only be made to this repository.
