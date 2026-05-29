# vibe-proxy-config

Личные конфиги для прокси-клиентов.

## Shadowrocket

[shadowrocket/vibe-config.conf](shadowrocket/vibe-config.conf) — конфиг с разделением трафика:
российские сайты (`.ru`, `.su`, `.рф`, `GEOIP RU`, банки, ip-чекеры) идут напрямую,
всё остальное — через прокси.

### Импорт по raw-URL

```
https://raw.githubusercontent.com/A-Tarski/vibe-proxy-config/main/shadowrocket/vibe-config.conf
```

Shadowrocket → **Config** → **+** → вставить URL → **Download**.

## Happ

[happ/vibe-config.json](happ/vibe-config.json) — routing-профиль для [Happ](https://www.happ.su/).
Та же логика: РУ-трафик (`geosite:category-ru`, `geoip:ru`, whitelist) напрямую,
остальное через прокси.

### Импорт по deeplink

Открыть на iOS/Android/macOS с установленным Happ:

[`happ://routing/onadd/...`](happ/vibe-config.deeplink) — содержимое в [vibe-config.deeplink](happ/vibe-config.deeplink).

Или вручную: **Routing** → **+** → вставить содержимое [vibe-config.json](happ/vibe-config.json) как JSON.

### Geo-базы

Конфиг подгружает geo-файлы от [roscomvpn-geoip](https://github.com/hydraponique/roscomvpn-geoip) и
[roscomvpn-geosite](https://github.com/hydraponique/roscomvpn-geosite) — там есть нужные категории
`category-ru`, `whitelist`. Они автообновляются по ветке `master`.

## AmneziaVPN

Папка [amnezia/](amnezia/) — split-tunneling список основных российских сайтов
(YouGile, маркетплейсы, банки, госуслуги, медиа), чтобы они работали **в обход VPN**.

- [ru-sites-domains.txt](amnezia/ru-sites-domains.txt) — человекочитаемый список доменов по категориям
- [ru-direct.json](amnezia/ru-direct.json) — файл импорта для Amnezia (формат `[{"hostname","ip"}]`)
- [generate_amnezia_list.py](amnezia/generate_amnezia_list.py) — генератор: резолвит домены в IP и пересобирает json
- [ru-direct-mapping.json](amnezia/ru-direct-mapping.json) — отладочный маппинг IP → домены

### Как подключить

1. AmneziaVPN → **Настройки → Раздельное туннелирование (Split Tunneling)** → раздел **Сайты**
2. Выбрать режим **«Все сайты, КРОМЕ указанных здесь»** (всё через VPN, эти — напрямую)
3. Меню (три точки) → **Импорт** → **Заменить список** → выбрать `ru-direct.json`

### ⚠️ Важное ограничение

Amnezia маршрутизирует **только по IP**, не по доменам. У marketplace-ов и CDN
IP-адреса периодически меняются, поэтому список **устаревает** — это особенность
Amnezia, а не ошибка. Когда какой-то сайт перестал ходить напрямую — пересобери список:

```bash
cd amnezia && python3 generate_amnezia_list.py
```

и заново импортируй `ru-direct.json` (режим «Заменить список»).

Для маршрутизации **по доменам** (без этой проблемы) используй Shadowrocket/Happ выше —
там правила `.ru`/`geosite:category-ru` работают по SNI и не требуют обновления IP.
