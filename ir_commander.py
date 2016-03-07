#!/usr/bin/python3

import socket
import time

if __name__ == '__main__':
    pass

#configure lightwave server settings
LW_UDP_IP = "192.168.0.10"
LW_UDP_PORT = 9760
LW_MSG_START = "666,!"

#some vars
lock_light_changes = False


def print_response(desc):
	print("------------------------")
	print("   " + desc)
	print("------------------------")
	print("")
	return
	
def send_udp(msg, description):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet and UDP
    print_response("Lightwave command: " + description + " - \"" + msg + "\"")
    sock.sendto(msg.encode('utf-8'), (LW_UDP_IP, LW_UDP_PORT))
    return


def send_lightwave_command(acomm,description):
    if lock_light_changes:
        print("Lightwave command ignored, lock is on: " + description)
        return
    msg = LW_MSG_START + acomm
    send_udp(msg,description)
    return
    
def reboot_Pi():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)
    return


#######################################
######## Message handling loop ########
#######################################

aCommand = ""
while aCommand != "0":
    aCommand = input("Command? ")
    if aCommand == "1": 
        send_lightwave_command("R2FmP1","TV Time")
    elif aCommand == "2": 
        send_lightwave_command("R2Fa", "All off")
    elif aCommand == "3":  
        send_lightwave_command("R2FmP3","All on")
    elif aCommand == "4":  
        send_lightwave_command("R2FmP2","Dim room")
    elif aCommand == "5": #low light for pause
    	send_lightwave_command("R2D3FdP2","Main Sofas 5%")
    	time.sleep(0.2)
    	send_lightwave_command("R2D4FdP2","Main Middle 5%")
    elif aCommand == "6":
    	send_lightwave_command("R2D3F0","Main Sofas Off")
    	time.sleep(0.2)
    	send_lightwave_command("R2D4F0","Main Middle Off")
    elif aCommand == "7":
    	lock_light_changes = True
    elif aCommand == "8":
    	lock_light_changes = False
    #elif aCommand == "101":
    	#turn_PS4_On()
    elif aCommand == "999":
    	reboot_Pi()
    elif aCommand == "register_lw": 
        send_lightwave_command("F*p.", "LightwaveRF register command")

print("Finished!")
