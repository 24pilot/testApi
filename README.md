# testApi

    path('report/<int:customer>/<int:year>/<int:month>/', views.report_user_year_month),
    path('report/<int:customer>/<int:year>/', views.report_user_year),
    path balance # It can filter fields >>'item', 'customer', 'created_at'
    Sample:
    /balance/?customer=2
    /balance/?item=1
    /balance/?item=1&customer=2
    /report/1/2021/  >>customer 1, year 2021
    /report/1/2021/4/ >>customer 1, year 2021, month 4
