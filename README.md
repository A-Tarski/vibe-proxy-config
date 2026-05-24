# vibe-proxy-config

Личные конфиги для прокси-клиентов.

## Shadowrocket

[shadowrocket/sr_ru_geo_custom.conf](shadowrocket/sr_ru_geo_custom.conf) — конфиг с разделением трафика:
российские сайты (`.ru`, `.su`, `.рф`, `GEOIP RU`, банки, ip-чекеры) идут напрямую,
всё остальное — через прокси.

### Импорт по raw-URL

```
https://raw.githubusercontent.com/A-Tarski/vibe-proxy-config/main/shadowrocket/sr_ru_geo_custom.conf
```

Shadowrocket → **Config** → **+** → вставить URL → **Download**.
