import socket
from typing import List, Tuple, ByteString
from pathlib import Path
from text_to_phone import TextPhone
from pythonosc import udp_client
from time import sleep
from random import random

class Server():

    def __init__(self,pd_ip:str,pd_port:int) -> None:
        self.udp_client = udp_client.SimpleUDPClient(pd_ip,pd_port)
        self.osc_address = "/wav_path"

    def send_audio_grains(self, words_list:List[List[str]]) -> None:
        for word in words_list: 
            for phone_wav_path in word:
                phone_wav_path = Path("..","Dataset","Buckeye","Processed",phone_wav_path)
                try:
                    self.udp_client.send_message(self.osc_address, str(phone_wav_path))
                    sleep(0.166)
                    print(f"Sent {phone_wav_path.name} succesfully!")
                except Exception as e:
                    print(f"ERROR: {e}")
            rand_silence = random()*random() + 1 
            sleep(rand_silence)

"""     def shutdown(self) -> None:
        self.udp_client.close() """

if __name__ == "__main__":
    
    pd_addr = ("127.0.0.1", 13001)
    srv = Server(pd_ip=pd_addr[0], pd_port=pd_addr[1])
    txt_ph = TextPhone("en-us")
    res = txt_ph.granulate("Hello, meet Radu", True)
    print(res)
    srv.send_audio_grains(res)    
 