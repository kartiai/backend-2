import databases
import ormar
import sqlalchemy
import os

engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'))
database=databases.Database(os.getenv('DATABASE_URL'))

# Initialize the database
base_ormar_config = ormar.OrmarConfig(
    metadata=sqlalchemy.MetaData(),
    database=database,
    engine=engine,
)

# Define the User model
class User(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="users")

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    address: str =  ormar.String(max_length=42, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)

class FileStorage(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="files_storage")

    cid: str = ormar.String(max_length=64, primary_key=True)
    file_name: str = ormar.String(max_length=128)
    file_size: int = ormar.Integer()
    file_type: str = ormar.String(max_length=64 )
    file_date: str = ormar.String(max_length=128)

class UserFile(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="user_file")

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    cid: str = ormar.ForeignKey(FileStorage, ondelete='CASCADE')
    user_id: str = ormar.Integer()

base_ormar_config.metadata.create_all(engine)