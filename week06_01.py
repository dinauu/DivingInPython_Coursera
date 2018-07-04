import asyncio

metrics_dict = {}


def process_data(data):
    success_status = 'ok\n\n'
    wrong_command_status = 'error\nwrong command\n\n'
    index_error = 'Index error'
    command = data.split()
    if 'put' in command[0]:
        key, value, timestamp = command[1], command[2], command[3]
        old_metrics = metrics_dict.get(key, [])
        for i, metric in enumerate(old_metrics):
            if metric[0] == timestamp:
                old_metrics.remove((timestamp, metric[1]))
                old_metrics.insert(i, (timestamp, value))
                return success_status
        old_metrics.append((timestamp, value))
        metrics_dict.update(
            {
                key: old_metrics
            }
        )
        return success_status
    elif 'get' in command[0]:
        send_metrics = 'ok\n'
        key = command[1]
        if key == '*':
            for key, item_list in metrics_dict.items():
                item_list.sort()
                for item_tuple in item_list:
                    try:
                        send_metrics += '{key} {value} {timestamp}\n'.format(
                            key=key, value=item_tuple[1], timestamp=item_tuple[0]
                        )
                    except IndexError:
                        return index_error
            return send_metrics + '\n'
        metrics = metrics_dict.get(key, None)
        if metrics is None:
            return success_status
        try:
            metrics.sort()
            for metric in metrics:
                send_metrics += '{key} {value} {timestamp}\n'.format(
                    key=key, value=metric[1], timestamp=metric[0]
                )
            return send_metrics + '\n'
        except IndexError:
            return index_error
    else:
        return wrong_command_status


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = process_data(data.decode())
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)


