import time

import requests
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from _helpers.sql import establish_connection, execute_query


class GatewayAPI(viewsets.ViewSet):
    """
    Sample input:
    type: client-register
    username: nima
    email: nima0fathi@gmail.com
    password: Mypassword123
    """

    def list(self, request):
        request_type = request.data["req_type"]
        token = request.data.get('token', None)
        if request_type == 'client-register':
            return self.client_register(request.data)
        if request_type == 'login':
            return self.login(request.data)
        if request_type == 'client-profile-view':
            if not self.validate_token(token, 'client'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.client_profile_view(request.data)
        if request_type == 'client-profile-update':
            if not self.validate_token(token, 'client'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.client_profile_update(request.data)
        if request_type == 'admin-profile-view':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.admin_profile_view(request.data)
        if request_type == 'admin-profile-update':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.admin_profile_update(request.data)
        if request_type == 'create_book':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.create_book(request.data)
        if request_type == 'update_book':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.update_book(request.data)
        if request_type == 'get_book':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.get_book(request.data)
        if request_type == 'delete_book':
            if not self.validate_token(token, 'admin'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.delete_book(request.data)
        if request_type == 'search':
            if not self.validate_token(token, 'client'):
                return Response(data='token invalid or expired', status=status.HTTP_403_FORBIDDEN)
            return self.search(request.data)
        return Response("")

    def validate_token(self, token, account_type):
        print('here')
        now = timezone.now()
        command = """
        SELECT count(*) FROM account_management_accesstoken where token=%s AND expire_time>=%s AND account_type=%s
        """
        connection = establish_connection()
        result = execute_query(connection=connection, command=command, inputs=[token, now, account_type])
        if result[0][0] != 0:
            return True
        return False

    def request_handler(self, url, data, request_type):
        request_success = False
        retry_count = 0
        while not request_success:
            try:
                resp = getattr(requests, request_type)(url=url, data=data, timeout=0.5)
                request_success = True
            except requests.Timeout:
                request_success = False
                retry_count += 1
            if resp.status_code >= 500:
                retry_count += 1
                request_success = False
            if retry_count >= 3:
                retry_count %= 3
                time.sleep(10)
        return resp.json(), resp.status_code

    def client_register(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-register', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def login(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/login', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def client_profile_view(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-profile-view', data=data,
                                                      request_type='get')
        return Response(data=resp_data, status=status_code)

    def client_profile_update(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/client-profile-update', data=data,
                                                      request_type='put')
        return Response(data=resp_data, status=status_code)

    def admin_register(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-register', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def admin_profile_view(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-profile-view', data=data,
                                                      request_type='get')
        return Response(data=resp_data, status=status_code)

    def admin_profile_update(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8000/api/admin-profile-update', data=data,
                                                      request_type='put')
        return Response(data=resp_data, status=status_code)

    def get_book(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8001/book/retrieve/' + data['id'],
                                                      data=data, request_type='get')
        return Response(data=resp_data, status=status_code)

    def update_book(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8001/book/update/' + data['id'], data=data,
                                                      request_type='put')
        return Response(data=resp_data, status=status_code)

    def create_book(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8001/book/create/', data=data,
                                                      request_type='post')
        return Response(data=resp_data, status=status_code)

    def delete_book(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8001/book/delete/' + data['id'], data=data,
                                                      request_type='delete')
        return Response(data=resp_data, status=status_code)

    def search(self, data):
        resp_data, status_code = self.request_handler(url='http://127.0.0.1:8002/search_book/', data=data,
                                                      request_type='get')
        return Response(data=resp_data, status=status_code)
