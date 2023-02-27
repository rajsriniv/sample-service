from flask import Flask, request
from registration import Registartion
import json
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor,
)
from opentelemetry.semconv.trace import SpanAttributes


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return '{"status": "UP"}'

@app.route('/users/register', methods=['POST', 'GET'])
def register_users():
    with tracer.start_as_current_span("register_user") as span:
        registration = Registartion()
        span.set_attribute(SpanAttributes.HTTP_URL, "/users/register")
        span.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
        if request.method == 'GET':
            registered_users = registration.get_registered_user()
            logging.info(registered_users)
            result = json.dumps(registered_users)
            return result
        data = request.get_json()
        logging.info('Sent data {0}'.format(data['name']))
        result = registration.register_user(data)
        logging.info(result)
        if result:
            return '{"status": "added"}'
        else:
            return '{"status": "failed"}'
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
    