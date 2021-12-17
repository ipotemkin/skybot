from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils import parse_channel, extract_source
import re
from gd_utils import FeedbackItem, FeedbackDAO
from datetime import datetime
from views import add_error_msg, blocks_template, msg_add_priority
from views import register_view, product_view, group_id_view, priority_view, lesson_id_view
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# an object to write feedback data to a google sheets table
report_table = FeedbackDAO(os.getenv("MY_TABLE_URL"))

# a register of feedback and other data of actual conversations with the bot
feedback_data = {}

app = App(token=os.getenv('BOT_TOKEN'))


def kill_buttons(body, client):
    """
    updates a message removing buttons
    """
    # new_blocks = body['message']['blocks'][0]
    blocks_text = body['message']['blocks'][0]['text']['text']
    # print(blocks_text)
    blocks_template[0]['text']['text'] = blocks_text
    # print(new_blocks)
    # del new_blocks['block_id']
    client.chat_update(
        channel=body['container']['channel_id'],
        ts=body['container']['message_ts'],
        # blocks=add_error_msg_2['blocks']
        # blocks=new_blocks
        blocks=blocks_template
    )


def get_channel_name(channel_id, client):
    """
    returns a channel name with given ID
    """
    conv_info = client.conversations_info(channel=channel_id)
    return conv_info['channel']['name']


def get_user_name(user_id, client):
    """
    returns a user name with given ID
    """
    user_info = client.users_info(user=user_id)
    # print(user_info)
    return user_info['user']['name']


def create_feedback_msg(current_feedback: FeedbackItem) -> str:
    """
    makes a template message
    """
    msg = f"Запись:\n" \
        f"date: {current_feedback.date}\n" \
        f"priority: {current_feedback.priority}\n" \
        f"channel: {current_feedback.channel}\n" \
        f"product: {current_feedback.product}\n" \
        f"group_id: {current_feedback.group_id}\n" \
        f"lesson_id: {current_feedback.lesson_id}\n" \
        f"reporter: {current_feedback.reporter}\n" \
        f"content: {current_feedback.content}\n" \
        f"source: {current_feedback.source}"
    return msg


# entry point one !
@app.message(re.compile("([О,о]шибк*)"))
@app.message(re.compile("([О,о]шибочк*)"))
@app.message(re.compile("([О,о]шипк*)"))  # if a user made a typing error
@app.message(re.compile("([О,о]печатк*)"))
def message_error(context, say, message, body, client):
    """
    launches the bot when some patterns found in a user message
    """
    # msg = context['matches'][0]

    # for debug
    # print("Прочитал сообщение со словом ошибка")
    # print("message_error:body:", body)
    # print("message_error:message:", message)

    channel_id = message['channel']
    user_id = message['user']
    # text = message['text']
    user_name = get_user_name(user_id, client)
    channel_full_name = get_channel_name(channel_id, client)
    channel_d = parse_channel(channel_full_name)

    noticed_error_msg = f"Привет, <@{message['user']}>! Я бот регистрации ошибок.\n" \
                        f"Хотите зарегистрировать сообщение об ошибке?\n"
                        # f"Триггер: {msg}\n" \
                        # f"Ваше сообщение: {message['text']}\n" \
                        # f"User_id: {user_id}\n" \
                        # f"Channel_id: {channel_id}\n"\
                        # f"Текст сообщения об ошибке: {text}\n" \
                        # f"Распаковка канала: {channel_d}"

    add_error_msg["blocks"][0]["text"]["text"] = noticed_error_msg

    res = say(
        blocks=add_error_msg["blocks"],
        test="My Text"
    )
    feedback_data[res['ts']] = FeedbackItem(
        channel=channel_full_name,
        product=channel_d["product"],
        group_id=channel_d["group_id"],
        reporter=user_name,
        content=message['text'],
        lesson_id=channel_d['lesson_id'],
        channel_id=channel_id,
        date=datetime.strftime(datetime.today(), "%d.%m.%Y"),
        source=extract_source(message['text'])
    )

    # for debug
    # print(res)
    # print(feedback_data)


@app.action("button_yes")
def handle_yes_to_error_register(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)

    # print("handle_yes_to_error_register:body", body)
    # print("handle_yes_to_error_register:logger", logger)

    current_feedback = feedback_data[body['container']['message_ts']]

    if current_feedback.is_ready():
        res = say(blocks=msg_add_priority['blocks'])
        feedback_data[res['ts']] = current_feedback

    else:
        res = say("Отлично. Тогда мне от Вас нужные еще некоторые детали")
        # if FEEDBACK.content:
        #     register_view['blocks'][1]['element']['placeholder']['text'] = FEEDBACK.content

        if not current_feedback.product:
            register_view['blocks'].append(product_view)

        if not current_feedback.group_id:
            register_view['blocks'].append(group_id_view)

        if not current_feedback.lesson_id:
            register_view['blocks'].append(lesson_id_view)

        register_view['blocks'].append(priority_view)

        res = client.views_open(
            # Pass a valid trigger_id within 3 seconds of receiving it
            trigger_id=body["trigger_id"],
            # View payload
            view=register_view
        )
        del register_view['blocks'][0:6]
        feedback_data[res['view']['id']] = current_feedback

    # print(res)
    # обновляем код у записи результата, чтобы не потерять разговор
    del feedback_data[body['container']['message_ts']]
    # print(feedback_data)

    logger.info(body)


