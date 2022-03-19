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

**Интерфейс**

`/help` - хелп по боту.

`/reserve` - включить/выключить уведомления по резерву.

`/apy` - включить/выключить уведомления по ключевой ставке.