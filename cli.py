from api import *

prefix = '[ >> ] '
int_prefix = '[ > ] '
truth_kw = ['1','true', 1, 'no']
false_kw = ['0','false', 0, 'no']
help_kw = ['h', 'help']
quit_kw = ['quit', 'q']
create_kw = ['cr','create']
reinit_kw = ['r','reinitialise']
tls_set_kw = ['tls_set']
tls_insecure_set_kw = ['tls_insecure_set']
connect_kw = ['c','connect']
publish_kw = ['p','publish']
set_user_pw_kw = ['set_user_pw']
disconnect_kw = ['d','disconnect']
subscribe_kw = ['s','subscribe']
unsubscribe_kw = ['u','unsubscribe']
set_user_data_kw = ['set_user_data']




Log = Logger()
command = ''
client = ''

def usage():
    helpstring = """
    CLI for interacting with a mqtt server

    h/help:         Show This Message
    q/quit:         Quit Client
    qq:             Quick Quit

    """
    print(helpstring)

def get_user_data():
    data = input(int_prefix + "What is the user data?:\n")
    return eval(data)

def initialize_client():
    return mqtt.Client()

def reinitialise_client(client):
    client_id = input(int_prefix + "Client ID: (blank for random, \\x for hex chars)\n"+ int_prefix)
    clean = input(int_prefix + "Clean Session? (0 for false else true)\n" + int_prefix)
    clean = False if not clean else True
    user_data = get_user_data()
    return reinitialise(client, client_id='', clean, user_data)

def set_tls(client):
    cert_path = input(int_prefix + "Path to tls certs dir?")
    pem_path = input(int_prefix + "Path to public key?")
    priv_path = input(int_prefix + "Path to private key?")
    cert_type = input(int_prefix + "Cert types (blacnk for ssl.CERT_REQUIRED)")
    ver = input(int_prefix + "TLS veriosn? (blank for TLSv1)")
    ciphers = input(int_prefix + "Type of ssl ciphers? (default blank None)")
    return tls_set(client, cert_path, pem_path, priv_path, cert_type, ver, ciphers=None)

def tls_set_insecure(client):
    print(int_prefix + "Do you want to set client tls to insecure?")
    print(int_prefix + "yes:\t1 | true  | no")
    print(int_prefix + "no: \t0 | false | no")
    truth = input(int_prefix)
    if truth in truth_kw:
        return tls_insecure_set(client, True)
    elif truth in false_kw:
        return client
    else:
        print(int_prefix + "Invalid option.")
        return tls_set_insecure(client)

def client_connect(client):
    host = input(int_prefix + 'Enter host address:')
    port = input(int_prefix + "Enter Port:")


############### write inputs logic for below
def client_publish(client):
    topic = input(int_prefix)
    payload = input(int_prefix)
    qos = input(int_prefix)
    retain = input(int_prefix)
    return publish(client, topic, payload, qos, reatain)

def set_pw_user(client):
    username = input(int_prefix)
    password = input(int_prefix)
    return set_user_pw(client, username, password)

# def disconnect_client(client):
#     return disconnect(client)

def client_subscribe(client):
    topics = []
    topic = ''
    while topic not in quit_kw:
        topic = input(int_prefix)
        if topic and topic not in quit_kw:
            qos = input(int_prefix)
            topics.append((topic, qos))
    return subscribe(client, topics)

def client_unsubscribe(client):
    topic = input(int_prefix)
    return unsubscribe(client, topic)

def user_data_set(client):
    user_data = eval(input("Enter duser data:"))
    return set_user_data(client, user_data)


while command not in quit_kw:
    command = input(prefix + "Please enter a command\n").lower()
    if command == 'qq':
        break
    if not client:
        client = initialize_client()
    if command in create_kw:
        client = initialize_client()
    elif command in reinit_kw:
        client = reinitialise_client(client)
    elif command in tls_set_kw:
        client = set_tls(client)
    elif command in tls_insecure_set_kw:
        client = tls_set_insecure(client)
    elif command in connect_kw:
        client = client_connect(client)
    elif command in publish_kw:
        client = client_publish(client)
    elif command in set_user_pw_kw:
        client = set_pw_user(client)
    elif command in disconnect_kw:
        client = disconnect(client)
    elif command in subscribe_kw:
        client = client_subscribe(client)
    elif command in unsubscribe_kw:
        client = client_unsubscribe(client)
    elif command in set_user_data_kw:
        client = user_data_set(client)


except KeyboardInterrupt:
    print("Closing...")
    # close socket
    # remove obj
    print("Closed.")