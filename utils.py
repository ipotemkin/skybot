# channel parsing
import re

# info ---------------------
# профессия_поток_lesson_урок
#
# prof-pd-5_0-flood
# prof-pd-5_0-general
# prof-pd-5_0-high_level
# prof-pd-5_0-hw1
# prof-pd-5_0-lessons
# prof-pd-5_0-professors_team
# prof-pd-course-work_1
# prof-pd-5_0-hw-web-12
#
# required fields
# channel - entire string
# product - the first word after prof, or the second word
# group_id
# lesson_id
# ----------------------------

# examples for testing
s = ""
s1 = "prof-pd-course-work_1"
s2 = "prof-pd-5_0-hw-web-12"
s3 = "prof-pd-5_0-hw-web"


def parse_channel(raw_str: str):
    """
    parses a channel name into product, group_id, lesson_id
    :param raw_str:  a raw channel name
    :return: a dict with product, group_id, lesson_id
    """
    product_obj = re.search(r'-(\S*?)-', raw_str)
    product = product_obj.group(0).strip("-") if product_obj else None

    group_id_obj = re.search(r'-[0-9, _]*-', raw_str)
    group_id = group_id_obj.group(0).strip("-") if group_id_obj else None

    lesson_id_obj = re.search(r'[0-9]*$', raw_str)
    lesson_id = lesson_id_obj.group(0) if lesson_id_obj else None

    return {"product": product, "group_id": group_id, "lesson_id": lesson_id}


def parse_channel_msg(raw_str: str):
    res = parse_channel(raw_str)
    if not res["product"]:
        print("No product")
    if not res["group_id"]:
        print("No group_id")
    if not res["lesson_id"]:
        print("No lesson_id")


if __name__ == "__main__":
    print(s1, parse_channel(s1))
    parse_channel_msg(s1)

    print(s2, parse_channel(s2))
    parse_channel_msg(s2)

    print(s3, parse_channel(s3))
    parse_channel_msg(s3)
