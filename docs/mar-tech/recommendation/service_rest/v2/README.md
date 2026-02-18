# REST API рекомендаций 1.1.0

**Зачем:** Расширение 1.0.0 — добавлены стратегии МСБ и композит (fallback).

**Кто:** Пользователь — владелец дашборда.

**Стратегии 1.1.0 (дополнительно к 1.0.0):**
3. **MSB** — по категории бизнеса; требуется база МСБ (импорт 2GIS, [service_main/README.md](../../service_main/README.md))
4. **COMPOSITE** — fallback 1→2→3; при пустом результате переход к следующей стратегии

**API:** `GET /api/v1/account_recommendation` — algo=PBUW | CATG | MSB | COMPOSITE.

**Зависимости:**
- [v1/SRS_v1.md](../v1/SRS_v1.md) — базовые сценарии и FR
- [service_main/SRS_msb_v1.md](../../service_main/SRS_msb_v1.md) — источник данных для стратегии 3

**Документы:**
- [SRS_v2.md](SRS_v2.md) — полные требования 1.1.0
- [openapi_v2.yaml](openapi_v2.yaml) — контракт API
- [diagramm/sequence.puml](diagramm/sequence.puml) — диаграмма (стратегии 3–4)
