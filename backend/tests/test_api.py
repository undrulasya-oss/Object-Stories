import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import get_db
from app.main import app
from app.models import Base, Category, Artifact, Relationship, Trail, TrailArtifact

@pytest.fixture
def client(monkeypatch):
    engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    Base.metadata.create_all(engine); Session=sessionmaker(bind=engine,expire_on_commit=False)
    db=Session(); cat=Category(name='Science',slug='science',description='Tools'); db.add(cat);db.flush()
    a=Artifact(name='Astrolabe',slug='astrolabe',short_description='A sky instrument',story='A layered instrument for astronomy.',historical_period='Medieval',origin='Islamic world',materials=['brass'],historical_significance='Used in astronomy.',tags=['sky'],category_id=cat.id)
    b=Artifact(name='Telescope',slug='telescope',short_description='An optical instrument',story='An instrument for distant observation.',historical_period='17th century',origin='Netherlands',materials=['glass'],historical_significance='Changed astronomy.',tags=['optics'],category_id=cat.id)
    db.add_all([a,b]);db.flush();db.add(Relationship(source_artifact_id=a.id,target_artifact_id=b.id,relationship_type='shared-theme',explanation='Both extend observation.'))
    t=Trail(title='Seeing More',slug='seeing-more',description='A short trail',estimated_minutes=5);db.add(t);db.flush();db.add(TrailArtifact(trail_id=t.id,artifact_id=a.id,position=1,step_explanation='Begin with the sky.'));db.commit();db.close()
    def override():
        session=Session()
        try: yield session
        finally:session.close()
    app.dependency_overrides[get_db]=override
    monkeypatch.setenv('ADMIN_API_KEY','test-key')
    with TestClient(app) as c: yield c
    app.dependency_overrides.clear();Base.metadata.drop_all(engine);engine.dispose()

def test_artifact_lookup_and_not_found(client):
    assert client.get('/api/v1/artifacts/astrolabe').status_code==200
    assert client.get('/api/v1/artifacts/unknown').status_code==404

def test_search_filter_and_pagination(client):
    r=client.get('/api/v1/artifacts',params={'q':'optical','page':1,'page_size':1})
    assert r.status_code==200 and r.json()['total']==1 and r.json()['items'][0]['slug']=='telescope'
    r=client.get('/api/v1/artifacts',params={'category':'science','page':1,'page_size':1})
    assert r.json()['total']==2 and r.json()['pages']==2 and len(r.json()['items'])==1

def test_connections_and_trails(client):
    connections=client.get('/api/v1/artifacts/1/connections').json()['items']
    assert connections[0]['artifact']['slug']=='telescope'
    trail=client.get('/api/v1/trails/seeing-more').json()
    assert trail['steps'][0]['artifact']['slug']=='astrolabe'

def test_admin_write_is_protected(client):
    payload={'name':'Sundial','slug':'sundial','short_description':'A time tool','story':'A shadow marks time.','historical_period':'Ancient','origin':'Mediterranean','materials':['stone'],'historical_significance':'Solar time.','category_id':1}
    assert client.post('/api/v1/artifacts',json=payload).status_code==403
    assert client.post('/api/v1/artifacts',json=payload,headers={'X-Admin-Key':'test-key'}).status_code==201
    assert client.get('/api/v1/artifacts/sundial').status_code==200
