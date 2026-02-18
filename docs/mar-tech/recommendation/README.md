# Рекомендации конкурентов (Recommendation)
Фича в виде виджета на дашбордах пользователей. Цель — больше аккаунтов → выше тариф.

Стратегии подбора аккаунтов:

1. **Коллаборативная фильтрация** — «с этим часто покупают»; использование предпочтений группы для прогноза.
2. **По категории соцсети** — если аккаунты одной соцсети.
3. **По категории бизнеса (МСБ)** — фильтр по сегменту (региональный/городской/локальный).
4. **Композит (fallback)** — объединение стратегий; при пустом списке — переход к следующей.

Подробнее — [service_rest/v1/README.md](service_rest/v1/README.md), [service_rest/v2/README.md](service_rest/v2/README.md).  
Модуль импорта МСБ (2GIS) — [service_main/README.md](service_main/README.md).

### Структура каталога

```
docs/mar-tech/recommendation/
├── README.md
├── service_rest/           # REST API рекомендаций
│   ├── README.md           # Обзор версий 1.0.0 / 1.1.0
│   ├── v1/                 # 1.0.0 — стратегии 1 и 2
│   │   ├── README.md
│   │   ├── SRS_v1.md
│   │   ├── openapi_v1.yaml
│   │   └── diagramm/
│   │       └── sequence.puml
│   └── v2/                 # 1.1.0 — стратегии 3 и 4
│       ├── README.md
│       ├── SRS_v2.md
│       ├── openapi_v2.yaml
│       └── diagramm/
│           └── sequence.puml
└── service_main/           # Основное приложение (админка, импорт МСБ)
    ├── README.md
    ├── SRS_msb_v1.md
    ├── TDD_msb_v1.md
    └── diagramm/
        └── sequence.puml
```

## Артефакты

| Артефакт | Описание |
|----------|----------|
| **service_rest/v1/README.md** | Обзор REST API 1.0.0 — стратегии 1 и 2. |
| **service_rest/v1/SRS_v1.md** | SRS по фиче «Рекомендации» 1.0.0. |
| **service_rest/v1/openapi_v1.yaml** | OpenAPI 1.0.0: algo=PBUW/CATG. |
| **service_rest/v2/README.md** | Обзор REST API 1.1.0 — стратегии 3 и 4. |
| **service_rest/v2/SRS_v2.md** | Расширение 1.0.0: МСБ, композит. |
| **service_rest/v2/openapi_v2.yaml** | OpenAPI 1.1.0: algo=PBUW/CATG/MSB/COMPOSITE. |
| **service_main/README.md** | Обзор модуля импорта МСБ. |
| **service_main/SRS_msb_v1.md** | SRS импорта 2GIS (CSV) в базу МСБ. |
| **service_main/TDD_msb_v1.md** | Техдизайн импорта МСБ. |
