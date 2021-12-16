from slack_bolt import App
from credentials import BOT_TOKEN, SIGNING_SECRET, SLACK_APP_TOKEN
import ssl as ssl_lib
import certifi
from slack_sdk.web import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils import parse_channel
import re
from gd_utils import FeedbackItem

add_error_msg = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Да"
                    },
                    "style": "primary",
                    "value": "click_me_123",
                    "action_id": "button_yes"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Нет"
                    },
                    "style": "danger",
                    "value": "click_me_123",
                    "action_id": "button_no"
                }
            ]
        }
    ]
}

add_error_msg_2 = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
            }
        },
        # {
        #     "type": "actions",
        #     "elements": [
        #         {
        #             "type": "button",
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "Да"
        #             },
        #             "style": "primary",
        #             "value": "click_me_123",
        #             "action_id": "button_yes"
        #         },
        #         {
        #             "type": "button",
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "Нет"
        #             },
        #             "style": "danger",
        #             "value": "click_me_123",
        #             "action_id": "button_no"
        #         }
        #     ]
        # }
    ]
}


msg_add_priority = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Готов передать сообщение команде проекта! Насколько серьезная проблема?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Не дает учиться"
                    },
                    # "style": "primary",
                    "value": "click_me_123",
                    "action_id": "button_priority_1"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Запутывает или отвлекает"
                    },
                    # "style": "danger",
                    "value": "click_me_123",
                    "action_id": "button_priority_2"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Мелкая"
                    },
                    # "style": "danger",
                    "value": "click_me_123",
                    "action_id": "button_priority_3"
                }
            ]
        }
    ]
}


blocks_template = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ""
        }
    },
]

register_view = {
    "type": "modal",
    "callback_id": "view_1",
    "title": {"type": "plain_text", "text": "Запись об ошибке"},
    "submit": {"type": "plain_text", "text": "Отправить"},
    "blocks": [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Добавьте или скорректируйте информацию"},
            # "accessory": {
            #     "type": "button",
            #     "text": {"type": "plain_text", "text": "Click me!"},
            #     "action_id": "button_abc"
            # }
        },
        {
            "type": "input",
            "block_id": "input_description",
            "label": {"type": "plain_text", "text": "Текст сообщения об ошибке"},
            "element": {
                "type": "plain_text_input",
                "action_id": "description_input",
                "multiline": False,
                "placeholder": {"type": "plain_text", "text": "Добавьте описание ошибки"},
            }
        },
        # {
        #     "type": "input",
        #     "block_id": "input_product",
        #     "label": {"type": "plain_text", "text": "Профессия"},
        #     "element": {
        #         "type": "plain_text_input",
        #         "action_id": "product_input",
        #         "multiline": False,
        #         "placeholder": {"type": "plain_text", "text": "Укажите профессию"},
        #     }
        # },
        # {
        #     "type": "input",
        #     "block_id": "input_group_id",
        #     "label": {"type": "plain_text", "text": "Номер потока"},
        #     "element": {
        #         "type": "plain_text_input",
        #         "action_id": "group_id_input",
        #         "multiline": False,
        #         "placeholder": {"type": "plain_text", "text": "Укажите номер потока"},
        #     }
        # },
        # {
        #     "type": "input",
        #     "block_id": "input_lesson_id",
        #     "label": {"type": "plain_text", "text": "Номер урока"},
        #     "element": {
        #         "type": "plain_text_input",
        #         "action_id": "lesson_id_input",
        #         "multiline": False,
        #         "placeholder": {"type": "plain_text", "text": "Укажите номер урока"},
        #     }
        # },
    ]
}

product_view = {
    "type": "input",
    "block_id": "input_product",
    "label": {"type": "plain_text", "text": "Профессия"},
    "element": {
        "type": "plain_text_input",
        "action_id": "product_input",
        "multiline": False,
        "placeholder": {"type": "plain_text", "text": "Укажите профессию"},
    }
}

group_id_view = {
    "type": "input",
    "block_id": "input_group_id",
    "label": {"type": "plain_text", "text": "Номер потока"},
    "element": {
        "type": "plain_text_input",
        "action_id": "group_id_input",
        "multiline": False,
        "placeholder": {"type": "plain_text", "text": "Укажите номер потока"},
    }
}

lesson_id_view = {
    "type": "input",
    "block_id": "input_lesson_id",
    "label": {"type": "plain_text", "text": "Номер урока"},
    "element": {
        "type": "plain_text_input",
        "action_id": "lesson_id_input",
        "multiline": False,
        "placeholder": {"type": "plain_text", "text": "Укажите номер урока"},
    }
}

FEEDBACK = FeedbackItem()


# ssl_lib._create_default_https_context = ssl_lib._create_unverified_context

ssl_lib.create_default_context(cafile=certifi.where())
app = App(
    token=BOT_TOKEN,
    # signing_secret=SIGNING_SECRET,
    # client=WebClient(),
    # ssl_check_enabled=False
)


