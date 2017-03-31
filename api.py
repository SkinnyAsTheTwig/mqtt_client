import paho.mqtt.client as mqtt
import ssl
import sqlite3

rc_vals = {
    0:'Connection Accepted',
    1:'Connection Refused - incorrect protocol version',
    2:'Connection Refused - invalid client identifier',
    3:'Connection Refused - server unavailable',
    4:'Connection Refused - bad username or password',
    5:'Connection Refused - not authorised',
} # 6-255 unused in mqtt api

class Logger():
    def __init__(self, filename='mqttdb.sql'):
        self.filename = filename
        self.init_sql = """"""

    


def reinitialise(mqtt_obj, client_id='', clean_session=True, userdata=None):
    return mqtt_obj.reinitialise(client_id, clean_session, userdata)

def tls_set(mqtt_obj, cert_dir_path, pem_cert_path=None, priv_key_path=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None):
    return mqtt_obj.tls_set(ca_certs=cert_dir_path,
                    certfile=pem_cert_path,
                    keyfile=priv_key_path,
                    cert_reqs=cert_reqs,
                    tls_version=tls_version,
                    ciphers=ciphers
                    )

def tls_insecure_set(mqtt_obj, boolean):
    return mqtt_obj.tls_insecure_set(boolean)

def connect(mqtt_obj, host, port, keepalive=60, bind_address=''):
    try:
        mqtt_obj.connect_srv(host, port, keepalive, bind_address)
    except:
        mqtt_obj.connect(host, port, keepalive, bind_address)

def publish(mqtt_obj, topic, payload=None, qos=0, retain=False):
    mqtt_obj.publish(topic, payload, qos, retain)

def set_user_pw(mqtt_obj, username, password=None):
    mqtt_obj.username_pw_set(username, password)

def disconnect(mqtt_obj):
    mqtt_obj.disconnect()

def subscribe(mqtt_obj, topics): # topics (type list): [("topic", qos_int)]
    mqtt_obj.subscribe(topics)

def unsubscribe(mqtt_obj, topic):
    mqtt_obj.unsubscribe(topic)

def set_user_data(mqtt_obj, user_data):
    mqtt_obj.user_data_set(user_data)

class MQTTClient(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        connec_val = rc_vals.get(rc, 'Connection Refused: unknown reason')
        print(rc_vals[rc])

    def on_log(self):
        pass
    
    def on_subscribe(self, client, userdata, mid, granted_ops):
        """
        client:         the client instance for this callback
        userdata:       the private user data as set in Client() or userdata_set()
        mid:            matches the mid variable returned from the corresponding
                        subscribe() call.
        granted_qos:    list of integers that give the QoS level the broker has
                        granted for each of the different subscription requests.
        """
        #subscribe_string = 'Subscribed to '
        #print(subscribe_string)
        pass

    def on_message(self, client, userdata, message):
        """
        client:     the client instance for this callback
        userdata:   the private user data as set in Client() or userdata_set()
        message:    an instance of MQTTMessage.
                    This is a class with members topic, payload, qos, retain.
        """
        mesg_str = 'Message received: \n\tTopic: {topic}\n\tQOS: {qos}\n\tPayload: {payload}'.format(
            topic = message.topic,
            qos = message.qos,
            payload = str(message.payload)
        )
        print(mesg_str)
    
    def on_publish(self, client, userdata, mid):
        """
        client:     the client instance for this callback
        userdata:   the private user data as set in Client() or userdata_set()
        mid:        matches the mid variable returned from the corresponding
                    publish() call, to allow outgoing messages to be tracked.
        """
        publish_str = 'Published msg {id}'.format(mid)
        print(publish_str)

    def on_unsubscribe(self, client, userdata, mid):
        """
        client:     the client instance for this callback
        userdata:   the private user data as set in Client() or userdata_set()
        mid:        matches the mid variable returned from the corresponding
                    unsubscribe() call.
        """
        #unsub_str = 'unsubscribed from '
        #print(unsub_str)
        pass

    def on_disconnect(self, client, userdata, rc):
        """
        client:     the client instance for this callback
        userdata:   the private user data as set in Client() or userdata_set()
        rc:         the disconnection result
                    The rc parameter indicates the disconnection state. If
                    MQTT_ERR_SUCCESS (0), the callback was called in response to
                    a disconnect() call. If any other value the disconnection
                    was unexpected, such as might be caused by a network error.
        """
        connec_val = rc_vals.get(rc, 'Connection Refused: unknown reason')
        print(connec_val)



if __name__ == '__main__':
    newClient = MQTTClient(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
    # if no clientid one is randomly chosen (can be a dupe)
    # clean_session means starting fresh w the server
    # websockets is alternative to tcp
    newClient.loop_start()