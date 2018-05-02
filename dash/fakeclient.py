import time
import random

import zmq


URLS = ('/',
        '/items/',
        '/items/{}/',
        '/items/{}/some-detail/',
        '/account/dashboard',
        '/help/',
        '/some-other-items/{}/',
        '/users/{}/stories/{}/')

def random_url():
    url = random.choice(URLS)
    url = url.format(*[random.randint(0,100) for _ in range(url.count('{'))])
    return url

def main():
    random.seed()
    
    context = zmq.Context.instance()
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://127.0.0.1:14541')
    i =0 
    while i < 2000:
        socket.send_json({'t': 'e', 'c':'http_request', 'v' : random_url(), 'd' : random.random() * 5})
        time.sleep(random.random()*0.05)
        i = i + 1
        print (i)

if __name__ == "__main__":
    main()
