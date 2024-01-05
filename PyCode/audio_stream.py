import socket
from typing import Tuple, ByteString
from os import path

class Server():

    PD_ADDRESS = ("127.0.0.1", 9001)

    def __init__(self) -> None:
        self.audio_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_server.bind(("127.0.0.1",16809))

    """     
        def accept_income(self):
            client_socket, cl_address = self.audio_server.accept()
            print(f"Contacted:{cl_address}")
            self.client_socket = client_socket
            self.client_address = cl_address 
    """
        
    
    def send_audio(self, wav_filepath:str) -> None:

        with open(wav_filepath, 'rb') as wav_f:
            wav_data = wav_f.read()
        
        self.audio_server.sendto(wav_data, self.PD_ADDRESS)
        print(f"Sent {path.basename(wav_filepath)} succesfully!")

    def shutdown(self) -> None:
        self.audio_server.close()