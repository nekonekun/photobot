pybabel extract --input-dirs=src/photobot/tg -o src/photobot/tg/locales/messages.pot
pybabel update -d src/photobot/tg/locales -D messages -i src/photobot/tg/locales/messages.pot
