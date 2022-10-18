import paho.mqtt.client as mqtt
import threading

_DEBUG=True

class mqtt_subscriber():
    """ Mqtt subscriber to receive a raw rotational speed"""
    def __init__(self, on_message, synchro, topic, broker_addr='localhost'):
        """
        Class constructor

        Parameter:
        ---------
        on_message: callback function
            mqtt callback subscriber to get the value

        synchro: threading.Lock
            to synchronize the end of the client subscriber
        
        broker_addr: string
            broker address (name or IP) in action

        topic: string
            Mqtt topic to be subscribed
        
        """
        self.on_message=on_message
        self.mqttBroker = broker_addr
        self.topic = topic
        # Lock thread synchronization
        self.lock = synchro
        self.lock.acquire()


    def subscribe_connect(self):
        """ client function launched in a thread
        """
        if _DEBUG==True: print("Start mqtt subscriber")
        # Broker connection
        client = mqtt.Client("Console")
        client.connect(self.mqttBroker) 
        # Topics 'fit_and_fun/speed' subscription
        client.loop_start()
        client.subscribe(self.topic)
        client.on_message=self.on_message 
        # Wait for the end
        self.lock.acquire()
        client.loop_stop()
        if _DEBUG==True: print("End mqtt subscriber")
   
    def run(self):
        """ Start the thread """
        self.t1=threading.Thread(target=self.subscribe_connect)
        self.t1.start()

    def stop(self):
        """ Stop the thread """
        self.lock.release()
        self.t1.join()
