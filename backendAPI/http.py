from rest_framework import status
from rest_framework.response import Response


def JsonResponse(data=None, status=status.HTTP_200_OK):
    if data:
        resp = data
    else:
        resp = {'success': True}
    return Response(resp, status=status, content_type='application/json')


def JsonError(errors, status=status.HTTP_400_BAD_REQUEST):
    if type(errors) == type(str()):
        data = {
            'errors': [{
                'code': status,
                'description': errors
            }]
        }
    else:
        data = dict()
        for e_key in errors:
            data = {
                'errors': [{
                    'code': status,
                    e_key: u', '.join(errors.get(e_key))
                }]
            }
    return Response(data, status=status, content_type='application/json')