# -*- coding: utf-8 -*-
"""
Сверка отчёта продавца (revise_rep) с нашей БД (revise_stats).
Сравнение по номеру заказа и сумме комиссии (CPA руб. vs profit_amount).
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent


def parse_cpa_rub(s: str) -> float:
    """Парсит 'CPA, руб.' из отчёта продавца: '-2,584.32' или '373.56'."""
    if not s or not s.strip():
        return 0.0
    s = s.strip().replace(' ', '').replace(',', '')
    try:
        return float(s)
    except ValueError:
        return 0.0


def load_seller_report(path: Path) -> dict[str, float]:
    """Загружает отчёт продавца: order_number -> сумма CPA (руб.) по заказу."""
    order_cpa = defaultdict(float)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        # Ищем индекс колонки "CPA, руб." (именно вознаграждение в рублях, не ставка CPA)
        cpa_col = None
        order_col = 0
        for i, col in enumerate(header):
            if 'руб' in col and ('CPA' in col or 'cpa' in col.lower()):
                cpa_col = i  # предпочитаем последнюю подходящую — это "CPA, руб."
            if 'Номера заказа' in col or 'номера' in col.lower():
                order_col = i
        if cpa_col is None:
            cpa_col = 11
        # В данных из-за trailing comma сумма "CPA, руб." фактически в колонке 10
        if cpa_col == 11 and len(header) >= 11:
            cpa_col = 10
        for row in reader:
            if len(row) <= max(order_col, cpa_col):
                continue
            try:
                order_id = row[order_col].strip()
                if not order_id or not order_id.isdigit():
                    continue
                cpa = parse_cpa_rub(row[cpa_col])
                order_cpa[order_id] += cpa
            except (IndexError, ValueError):
                continue
    return dict(order_cpa)


def load_our_stats(path: Path) -> dict[str, float]:
    """Загружает нашу выгрузку: order_number -> profit_amount (одна строка на заказ)."""
    order_profit = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id = (row.get('order_number') or '').strip()
            if not order_id:
                continue
            try:
                profit = float(row.get('profit_amount', 0) or 0)
            except (ValueError, TypeError):
                profit = 0.0
            # если один заказ встречается несколько раз — суммируем (на всякий случай)
            order_profit[order_id] = order_profit.get(order_id, 0) + profit
    return order_profit


def round2(x: float) -> float:
    return round(x, 2)


def main():
    rep_path = BASE / 'revise_rep_09_01-15.csv'
    stats_path = BASE / 'revise_stats_09_01-15.csv'

    seller = load_seller_report(rep_path)
    ours = load_our_stats(stats_path)

    all_orders = set(seller) | set(ours)
    tolerance = 0.02  # допуск на округление (2 копейки)

    only_in_seller = []
    only_in_ours = []
    amount_mismatch = []  # (order_id, seller_cpa, our_profit, diff)

    for order_id in sorted(all_orders, key=int):
        s_cpa = seller.get(order_id, 0)
        o_profit = ours.get(order_id, 0)
        s_cpa_r = round2(s_cpa)
        o_profit_r = round2(o_profit)

        if order_id not in ours:
            only_in_seller.append((order_id, s_cpa_r))
            continue
        if order_id not in seller:
            only_in_ours.append((order_id, o_profit_r))
            continue

        diff = round2(o_profit_r - s_cpa_r)
        if abs(diff) > tolerance:
            amount_mismatch.append((order_id, s_cpa_r, o_profit_r, diff))

    # Итоги
    total_seller = round2(sum(seller.values()))
    total_ours = round2(sum(ours.values()))
    total_diff = round2(total_ours - total_seller)

    report = {
        'only_in_seller': only_in_seller,
        'only_in_ours': only_in_ours,
        'amount_mismatch': amount_mismatch,
        'total_seller': total_seller,
        'total_ours': total_ours,
        'total_diff': total_diff,
        'count_only_seller': len(only_in_seller),
        'count_only_ours': len(only_in_ours),
        'count_mismatch': len(amount_mismatch),
    }
    return report


def format_report_for_mail(r: dict) -> str:
    """Формирует текстовую сводку для письма продавцу."""
    lines = []
    lines.append('=== СВОДКА СВЕРКИ ===')
    lines.append(f"Итого по вашему отчёту (руб.): {r['total_seller']:,.2f}".replace(',', ' '))
    lines.append(f"Итого по нашим данным (руб.): {r['total_ours']:,.2f}".replace(',', ' '))
    lines.append(f"Разница (руб.): {r['total_diff']:,.2f}".replace(',', ' '))
    lines.append('')
    lines.append(f"Заказы только в вашем отчёте (нет у нас): {r['count_only_seller']}")
    lines.append(f"Заказы только в наших данных (нет в вашем отчёте): {r['count_only_ours']}")
    lines.append(f"Заказы с расхождением по сумме: {r['count_mismatch']}")
    # разбивка расхождений: округление (< 1 руб) vs существенные
    small = [(oid, s, o, d) for oid, s, o, d in r['amount_mismatch'] if abs(d) < 1]
    significant = [(oid, s, o, d) for oid, s, o, d in r['amount_mismatch'] if abs(d) >= 1]
    lines.append(f"  из них незначительные (округление до 1 руб.): {len(small)}")
    lines.append(f"  существенные расхождения: {len(significant)}")
    if r['only_in_ours']:
        sum_only_ours = sum(v for _, v in r['only_in_ours'])
        lines.append(f"Сумма по заказам «только у нас» (руб.): {sum_only_ours:,.2f}".replace(',', ' '))
    if significant[:10]:
        lines.append('')
        lines.append('Примеры существенных расхождений (номер заказа, у вас, у нас, разница):')
        for t in significant[:10]:
            lines.append(f"  {t[0]}: {t[1]:.2f} / {t[2]:.2f} / {t[3]:+.2f}")
    if r['only_in_ours'][:10]:
        lines.append('')
        lines.append('Примеры заказов, которые есть у нас, но отсутствуют в вашем отчёте:')
        for oid, amt in r['only_in_ours'][:10]:
            lines.append(f"  {oid}: {amt:.2f} руб.")
    return '\n'.join(lines)


if __name__ == '__main__':
    r = main()
    print('Заказы только в отчёте продавца:', r['count_only_seller'])
    print('Заказы только у нас:', r['count_only_ours'])
    print('Расхождения по сумме (заказов):', r['count_mismatch'])
    print('Итого по отчёту продавца (руб.):', r['total_seller'])
    print('Итого у нас (руб.):', r['total_ours'])
    print('Разница итогов (руб.):', r['total_diff'])
    print()
    print(format_report_for_mail(r))
