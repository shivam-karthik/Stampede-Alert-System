import conf, json, time, math, statistics
from boltiot import Sms, Bolt


mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
people = 0

length = int(input('lengthOfPlace'));
width = int(input('widthOfPlace'));
area = length * width;
bound = area/5;

while True:
  
    #Read input and determine number of people entering in the room
    response1 = mybolt.digitalRead('0') #IR sensor for entry door
    print(response1)
    data = json.loads(response1)
    if data['value'] == "0" :
        people = people + 1
        print('added')
    #Read input and determine number of people existing in the room
    response2 = mybolt.digitalRead('1') #TR sensor for exit door
    print(response2)
    data = json.loads(response2)
    if data['value'] == "0" :
        people = people - 1
    if people < 0:
        people = 0
    #Take action on crowd data
    print(people)

    try:
        if people  > bound :
            print ("The crowd level increased suddenly. Sending an SMS.")
            response = sms.send_sms("Overcrowded Situation")
            print("This is the response ",response)
            mybolt.digitalWrite('4','HIGH')
        else:
            mybolt.digitalWrite('4','LOW')
        time.sleep(1)

    except Exception as e:
        print("Something went wrong: ",e)
        print("Restarting Bolt...")
        response = mybolt.restart()
