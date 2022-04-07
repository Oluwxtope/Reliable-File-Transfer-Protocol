# Reliable File Transfer Protocol  

## How to Run Locally  
1. Open one terminal tab and navigate into the directory with the program files. This will run the receiver.py program  
2. Open another terminal tab and navigate into the directory with the program files. This will run the sender.py program  
3. On the terminal tab running the receiver program, run the receiver: `python3 receiver.py`  
   The receivers input format is as follows: `<UDP port number to receive packet> <drop probability> <name of the received file>`
   > Example: `9994 0.5 received.txt`  
4. On the other terminal tab running the sender program, run the sender: `python3 sender.py`  
   The senders input format is as follows: `<host address of the receiver> <port number to used to send data> <port number to receive ACKs from the receiver> <timeout interval (milliseconds)> <name of the file to send>`  
   > Example: `localhost 9994 9992 50 send.txt`