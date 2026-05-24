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
