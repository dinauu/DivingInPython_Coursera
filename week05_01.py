import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def get(self, key):
        metric_dict = {}
        send_data = 'get {}\n'.format(key).encode('utf8')
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(send_data)
                response = sock.recv(1024)
                if b'ok' not in response:
                    raise ClientError
                response = str(response).split('\\n')
                for metric in response:
                    metric = metric.split(' ')
                    if len(metric) == 3:
                        metric_key, metric_value, timestamp = metric[0], float(metric[1]), int(metric[2])
                        metric_list = metric_dict.get(metric_key, [])
                        metric_list.append((timestamp, metric_value))
                        metric_dict.update({
                            metric_key: metric_list
                        })
                return metric_dict
            except Exception:
                raise ClientError

    def put(self, metric_key, metric_value, timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))
        send_data = 'put {} {} {}\n'.format(metric_key, metric_value, timestamp).encode('utf8')
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(send_data)
                response = sock.recv(1024)
                if b'ok\n\n' not in response:
                    raise ClientError
            except Exception:
                raise ClientError


class ClientError(Exception):
    pass


if __name__ == '__main__':
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("k1", 0.25, timestamp=70)
    client.put("k1", 2.156, timestamp=5)
    print(client.get('*'))
