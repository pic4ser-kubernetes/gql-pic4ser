__version__ = '0.1.0'

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class GQLSendMixin:

    def __init__(self, url, *args, **kwargs):
        gql_transport = RequestsHTTPTransport(
            url=url,
            verify=True,
            retries=3,
        )

        self._gql_client = Client(transport=gql_transport, fetch_schema_from_transport=True)

        super().__init__(*args, **kwargs)

    def _gql_send(self, query_string, variables=None):
        query = gql(query_string)
        return self._gql_client.execute(query, variable_values=variables)

    def gql_add_data(self, session: str, robot: str, data_group: str, data: float, timestamp: str):
        query = '''
        mutation addData($session: String!, $robot: String!, $dataGroup: String!, $data: Float!, $timestamp: DateTime!) {
            addData(
                dataDict: {session: $session, robot: $robot, dataGroup: $dataGroup, data: $data, timestamp: $timestamp}
            ) {
                ok
            }
        }
        '''

        variables = {
            'session': session,
            'robot': robot,
            'dataGroup': data_group,
            'data': data,
            'timestamp': timestamp,
        }

        return self._gql_send(query, variables)

    def gql_update_status(self, session: str, robot: str, parameter_name: str, status: str, timestamp: str):
        query = '''
        mutation updateStatus($session: String!, $robot: String!, $name: String!, $status: String!, $timestamp: DateTime!) {
            updateStatus(
                statusDict: {session: $session, robot: $robot, name: $name, status: $status, timestamp: $timestamp}
            ) {
                ok
            }
        }
        '''

        variables = {
            'session': session,
            'robot': robot,
            'name': parameter_name,
            'status': status,
            'timestamp': timestamp,
        }

        return self._gql_send(query, variables)

    def gql_add_webcam(self, session: str, robot: str, name: str, url: str):
        query = '''
        mutation addWebcam($session: String!, $robot: String!, $name: String!, $url: String!) {
            addWebcam(
                webcamDict: {session: $session, robot: $robot, name: $name, url: $url}
            ) {
                ok
            }
        }
        '''

        variables = {
            'session': session,
            'robot': robot,
            'name': name,
            'url': url,
        }

        return self._gql_send(query, variables)
