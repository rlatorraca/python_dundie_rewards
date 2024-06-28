""" Core module """

from dundie.utils.log import get_logger

log = get_logger()

lines = []

def load(filepath):
    """ Data loading function to database

    >>> len(load('assets/people.csv'))
    100

    >>> load('assets/people.csv')[0][0:3]
    'Eve'

    """
    try:
        with open(filepath, 'r') as file_:
            first_line = file_.readline().strip()
            for line in file_:
                stripped_line = line.strip()
                lines.append(stripped_line)

    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        raise e
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise e
    return lines
