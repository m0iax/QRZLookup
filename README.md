# QRZLookup
QRZ Lookup for JS8Call 2.2


This app is designed to work with JS8Call Version 2.2. http://js8call.com

THis app listens to the UDP API of JS8Call 2.2 and when a callsign is selected in Js8Call 2.2 it will perform a Lookup on QRZ.com and display the operators details.
A username and password for QRZ.com is required for this to work.

This app also listens to the UDP output from JS8Call and will automatically upload log ADIF entries to QRZ.com and/or eQSL.cc when the user logs a QSO in JS8Call.

<strong>PLEASE NOTE THIS APP IS IN DEVELOPMENT AND SUPBJECT TO CHANGE AT ANY TIME. it is released for those who are happy to test it</strong>
the funal version will change to use the TCP API and any other enhancements I can add.
<br>
It will run on any OS that will run python.

Prerequiesites:

JS8Call
python 3.7 or later
an account on QRZ.com with a valid APIKEY*
a User name and password for eQSL.cc*
*and account for either QRZ.com or eQSL.cc is required. you dont need both but it will work with both

Install:

clone or download this repo if downlading a .zip file unzip into a directory on your computer.

Install Pythin modules:

<strong>Linux:</strong>
<br>
pip3 install xmltodict<br>
pip3 install requests
<br>
<strong>windows:</strong>
<br>
py -m pip install xmltodict<br>
py -m pip install requests
<br>
Linux (including Ras
pberry Pi) and MacOS

run a command prompt, change directory to the installation directory.

cd QRZLookup
(before running for the fisr time enter the following command:)
chmod +x QRZLookup.py<br>


to run the app: <strong>./QRZLookup.py</strong>

Windows from the command prompt

cd QRZLookup

(before running for the first time install the prerequisite modules)
py -m pip install requests

py -m QRZLookup.py



The first time you run the app it will create two files in the installation directory

js8call.cfg
loguploader.cfg

js8call.cfg has the UDP port number to listen on, it uses the JS8Call default of 2242. You only need to change this if you have changed it in the JS8Call settings.

To set up the loguploader open the file loguploader.cfg in a text editor, the contents will look like this:

[QRZ.COM]
apikey = APIKEY

[EQSL.CC]
username = USERNAME
password = PASSWORD
qthnickname =

[SERVICES-AT-STARTUP]
eqsl = 0
qrz = 0
clublog = 0
hrdlog = 0
qrzlookup = 1

[SERVICES-INUSE]
eqsl = 1
qrz = 1
clublog = 0
hrdlog = 0
qrzlookup = 1

Do not change the format of the file, but update the values APIKEY, USERNAME, PASSWORD with your details, for example

[QRZ.COM]
apikey = ABCD-EFGH

[EQSL.CC]
username = MyUserName
password = MyPassword
qthnickname = MyNickname

[SERVICES-AT-STARTUP]
eqsl = 0
qrz = 0
clublog = 0
hrdlog = 0
qrzlookup = 1

[SERVICES-INUSE]
eqsl = 1
qrz = 1
clublog = 0
hrdlog = 0
qrzlookup = 1

Note if you do not use one or the other then you do not need to change the default setting for it. In the services section you can specify which ones you want enabled at startup change the 0 to a 1 if you want is enabled by default when you run the app, leave them at 0 and you will just need to click the button after running.
NOTE FOR USERS UPDATING TO VERSION SUPPORTING QTH NICKNAME

You will either need to delete the exsiting file and run the app again to re-create it, or manually add the qthnickname setting

If you do not use the QTH Nickname in eQSL then just leave it blank

Once you have updated the settings file, close the app and run it again to pick up the new settings values. Click on the buttons to enable or disable auto upload, the button will be red or green to indicate disabled or enbled. If you run from a command prompt or terminal window you will see upload error messages if the upload fails, if it is sucessful you will not see a message after upload.

Future Enhancements Will include

Upload Status messages to be shown on the UI
Offline Mode - collect ADIF for upload when back online
I
f you have any feature requests please get in touch http://m0iax.com/findme

73 Mark M0IAX
