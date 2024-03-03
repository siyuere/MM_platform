from db.models import Task, Session, Model, ModelTaskResult


def get_all_tasks():
    session = Session()
    result = session.query(Task).all()
    session.close()
    return result

def get_model_info_by_id(model_id):
    session = Session()
    return session.query(Model.parameters, Model.parameters).filter(Model.model_id == model_id).first()

def get_model_path_by_id(model_id):
    session = Session()
    return session.query(ModelTaskResult.output_path).filter(ModelTaskResult.model_id == model_id).first()




if __name__ == '__main__':
    print(get_all_tasks())


