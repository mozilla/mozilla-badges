# Mozilla Badges

Mozilla Badges is a badge service based on [Playdoh][playdoh], a [Django][django ] deriviative. This is currently a new development, but you can find the live [badges.mozilla.org][bmo] code [elsewhere on GitHub][gh-bmo].

[django]: http://www.djangoproject.com/
[playdoh]: https://github.com/mozilla/playdoh
[bmo]: https://badges.mozilla.org
[gh-bmo]: https://github.com/mozilla/badges.mozilla.org


Setup
------

Basic setup instructions:

  git submodule update --init --recursive
  virtualenv --no-site-packages venv
  . ./venv/bin/activate
  pip install -r requirements/compiled.txt
  pip install -r requirements/dev.txt
  cp mozbadges/settings/local.py-dist mozbadges/settings/local.py

Now edit `mozbadges/settings/local.py` and choose a value for `SECRET_KEY`.  Adjust the settings under `DATABASE` as appropriate for your mysql setup.  Uncomment the entry under `HMAC_KEYS` and change the secret as desired.  Uncomment the `SESSION_COOKIE_SECURE` line if you are not using HTTPS.

Create a new mysql schema with a name corresponding to the `NAME` you chose in the `local.py` file.

  ./manage.py syncdb
  * follow prompts to set up a django superuser
  ./manage.py runserver 0.0.0.0:8000

License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

