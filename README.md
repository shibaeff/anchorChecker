Чтобы бот завелся нужен `config.cfg` в той же директории что и сам бот, структура этого файла следующая:
```
[TELEGRAM]
API_TOKEN: <your token here>
```

**Задача**
Надо реализовать бота-проверяльщика для мониторинга состояния Anchor Protocol 
в блокчейне Terra. Протокол - средство для получения пассивного дохода путем предоставлениям криптовалютных 
займов другим участникам. Участие в протоколе - дело рискованное. Поэтому необходимо уметь мониторить:
- ключевую ставку в протоколе
- резервы

Изменения по этим показателям запрашиваются в блокчейне и поступают пользователю в Телеграм-бот.
Это очень удобно, потому что многие пользователи Terra сидят в Телеграме.

**Сторонние Сервисы**
Штука для работы с Telegram API, наша самописная штука на Node.js, которая, 
в свою очередь, работает на Anchor SDK.

**Документация**
https://shibaeff.github.io/anchorBotDocs/

**Интерфейс**

`/help` - хелп по боту.

`/reserve` - включить/выключить уведомления по резерву.

`/apy` - включить/выключить уведомления по ключевой ставке.

***Deploy***

**local, simple:**

1) set your configs to config.cfg (telegram), set global LC_ALL
```
[TELEGRAM]
API_TOKEN = 0xyourToken
[REMOTE]
HOST=0.0.0.0
```
3) run `LC_ALL=ru_RU.UTF8 python3 .` or `python3 .`

**docker-based, local:**
1) set your configs to .env 
```
KEY=5241538
LC_ALL=ru_RU.UTF8
```
2) run `docker-compose up`

**docker-based, remote:**
1) set your configs to .env 
```
KEY=5241538
LC_ALL=ru_RU.UTF8
```
2) run `deploy.sh user@6.6.6.6` - where you want to deploy

***Checkup***
- [x] flake8, pydocstyle: run `doit run_checks`
- [x] tests: 5 tests for functions, located at anchor_binding
- [x] documentation is available here: ; documentation was generated with sphinx (use `doit docs`)
- [x] localization: run `doit compile_run`; before deployment set `LC_ALL` (english is default, ru_RU.UTF8 should be set in env)
- [x] automatization: Dockerfile, docker-compose are available. 
