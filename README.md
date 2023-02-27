# sample-service

A sample poc service using Flask which writes data to and reads data from Redis. OTEL tracing has been setup for this sample and it uses ConsoleSpanExporter to export spans to Console. Other OTEL exporters can be used to export to other tools like Zipkin. 

app.py is the entry point which contains two endpoints.
registration.py contains code to interact with Redis. 

This is a sample poc code and is not quality controlled nor much thought / time was put in writing this piece of code. Please treat it as such!!