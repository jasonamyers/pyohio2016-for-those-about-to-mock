def process_results(results):
    if results.status_code == 404:
        return {'message': 'Rock Not found!'}
    elif results.status_code == 500:
        return {'message': 'Rock Imploded!'}
    elif results.status_code == 200:
        return results.json()
    else:
        raise ValueError('SHARON!')


def process_file(filename):
    lines = []
    with open(filename, 'rw') as proc_file:
        for line in proc_file:
            lines.append(line.strip('\n'))
    return lines
