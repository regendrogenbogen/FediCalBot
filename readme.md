A simple bot that takes any public ical file and toots all events which will take place on the same day or in exactly a week. Needs to be called with command line parameter "soon" for events taking place in 7 days or "today" for todays events.

Uses Mastodon.py for tooting. For it to work you need to register your app on the server you will be tooting on:

```
from mastodon import Mastodon

Mastodon.create_app(
    'FediCalBot',
    api_base_url = 'https://your.server.mastodon',
    to_file = 'pytooter_clientcred.secret'
)
```

Then you can save your credentials so you can log in without putting them in your code:

```
from mastodon import Mastodon

mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
mastodon.log_in(
    'my_login_email@example.com',
    'incrediblygoodpassword',
    to_file = 'pytooter_usercred.secret'
)
```
