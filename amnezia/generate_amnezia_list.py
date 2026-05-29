#!/usr/bin/env python3
"""Генератор split-tunneling списка для AmneziaVPN.

Читает ru-sites-domains.txt, резолвит каждый домен в IPv4 через DNS-over-HTTPS
(dns.google) и собирает ru-direct.json в формате, который понимает импорт Amnezia:

    [{"hostname": "<ip>", "ip": "<ip>"}, ...]

Почему ключ = IP, а не домен:
  Импорт Amnezia складывает записи в map по полю hostname, поэтому на один
  домен выживает только один IP. Чтобы сохранить ВСЕ адреса сайта, ключом
  делаем сам IP (он же используется для маршрутизации).

Зачем DoH, а не socket.gethostbyname:
  Локальный DNS в РФ/через прокси может отдавать fake-IP или отравленные ответы.
  dns.google резолвит честно.

Запуск:
    python3 generate_amnezia_list.py
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

DOMAINS_FILE = Path(__file__).parent / "ru-sites-domains.txt"
OUTPUT_FILE = Path(__file__).parent / "ru-direct.json"
MAPPING_FILE = Path(__file__).parent / "ru-direct-mapping.json"
DOH_URL = "https://dns.google/resolve?name={name}&type=A"
TIMEOUT = 12


def read_domains(path: Path) -> list[str]:
    domains = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        domains.append(line)
    return domains


def resolve(domain: str) -> list[str]:
    """Вернуть список IPv4 для домена через DoH. Пустой список при ошибке."""
    url = DOH_URL.format(name=domain)
    req = urllib.request.Request(url, headers={"accept": "application/dns-json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
    except Exception as exc:  # noqa: BLE001 - сетевые ошибки логируем и продолжаем
        print(f"  ! {domain}: {exc}", file=sys.stderr)
        return []
    # type 1 == A-запись (IPv4)
    return [a["data"] for a in data.get("Answer", []) if a.get("type") == 1]


def main() -> int:
    domains = read_domains(DOMAINS_FILE)
    print(f"Резолвлю {len(domains)} доменов через {DOH_URL.split('?')[0]} ...")

    ip_to_domains: dict[str, set[str]] = {}
    for domain in domains:
        ips = resolve(domain)
        if not ips:
            print(f"  - {domain}: нет A-записей (пропущен)")
            continue
        for ip in ips:
            ip_to_domains.setdefault(ip, set()).add(domain)
        print(f"  + {domain}: {', '.join(ips)}")
        time.sleep(0.05)  # лёгкий троттлинг, чтобы не долбить DoH

    # Файл импорта Amnezia: ключ = IP (гарантирует уникальность и маршрутизацию)
    entries = [{"hostname": ip, "ip": ip} for ip in sorted(ip_to_domains)]
    OUTPUT_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Человекочитаемый маппинг IP -> какие домены его дали (для отладки)
    mapping = {ip: sorted(d) for ip, d in sorted(ip_to_domains.items())}
    MAPPING_FILE.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\nГотово: {len(entries)} уникальных IP -> {OUTPUT_FILE.name}")
    print(f"Маппинг IP->домены -> {MAPPING_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