@app.view("register_view")
def handle_submission(ack, body, client, view, logger, say):
    ack()
    # print("handle_submission:body", body)
    # print("handle_submission:view", view)

    current_feedback = feedback_data[view['id']]

    if not current_feedback.product:
        current_feedback.product = view['state']['values']["input_product"]["product_input"]['value']

    if not current_feedback.group_id:
        current_feedback.group_id = view['state']['values']["input_group_id"]["group_id_input"]['value']

    if not current_feedback.lesson_id:
        current_feedback.lesson_id = view['state']['values']["input_lesson_id"]["lesson_id_input"]['value']

    # print(view)
    # print(view['state']['values'])

    # current_feedback.priority = view['state']['values']["input_priority"]["priority_input"]['value']
    current_feedback.priority = view['state']['values']['select_priority']['input_priority']["selected_option"]['value']

    # say(create_feedback_msg(current_feedback), channel=current_feedback.channel_id)
    say("Сообщение об ошибке записано, спасибо!", channel=current_feedback.channel_id)
    report_table.create(current_feedback)

    del feedback_data[view['id']]
    # print(feedback_data)

    # try:
    #     client.chat_postMessage(channel=body["user"]['id'], text=msg)
    #     logger.info(body)
    # except Exception as e:
    #     logger.exception(f"Failed to post a message {e}")
    logger.info(body)


@app.view({'type': 'view_closed', 'callback_id': 'register_view'})
def handle_view_closed(ack, body, client, view, logger, say):
    ack()
    current_feedback = feedback_data[view['id']]
    say(
        "Вы не нажали на кнопку *Отправить*. Данные об ошибке не будут сохранены.\n"
        "Если Вы все-же хотите зарегистрировать ошибку, напишите новое сообщение об ошибке"
        " (должно содержать слово *ошибка* или *опечатка*).\nИли наберите команду */ошибка*",
        channel=current_feedback.channel_id
    )
    del feedback_data[view['id']]
    # print(feedback_data)
    logger.info(body)


@app.action("button_no")
def handle_no_to_error_register(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    say("Я Вас понял. Извините за беспокойство")
    del feedback_data[body['container']['message_ts']]
    # print(feedback_data) # debug
    logger.info(body)


def handle_button_priority(body, say, priority):
    current_feedback = feedback_data[body['container']['message_ts']]
    current_feedback.priority = priority
    # print(body)
    # say(create_feedback_msg(current_feedback))
    say("Сообщение об ошибке записано, спасибо!", channel=current_feedback.channel_id)
    report_table.create(current_feedback)

    del feedback_data[body['container']['message_ts']]
    # print(feedback_data)
    # say(blocks=msg_add_priority['blocks'])


@app.action("button_priority_1")
def handle_button_priority_1(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    handle_button_priority(body, say, 1)
    logger.info(body)


@app.action("button_priority_2")
def handle_button_priority_1(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    handle_button_priority(body, say, 2)
    logger.info(body)


@app.action("button_priority_3")
def handle_button_priority_1(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    handle_button_priority(body, say, 3)
    logger.info(body)


@app.event({'type': 'message', 'subtype': 'message_changed'})
def handle_message_events(body, logger, say):
    # say("Message changed")
    logger.info(body)


@app.event({'type': 'message', 'subtype': 'message_deleted'})
def handle_message_events(body, logger, say):
    # say("Message deleted")
    logger.info(body)


@app.command("/ошибка")
def handle_some_command(ack, body, logger, say):
    ack()
    channel_full_name = body['channel_name']
    channel_id = body['channel_id']
    user_name = body['user_name']
    text = body['text']
    channel_d = parse_channel(channel_full_name)

    noticed_error_msg = f"Хотите зарегистрировать сообщение об ошибке?"
    add_error_msg["blocks"][0]["text"]["text"] = noticed_error_msg
    res = say(
        blocks=add_error_msg["blocks"],
        test="My Text"
    )
    feedback_data[res['ts']] = FeedbackItem(
        channel=channel_full_name,
        product=channel_d["product"],
        group_id=channel_d["group_id"],
        reporter=user_name,
        content=text,
        lesson_id=channel_d['lesson_id'],
        channel_id=channel_id,
        date=datetime.strftime(datetime.today(), "%d.%m.%Y"),
        source=extract_source(text)
    )
    logger.info(body)


@app.action("input_priority")
def handle_input_priority_action(ack, body, view, logger):
    ack()
    # print("body:", body)
    # print("view:", view)
    logger.info(body)


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()
