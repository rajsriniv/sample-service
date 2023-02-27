import redis
import json
import logging
from opentelemetry import trace

registration_counter = 'REGISTRATION_COUNTER'

class Registartion:
    def __init__(self) -> None:
        pass
    
    def register_user(self, data):
        r = redis.Redis()
        logging.info(data)
        registration_key = r.incr(registration_counter)
        key = 'user' + '_' + data['name'] + '_' + str(registration_key)
        data['registration_key'] = registration_key
        result = r.set(key, json.dumps(data))
        logging.info('Result is {0}'.format(result))
        return result
    
    def get_registered_user(self):
        with trace.get_current_span() as span:
            registered_users = []
            r = redis.Redis()
            for key in r.scan_iter('user*'):
                user = r.get(key)
                registered_users.append(json.loads(user.decode("utf-8")))
            if registered_users is None:
                span.set_attribute("status", "no users found")
            else:
                span.set_attribute("status", "users found")
            return registered_users