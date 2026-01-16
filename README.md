Library installation compatible versions:
-- Python 3.12.7
-- pip 24.2
-- lk version 2.12.9


Requirements:

Install Python (https://www.python.org/downloads/release/python-3127/)

Install pip (https://pypi.org/project/pip/24.2/)

Install livekit cli(https://docs.livekit.io/intro/basics/cli/start/): 
	linux command: <curl -sSL https://get.livekit.io/cli | bash>
	windows command prompt: <winget install LiveKit.LiveKitCLI>

Create a project on livekit cloud:
  - https://cloud.livekit.io/
  - Go to settings--project to see livekit url, SIP URI of your project(used later for setup) 

Setup twilio login here: https://www.twilio.com/login
Follow steps 1 and 2 to setup twilio(alternatively explore https://docs.livekit.io/telephony/accepting-calls/inbound-twilio/ for more options)

Step 1. Purchase a phone number from Twilio
If you don't already have a phone number, see How to Search for and Buy a Twilio Phone Number From Console.

Step 2. Set up a TwiML Bin
Other approaches
This guide uses TwiML Bins, but you can also return TwiML via another mechanism, such as a webhook.

TwiML Bins are a simple way to test TwiML responses. Use a TwiML Bin to redirect an inbound call to LiveKit.

To create a TwiML Bin, follow these steps:

Navigate to your TwiML Bins page.
(create sip username and password and replace that in the lines below where necessary and remember the credentials for later)
(use the number you just bought on twilio for <your_phone_number> and replace string after @ with your SIP URI as seen on your livekit project)
Create a TwiML Bin and add the following contents:

<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial>
    <Sip username="<sip_trunk_username>" password="<sip_trunk_password>">
      sip:<your_phone_number>@565794gcn13.sip.livekit.cloud
    </Sip>
  </Dial>
</Response>


Go to your Livekit cloud project for SIP trunk setup as following:
	SIP trunk setup:
	   - https://docs.livekit.io/telephony/start/sip-trunk-setup/

pip install -r requirements.txt

Edit file .env.local to fill all the details for livekit and LLM API Keys

python agent download-files

python agent start
