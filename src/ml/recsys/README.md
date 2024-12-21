# Рекомендательная система

- **recommendation_system.py** - рекомендательная система.
- **metricts.py** - метрики для оценки качества рекомендаций.
- **sales_train.csv** - тренировочкая выборка, содержит колонки: *date, date_block_num, shop_id, item_id, item_price, item_cnt_day*. При покупке на сайте должна пополняться новыми значениями.
- **sales_prod.csv** - таблица с продажами на нашем сайте. Отличается от *sales_train* наличием *user_id*.
- **all_recommendations.csv** - будет содержать все рекомендации для каждого пользователя, чтобы считать метрики эффективности рекомендаций. Содержит колонки: *data,user_id,recommendations,bucket_id*.
- **items.csv** - содержит колонки: *item_name, item_id, item_category_id*.
- **item_categories.csv** - содержит колонки: *item_category_name, item_category_id*.
