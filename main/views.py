from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed

import pika
import redis


def put_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response_data = {}
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='main')
            channel.basic_publish(exchange='', routing_key='main',
                                  body=message)
            connection.close()
        except Exception as e:
            response_data['result'] = '0'
        else:
            response_data['result'] = '1'

        return JsonResponse(response_data)
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


def get_messages(request):
    if request.method == 'GET':
        messages = []
        redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        while True:
            b_message = redis_db.lpop('messages')
            if b_message:
                messages.append(str(b_message, 'utf-8'))
            else:
                break

        return JsonResponse({'messages': messages})
    else:
        HttpResponseNotAllowed(permitted_methods=['GET'])
