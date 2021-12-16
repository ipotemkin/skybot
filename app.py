from slack_bolt import App
from credentials import BOT_TOKEN, SIGNING_SECRET
import ssl as ssl_lib
import certifi
from slack_sdk.web import WebClient

# ssl_lib._create_default_https_context = ssl_lib._create_unverified_context

ssl_lib.create_default_context(cafile=certifi.where())
app = App(
    token=BOT_TOKEN,
    signing_secret=SIGNING_SECRET,
    # client=WebClient(),
    # ssl_check_enabled=False
)


if __name__ == "__main__":
    app.start(port=3000)
    # print(ssl_context)
    # print(certifi.where())