def kill_buttons(body, client):
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
    conv_info = client.conversations_info(channel=channel_id)
    return conv_info['channel']['name']


@app.message("hello")
def message_hello(message, say):
    print("Прочитал сообщение hello")
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


# @app.message("ошибка")
# @app.message("Ошибка")
# def message_error(message, say):
@app.message(re.compile("([О,о]шибк*)"))
@app.message(re.compile("([О,о]шибочк*)"))
@app.message(re.compile("([О,о]шипк*)"))  # if a user made a typing error
@app.message(re.compile("([О,о]печатк*)"))
def message_error(context, say, message, body, client):
    msg = context['matches'][0]

    # for debug
    print("Прочитал сообщение со словом ошибка")
    print("body:", body)
    print("message", message)

    # conv_info = client.conversations_info(channel=message['channel'])
    # channel_full_name = conv_info['channel']['name']
    # print(conv_info)

    # channel = body['channel_name']
    # user_name = body['user_name']
    # text = body['text']
    # channel_d = parse_channel(channel)

    channel_id = message['channel']
    user_id = message['user']
    text = message['text']
    channel_full_name = get_channel_name(channel_id, client)

    channel_d = parse_channel(channel_full_name)

    global FEEDBACK
    FEEDBACK.clear()
    FEEDBACK = FeedbackItem(
        channel=channel_full_name,
        product=channel_d["product"],
        group_id=channel_d["group_id"],
        reporter=message['user'],
        content=message['text'],
        lesson_id=channel_d['lesson_id']
    )

    noticed_error_msg = f"Привет, <@{message['user']}>! Я бот регистрации ошибок.\n" \
                        f"Хотите зарегистрировать сообщение об ошибке?\n" \
                        f"Триггер: {msg}\n" \
                        f"Ваше сообщение: {message['text']}\n" \
                        f"User_id: {user_id}\n" \
                        f"Channel_id: {channel_id}\n"\
                        f"Текст сообщения об ошибке: {text}\n" \
                        f"Распаковка канала: {channel_d}"

    add_error_msg["blocks"][0]["text"]["text"] = noticed_error_msg

    res = say(
        blocks=add_error_msg["blocks"],
        test="My Text"
    )

    print(res)

    # say(f"Привет, <@{message['user']}>! Я бот регистрации ошибок."
    #     f" Хотите зарегистрировать сообщение об ошибке?"
    #     f" Триггер: {msg}"
    #     f" Ваше сообщение: {message['text']}"
    #     )


@app.action("button_yes")
def handle_yes_to_error_register(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    if FEEDBACK.is_ready():
        # say("Отлично. Тогда мне от Вас нужные еще некоторые детали")
        say(blocks=msg_add_priority['blocks'])
    else:
        say("Отлично. Тогда мне от Вас нужные еще некоторые детали")
        if FEEDBACK.content:
            register_view['blocks'][1]['element']['placeholder']['text'] = FEEDBACK.content

        if not FEEDBACK.product:
            register_view['blocks'].append(product_view)

        if not FEEDBACK.group_id:
            register_view['blocks'].append(group_id_view)

        if not FEEDBACK.lesson_id:
            register_view['blocks'].append(lesson_id_view)



        # product_plh = "Укажите профессию"
        # lesson_id_plh = "Укажите номер урока"
        # group_id_plh = "Укажите номер потока"
        # if not FEEDBACK.lesson_id:
        #     say("Укажите номер урока")

        client.views_open(
            # Pass a valid trigger_id within 3 seconds of receiving it
            trigger_id=body["trigger_id"],
            # View payload
            view=register_view
        )

    logger.info(body)


@app.action("button_no")
def handle_no_to_error_register(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    say("Я Вас понял. Извините за беспокойство")
    logger.info(body)


@app.action("button_priority_1")
def handle_yes_to_error_register(ack, body, logger, say, client):
    ack()
    kill_buttons(body, client)
    say("Вы уверены?")
    # say(blocks=msg_add_priority['blocks'])
    logger.info(body)


@app.event({'type': 'message', 'subtype': 'message_changed'})
def handle_message_events(body, logger, say):
    # say("Message changed")
    logger.info(body)


@app.event({'type': 'message', 'subtype': 'message_deleted'})
def handle_message_events(body, logger, say):
    # say("Message deleted")
    logger.info(body)


# @app.event({'type': 'event_callback', 'event': {'type': 'message'}})
# def handle_message_events(body, logger, say, message):
#     print(message)
#     # say("Message deleted")
#     logger.info(body)


@app.command("/ошибка")
def handle_some_command(ack, body, logger, say):
    ack()
    print(body)
    channel = body['channel_name']
    user_name = body['user_name']
    text = body['text']
    channel_d = parse_channel(channel)
    say(f"reporter: @{user_name}, text: {text}, {channel_d}")
    logger.info(body)


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
    # app.start(port=3000)
    # print(ssl_context)
    # print(certifi.where())
