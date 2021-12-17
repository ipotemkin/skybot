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
    "notify_on_close": True,
    "type": "modal",
    "callback_id": "register_view",
    "title": {"type": "plain_text", "text": "Запись об ошибке"},
    "submit": {"type": "plain_text", "text": "Отправить"},
    "blocks": [
        # {
        #     "type": "section",
        #     "text": {"type": "mrkdwn", "text": "Добавьте или скорректируйте информацию"},
        #     "accessory": {
        #         "type": "button",
        #         "text": {"type": "plain_text", "text": "Click me!"},
        #         "action_id": "button_abc"
        #     }
        # },
        # {
        #     "type": "input",
        #     "block_id": "input_description",
        #     "label": {"type": "plain_text", "text": "Текст сообщения об ошибке"},
        #     "element": {
        #         "type": "plain_text_input",
        #         "action_id": "description_input",
        #         "multiline": False,
        #         "placeholder": {"type": "plain_text", "text": "Добавьте описание ошибки"},
        #     }
        # },
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

priority_view = {
    "type": "input",
    "block_id": "input_priority",
    "label": {"type": "plain_text", "text": "Насколько серьезная проблема?"},
    "element": {
        "type": "plain_text_input",
        "action_id": "priority_input",
        "multiline": False,
        "placeholder": {"type": "plain_text", "text": "Укажите 1-3, где 1 - самый высокий приоритет"},
    }
}

priority_view_new = {
    "type": "section",
    "block_id": "select_priority",
    "text": {
        "type": "mrkdwn",
        "text": "Наколько серьезная проблема?"
    },
    "accessory": {
        "type": "static_select",
        "placeholder": {
            "type": "plain_text",
            "text": " – ",
            "emoji": True
        },
        "options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": "1 - Не дает учиться",
                    "emoji": True
                },
                "value": "1"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "2 - Запутывает или отвлекает",
                    "emoji": True
                },
                "value": "2"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "3 - Мелкая",
                    "emoji": True
                },
                "value": "3"
            }
        ],
        "action_id": "input_priority"
    }
}
