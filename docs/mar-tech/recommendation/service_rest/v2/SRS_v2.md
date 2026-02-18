# REST API рекомендаций 1.1.0

**Версия:** 1.1.0 | **Дата:** 2025

---

**Проблема:** 1.0.0 не учитывает сегмент бизнеса (региональный/городской/локальный).  
**Решение:** Стратегии 3 (MSB) и 4 (композит fallback).  
**Главный сценарий:** Клиент вызывает GET /account_recommendation с algo=MSB или COMPOSITE (либо social+socialId без algo) → получает рекомендации; при COMPOSITE — fallback 1→2→3 до получения непустого результата.

> Обзор: [README.md](README.md) | Базовые FR: [../v1/SRS_v1.md](../v1/SRS_v1.md) (1.0.0)

---

## 1. Область действия

Расширение 1.0.0. Добавлены стратегии 3 (по категории бизнеса, МСБ) и 4 (композит). Стратегия 3 зависит от базы МСБ — [service_main/SRS_msb_v1.md](../../service_main/SRS_msb_v1.md).

---

## 2. Сценарии использования

### UR-003. Рекомендации по сегменту МСБ
Клиент передаёт algo=MSB, social, socialId → стратегия 3. Сегмент (regional/city/local) берётся из аккаунта и базы МСБ.

### UR-004. Композит (fallback)
Клиент передаёт algo=COMPOSITE или social+socialId без algo → fallback: 1 → 2 → 3; при пустом результате — переход к следующей стратегии. Поле strategiesTried отражает фактический путь.

---

## 3. Требования 1.1.0

### Дополнительные FR
- FR-014 — Стратегия MSB использует сегмент (regional/city/local) из базы МСБ
- FR-015 — COMPOSITE выполняет fallback 1→2→3, возвращает первый непустой результат
- FR-016 — При strategy=composite — strategiesTried содержит список применённых стратегий

### Дополнительные BR
- BR-006 — Стратегия 3 требует базу МСБ (импорт 2GIS)

### Изменения контракта
- algo: добавлены MSB, COMPOSITE
- strategy: by_msb, composite
- strategiesTried — при composite
- RecommendedAccount: businessCategory, segment

---

## 4. Контракты

- [openapi_v2.yaml](openapi_v2.yaml) — GET /account_recommendation, algo (PBUW, CATG, MSB, COMPOSITE)
- Добавление на дашборд — в сервисе main (POST /ajax/addWatch)

---

## 5. Тест-кейсы

| TC-ID | Сценарий | Ожидаемый результат | FR |
|-------|----------|---------------------|-----|
| TC-v2-01 | algo=MSB, social, socialId, база МСБ заполнена | Рекомендации по сегменту | FR-014 |
| TC-v2-02 | algo=MSB, база пуста | Пустой список (strategy=by_msb) | BR-006 |
| TC-v2-03 | algo=COMPOSITE, 1 пусто → 2 не пусто | Результат стратегии 2, strategiesTried=[1,2] | FR-015, FR-016 |
| TC-v2-04 | social+socialId без algo | Эквивалент COMPOSITE | FR-015 |

---

## Приложение. Глоссарий

| Термин | Определение |
|--------|-------------|
| **МСБ** | Малый и средний бизнес; данные из 2GIS |
| **Сегмент** | regional / city / local — размер бизнеса |
| **COMPOSITE** | Fallback по стратегиям 1→2→3 |
| **strategiesTried** | Список стратегий, применённых при composite |
