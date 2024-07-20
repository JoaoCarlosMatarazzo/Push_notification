from flask import request, jsonify
from pywebpush import webpush, WebPushException
from app import app

# Suas chaves VAPID
VAPID_PUBLIC_KEY = app.config['VAPID_PUBLIC_KEY']
VAPID_PRIVATE_KEY = app.config['VAPID_PRIVATE_KEY']

subscriptions = []

@app.route('/subscrib', methods=['POST'])
def subscribe():
    subscription_info = request.json
    subscriptions.append(subscription_info)
    return jsonify({"message": "Inscrição adicionada com sucesso!"}), 201

@app.route('/send_notification', methods=['POST'])
def send_notification():
    notification_info = request.json
    message = notification_info.get('message', 'Olá, mundo!')

    for subscription_info in subscriptions:
        try:
            webpush(
                subscription_info=subscription_info,
                data=message,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": "email:seu-email@dominio.com"}
            )
        except WebPushException as ex:
            print("Me desculpe, mas não posso fazer isso: {}", repr(ex))
            continue

    return jsonify({"message": "Notificação enviada!"}), 200

