# testApi
Common CRUD actions:

admin/
api-auth
auth/
registr/ 
users/
items/
transactions/  # It can filter fields >>'item', 'customer', 'created_at'

Report getting actions:
    /transactions/?customer=2
    /transactions/?item=1
    /transactions/?item=1&customer=2

Reports shows summa total and list of transactions:
    users/<int:customer>/
    path('report/<int:customer>/<int:year>/<int:month>/', views.report_user_year_month),
    path('report/<int:customer>/<int:year>/', views.report_user_year),
    path('summa/<int:customer>/<int:item>/', views.summa_user_item)  
    path('summa_all/?...params>>item, customer) -items list, customers list
    Samples:

    /summa_all/?item=1&item=2&customer=1
    /report/1/2021/  >>customer 1, year 2021
    /report/1/2021/4/ >>customer 1, year 2021, month 4
    /summa/1/1/        >>customer 1, item 1

--------------
{
    "url": "http://127.0.0.1:8000/users/2/",

    "users_transactions": [
        {
            "id": 1,
            "customer": "http://127.0.0.1:8000/users/2/",
            "item": "http://127.0.0.1:8000/items/1/",
            "created_at": "2021-04-23T10:30:00.185130Z",
            "item_name": "Apple",
            "item_price": 1,
            "customer_name": "admin"
        },
        {
            "id": 2,
            "customer": "http://127.0.0.1:8000/users/2/",
            "item": "http://127.0.0.1:8000/items/2/",
            "created_at": "2021-04-23T10:30:52.787682Z",
            "item_name": "Banan",
            "item_price": 1,
            "customer_name": "admin"
        }
    ],
    "transactions_count": 2,
    "transactions_summa": 2
}
--------------
{
    "item__price__sum": 7,
    "transactions": [
        {
            "model": "users.transaction",
            "pk": 3,
            "fields": {
                "created_at": "2021-04-23T10:32:11.132Z",
                "updated_at": "2021-04-23T10:32:11.132Z",
                "customer": 1,
                "item": 1
            }
        },
        {
            "model": "users.transaction",
            "pk": 4,
            "fields": {
                "created_at": "2021-04-23T13:43:09.696Z",
                "updated_at": "2021-04-23T13:43:09.696Z",
                "customer": 1,
                "item": 2
            }
        },
        {
            "model": "users.transaction",
            "pk": 9,
            "fields": {
                "created_at": "2021-04-23T16:06:12.130Z",
                "updated_at": "2021-04-23T16:26:56.032Z",
                "customer": 1,
                "item": 2
            }
        },
        {
            "model": "users.transaction",
            "pk": 12,
            "fields": {
                "created_at": "2021-04-28T10:08:06.292Z",
                "updated_at": "2021-04-28T10:08:06.292Z",
                "customer": 1,
                "item": 6
            }
        }
    ]
}