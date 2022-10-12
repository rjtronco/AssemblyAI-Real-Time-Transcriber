#  Assembly AI Real Time Speech to Text Transcriber

Reference: 

- https://www.assemblyai.com/docs/
- https://www.assemblyai.com/

## Highlights

🍭 Creating a real-time speech to text transcriber
- Utilize Assembly AI's real-time transcriber
- Create python file that uses this tool
- Integrate a WebUI to the python endpoint


packages to install:
  - streamlit
  - portaudio
  - pyaudio
  - websockets
  


## How it works

Utilize an asyncio function. This enables the endpoint to simultaneously send and receive data from and to Assembly AI realtime transcriber
```python
send_result, receive_result = await asyncio.gather(send(), receive())
```

Make use of websockets. This is just a snippet, please see whole file.
```python
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
async def send_receive():

    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(URL,extra_headers=(("Authorization", '<YOUR AUTH KEY>'),),ping_interval=5,ping_timeout=20) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")
```
 
 ### TESTING
  
CLI

Run `working_rts.py` in cli, then speak to your mic

[<img src="https://github.com/rjtronco/AssemblyAI-Real-Time-Transcriber/blob/main/rts_cli.png" width="800px" margin-left="-5px">]
<br>



WebUI

Run `streamlit run streamlit_realtime.py`

[<img src="https://github.com/rjtronco/AssemblyAI-Real-Time-Transcriber/blob/main/rts_webUI.png" width="800px" margin-left="-5px">]
<br>



Note: `CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio` to install on mac
