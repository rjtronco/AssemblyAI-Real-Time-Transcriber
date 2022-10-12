# Assembly AI Real Time Speech to Text Transcriber

### DialogFlow Setup
  - Create agent in DialogFlow
  - Create Custom intent for that agent
  - Add keywords to the training
  - Enable webhook for the custom intent
  - Create Flask App for the Fulfillment of the custom intent
  - Install ngrok in your local
  - run your flask app and ngrok
  - Use the test files to check if your endpoints work correctly
  

Go to `/Speech-to-Text` directory. Run `working_rts.py` in cli, then speak to your mic

Note: `CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio` to install on mac
