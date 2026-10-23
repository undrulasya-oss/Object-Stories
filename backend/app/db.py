import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()
URL=os.getenv('DATABASE_URL','sqlite:///./object_stories.db')
kwargs={'check_same_thread':False} if URL.startswith('sqlite') else {'pool_pre_ping':True}
engine=create_engine(URL,connect_args=kwargs)
SessionLocal=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
def get_db():
 db=SessionLocal()
 try: yield db
 finally: db.close()
