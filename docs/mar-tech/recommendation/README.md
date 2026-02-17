# Mar-Tech

MarTech-продукт для мониторинга соцсетей: рекомендации конкурентов, интеграции с платёжными системами и 1С.

# Интеграции в проекте

## Платежи

- **1С** — счета на оплату для юр. лиц (создание, оплата, state machine)
- **Stripe** (USD)
- **CloudPayments** (RUB/KZT)

## Фичи
- **Recommendation** — (фича) рекомендации конкурентов


## Рекомендации конкурентов (Recommendation)
Фича в виде виджета на дашбордах пользователей. Цель — больше аккаунтов → выше тариф.

Стратегии подбора аккаунтов:

1. **Коллаборативная фильтрация** — «с этим часто покупают»; использование предпочтений группы для прогноза.
2. **По категории соцсети** — если аккаунты одной соцсети.
3. **По категории бизнеса (МСБ)** — фильтр по сегменту (региональный/городской/локальный).
4. **Композит (fallback)** — объединение стратегий; при пустом списке — переход к следующей.

Подробнее — [service_rest/SRS_v1.md](service_rest/SRS_v1.md), [service_rest/SRS_v2.md](service_rest/SRS_v2.md).  
Модуль импорта МСБ (2GIS) — [service_main/README.md](service_main/README.md).

### Структура каталога

```
docs/mar-tech/recommendation/
├── README.md
├── service_rest/           # REST API рекомендаций
│   ├── SRS_v1.md           # SRS v1 — стратегии 1 и 2
│   ├── SRS_v2.md           # SRS v2 — стратегии 3 и 4
│   ├── openapi_v1.yaml
│   ├── openapi_v2.yaml
│   └── diagramm/
│       └── sequence.puml
└── service_main/           # Основное приложение (админка, импорт МСБ)
    ├── README.md           # Модуль МСБ — обзор
    ├── SRS_msb_v1.md       # SRS импорта МСБ (2GIS)
    ├── TDD_msb_v1.md       # Техдизайн импорта МСБ
    └── diagramm/
        └── sequence.puml
```

## Артефакты

| Артефакт | Описание |
|----------|----------|
| **service_rest/SRS_v1.md** | SRS по фиче «Рекомендации»: стратегии 1 и 2. |
| **service_rest/SRS_v2.md** | Расширение v1: стратегии 3 (МСБ) и 4 (композит fallback). |
| **service_rest/openapi_v1.yaml** | OpenAPI v1: GET /account_recommendation, algo=PBUW/CATG. |
| **service_rest/openapi_v2.yaml** | OpenAPI v2: GET /account_recommendation, algo=PBUW/CATG/MSB/COMPOSITE. |
| **service_main/README.md** | Обзор модуля импорта МСБ. |
| **service_main/SRS_msb_v1.md** | SRS модуля импорта данных 2GIS (CSV) в базу МСБ. |
| **service_main/TDD_msb_v1.md** | Техдизайн: yiic backgroundImport2Gis, exec в фоне. |
