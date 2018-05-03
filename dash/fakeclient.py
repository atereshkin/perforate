import time
import random
from threading import Thread

from clientapi import perforate


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

    p = perforate.Perforate()
    p.register_event_class('http_request', 'Http request', is_prolonged=True)
    p.register_event_class('sql_query', 'SQL query', is_prolonged=True)
    p.register_metric('job_queue_length', 'Jobs in queue')

    def emulate_http_reqs():
        for i in range(2000):
            p.emit_http_request(random_url(), random.random() * 5)
            time.sleep(random.random()*0.05)
            i = i + 1
    def emulate_sql_queries():
        for i in range(2000):
            p.emit_sql_query('SELECT username from auth_user where auth_user.id=10', random.random()/2)
            time.sleep(random.random()*0.05)
            i = i + 1

    def emulate_queue_measurements():
        for i in range(100):
            p.record_job_queue_length(random.randint(0,100))
            time.sleep(1)
            i = i + 1
        
            
    ht = Thread(target=emulate_http_reqs, args=())
    st = Thread(target=emulate_sql_queries, args=())
    qt = Thread(target=emulate_queue_measurements, args=())

    ht.start()
    st.start()
    qt.start()
    ht.join()
    st.join()
    qt.join()
    
    

if __name__ == "__main__":
    main()
