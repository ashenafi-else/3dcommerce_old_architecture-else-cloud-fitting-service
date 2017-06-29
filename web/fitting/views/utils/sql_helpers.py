"""SQL request relation routines"""


def sql_call(connection, sql_request):
    data = []
    with connection.cursor() as cursor:
        cursor.execute(sql_request)
        desc = cursor.description
        data = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    return data
