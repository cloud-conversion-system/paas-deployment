import zipfile
import py7zr
import tarfile
import os
from cloud_conversion_tool.modelos.modelos import Task, TaskSchema, Status
from ..cloud_bucket_access import gcsManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from flask import Flask

app = Flask(__name__)
engine = create_engine(
    'postgresql://postgres:password@104.198.61.85/cloud_conversion_tool')
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)
task_schema = TaskSchema()
UPLOAD_FOLDER = '/python-docker/cloud_conversion_tool/files/'


@app.route('/process-tasks', methods=['POST'])
def handle_pubsub_message():
    check_database()
    return "Message processed successfully"


def check_database():
    # Process pending tasks
    tasks = db_session.query(Task).filter_by(status=Status.UPLOADED).all()
    for task in tasks:
        compress_file(task.file_name, task.new_format, task.id)


def compress_file(file_name, algorithm, task_id):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    gcsManager.downloadFile(file_name)
    if algorithm == 'zip':
        with zipfile.ZipFile(file_path+'.zip', 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        compressed_file_name = os.path.splitext(file_name)[0] + '.zip'
        gcsManager.uploadFile(file_path+'.zip', compressed_file_name)
        os.remove(file_path+'.zip')
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con ZIP'
    elif algorithm == '7z':
        with py7zr.SevenZipFile(file_path+'.7z', 'w') as szf:
            szf.write(file_path, arcname=os.path.basename(file_path))
        compressed_file_name = os.path.splitext(file_name)[0] + '.7z'
        gcsManager.uploadFile(file_path+'.7z', compressed_file_name)
        os.remove(file_path+'.7z')
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con 7Z'
    elif algorithm == 'targz':
        with tarfile.open(file_path+'.tar.gz', 'w:gz') as tgzf:
            tgzf.add(file_path, arcname=os.path.basename(file_path))
        compressed_file_name = os.path.splitext(file_name)[0] + '.tar.gz'
        gcsManager.uploadFile(file_path+'.tar.gz', compressed_file_name)
        os.remove(file_path+'.tar.gz')
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con TAR.GZ'
    elif algorithm == 'tarbz2':
        with tarfile.open(file_path+'.tar.bz2', 'w:bz2') as tbzf:
            tbzf.add(file_path, arcname=os.path.basename(file_path))
        compressed_file_name = os.path.splitext(file_name)[0] + '.tar.bz2'
        gcsManager.uploadFile(file_path+'.tar.bz2', compressed_file_name)
        os.remove(file_path+'.tar.bz2')
        update_task(task_id)
        return f'El archivo {file_path} ha sido comprimido con TAR.BZ2'


def update_task(task_id):
    task = db_session.query(Task).filter_by(id=task_id).first()
    task.status = Status.PROCESSED
    db_session.commit()
    task_schema.dump(task)


if __name__ == '__main__':
    app.run()
