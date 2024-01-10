from db.models import Task, Session, request


def get_all_tasks():
    session = Session()
    result = session.query(Task).all()
    session.close()
    return result





if __name__ == '__main__':
    print(get_all_tasks())


