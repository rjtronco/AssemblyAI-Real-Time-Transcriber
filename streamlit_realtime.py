import streamlit as st
import websockets
import asyncio
import base64
import json
# from configure import auth_key

import pyaudio

if 'text' not in st.session_state:
	st.session_state['text'] = 'Listening...'
	st.session_state['run'] = False

 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

def start_listening():
	st.session_state['run'] = True

def stop_listening():
	st.session_state['run'] = False


st.title('Get real-time transcription')

start, stop = st.columns(2)
start.button('Start listening', on_click=start_listening)

stop.button('Stop listening', on_click=stop_listening)

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 

async def send_receive():
	
        print(f'Connecting websocket to url ${URL}')

        async with websockets.connect(
            URL,
            extra_headers=(("Authorization", '10103d1330a1429eb01e826aa6fb59e6'),),
            ping_interval=5,
            ping_timeout=20
        ) as _ws:

            r = await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")

            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")


            async def send():
                while st.session_state['run']:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data":str(data)})
                        r = await _ws.send(json_data)

                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break

                    except Exception as e:
                        print(e)
                        assert False, "Not a websocket 4008 error"

                    r = await asyncio.sleep(0.01)


            async def receive():
                while st.session_state['run']:
                    try:
                        result_str = await _ws.recv()
                        vowel = ['a','e','i','o','u']

                        if json.loads(result_str)['message_type']=='FinalTranscript':
                            sentence = json.loads(result_str)['text']
                            print(sentence)
                            split_sentence = sentence.split()
                            return_str = ''
                            punctuation = ''
                            # -- iterate each word , then assess last char
                            print(split_sentence)
                            for index, word in enumerate(split_sentence):
                                print(f"word: {word}, index: {index}, len: {len(split_sentence)}")
                                comma = ""
                                #  if last word in the sentence, get punctuation then process word without the attached punctuation
                                if index == len(split_sentence) - 1 :
                                    punctuation = str(word)[-1]
                                    word = str(word)[0:-1]
                                
                                return_str += " "
                                #if word has comma 
                                if str(word)[-1] == ",":
                                    word = str(word)[0:-1]
                                # if last char of word is vowel or not. Comma var is appended whether it has value or not
                                if str(word)[-1] in vowel:
                                    return_str += str(word) +"-v" +comma
                                else:
                                    return_str += str(word) +"-c"+comma
                            st.session_state['text'] = return_str + "" +punctuation
                            st.markdown(st.session_state['text'])

                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break

                    except Exception as e:
                        print(e)
                        assert False, "Not a websocket 4008 error"
			
            send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())
