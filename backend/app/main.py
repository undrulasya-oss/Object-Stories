from fastapi import FastAPI, Depends, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, select, func
from .schemas import ArtifactIn, ArtifactPatch, ArtifactOut, CategorySummary, Page
from typing import Literal
from .db import get_db
from .models import Base, Artifact, Category, Relationship, Trail, TrailArtifact, Exhibition
import os, logging

logging.basicConfig(level=logging.INFO)
app=FastAPI(title='Object Stories API',version='1.0.0',description='A relational museum of artifacts and their connections.')
origins=[x.strip() for x in os.getenv('FRONTEND_ORIGINS','http://localhost:3000').split(',')]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['GET','POST','PATCH','DELETE'],allow_headers=['*'])
def obj(a):return {'id':a.id,'name':a.name,'slug':a.slug,'short_description':a.short_description,'story':a.story,'historical_period':a.historical_period,'origin':a.origin,'materials':a.materials or [],'historical_significance':a.historical_significance,'image_url':a.image_url or 'https://object-stories-weld.vercel.app/artifacts/' + a.slug + ('.png' if a.slug in ('daguerreotype-portrait','morse-telegraph-key') else '.jpg'),'image_attribution':a.image_attribution,'source_url':a.source_url,'tags':a.tags or [],'is_published':a.is_published,'category':{'id':a.category.id,'name':a.category.name,'slug':a.category.slug}}
def published(db):return db.query(Artifact).options(joinedload(Artifact.category)).filter(Artifact.is_published.is_(True))
@app.get('/health')
def health():return {'status':'ok'}
@app.get('/api/v1/artifacts',response_model=Page)
def artifacts(q:str|None=None,category:str|None=None,period:str|None=None,origin:str|None=None,material:str|None=None,tag:str|None=None,page:int=Query(1,ge=1),page_size:int=Query(12,ge=1,le=40),sort:Literal['name','newest']=Query('name'),db:Session=Depends(get_db)):
 query=published(db)
 if q: query=query.filter(or_(Artifact.name.ilike(f'%{q}%'),Artifact.short_description.ilike(f'%{q}%'),Artifact.story.ilike(f'%{q}%'),Artifact.origin.ilike(f'%{q}%')))
 if category:query=query.join(Category).filter(Category.slug==category)
 if period:query=query.filter(Artifact.historical_period.ilike(f'%{period}%'))
 if origin:query=query.filter(Artifact.origin.ilike(f'%{origin}%'))
 if material:query=query.filter(func.cast(Artifact.materials,String).ilike(f'%{material}%'))
 if tag:query=query.filter(func.cast(Artifact.tags,String).ilike(f'%{tag}%'))
 total=query.count();query=query.order_by(Artifact.name if sort=='name' else Artifact.created_at.desc());rows=query.offset((page-1)*page_size).limit(page_size).all()
 return {'items':[obj(x) for x in rows],'total':total,'page':page,'page_size':page_size,'pages':(total+page_size-1)//page_size}
@app.get('/api/v1/discover/random')
def random_artifact(db:Session=Depends(get_db)):
 from sqlalchemy.sql import func as sqlfunc
 a=published(db).order_by(sqlfunc.random()).first()
 if not a:raise HTTPException(404,'No published artifacts')
 return {'artifact':obj(a),'why':a.historical_significance}
@app.get('/api/v1/artifacts/{key}',response_model=ArtifactOut)
def artifact(key:str,db:Session=Depends(get_db)):
 a=published(db).filter(or_(Artifact.slug==key,Artifact.id==int(key) if key.isdigit() else False)).first()
 if not a:raise HTTPException(404,'Artifact not found')
 return obj(a)
@app.get('/api/v1/artifacts/{artifact_id}/connections')
def connections(artifact_id:int,db:Session=Depends(get_db)):
 rows=db.query(Relationship).filter(or_(Relationship.source_artifact_id==artifact_id,Relationship.target_artifact_id==artifact_id)).all();items=[]
 for r in rows:
  target=r.target if r.source_artifact_id==artifact_id else r.source
  if target.is_published:items.append({'type':r.relationship_type,'explanation':r.explanation,'curated':r.curated,'artifact':obj(target)})
 return {'items':items}
@app.get('/api/v1/relationships')
def relationships(db:Session=Depends(get_db)):
 return [{'id':r.id,'source':obj(r.source),'target':obj(r.target),'type':r.relationship_type,'explanation':r.explanation,'curated':r.curated} for r in db.query(Relationship).all()]
@app.get('/api/v1/categories')
def categories(db:Session=Depends(get_db)):
 return [{'id':c.id,'name':c.name,'slug':c.slug,'description':c.description,'artifact_count':len([a for a in c.artifacts if a.is_published])} for c in db.query(Category).all()]
@app.get('/api/v1/categories/{slug}')
def category(slug:str,db:Session=Depends(get_db)):
 c=db.query(Category).filter_by(slug=slug).first()
 if not c:raise HTTPException(404,'Category not found')
 return {'id':c.id,'name':c.name,'slug':c.slug,'description':c.description}
@app.get('/api/v1/trails')
def trails(db:Session=Depends(get_db)):
 return [trail_out(t) for t in db.query(Trail).filter_by(is_published=True).all()]
def trail_out(t):return {'id':t.id,'title':t.title,'slug':t.slug,'description':t.description,'estimated_minutes':t.estimated_minutes,'steps':[{'position':s.position,'step_explanation':s.step_explanation,'artifact':obj(s.artifact)} for s in t.steps]}
@app.get('/api/v1/trails/{slug}')
def trail(slug:str,db:Session=Depends(get_db)):
 t=db.query(Trail).filter_by(slug=slug,is_published=True).first()
 if not t:raise HTTPException(404,'Trail not found')
 return trail_out(t)
@app.get('/api/v1/exhibitions')
def exhibitions(db:Session=Depends(get_db)):
 return [{'id':e.id,'title':e.title,'slug':e.slug,'description':e.description,'cover_image_url':e.cover_image_url,'items':[{'position':i.position,'artifact':obj(i.artifact)} for i in e.objects]} for e in db.query(Exhibition).all()]
@app.get('/api/v1/exhibitions/{slug}')
def exhibition(slug:str,db:Session=Depends(get_db)):
 e=db.query(Exhibition).filter_by(slug=slug).first()
 if not e:raise HTTPException(404,'Exhibition not found')
 return {'id':e.id,'title':e.title,'slug':e.slug,'description':e.description,'cover_image_url':e.cover_image_url,'items':[{'position':i.position,'artifact':obj(i.artifact)} for i in e.objects]}
def admin(x_admin_key:str|None):
 if not os.getenv('ADMIN_API_KEY') or x_admin_key!=os.getenv('ADMIN_API_KEY'):raise HTTPException(403,'Valid X-Admin-Key required')
@app.post('/api/v1/artifacts',status_code=201,response_model=ArtifactOut)
def create_artifact(data:ArtifactIn,x_admin_key:str|None=Header(None),db:Session=Depends(get_db)):
 admin(x_admin_key);a=Artifact(**data.model_dump());db.add(a)
 try:db.commit();db.refresh(a)
 except Exception as e:db.rollback();raise HTTPException(409,'Artifact slug or data conflicts with an existing record') from e
 return obj(a)
@app.patch('/api/v1/artifacts/{artifact_id}',response_model=ArtifactOut)
def update_artifact(artifact_id:int,data:ArtifactPatch,x_admin_key:str|None=Header(None),db:Session=Depends(get_db)):
 admin(x_admin_key);a=db.get(Artifact,artifact_id)
 if not a:raise HTTPException(404,'Artifact not found')
 for k,v in data.model_dump(exclude_unset=True,exclude_none=True).items():setattr(a,k,v)
 db.commit();db.refresh(a);return obj(a)
@app.delete('/api/v1/artifacts/{artifact_id}',status_code=204)
def delete_artifact(artifact_id:int,x_admin_key:str|None=Header(None),db:Session=Depends(get_db)):
 admin(x_admin_key);a=db.get(Artifact,artifact_id)
 if not a:raise HTTPException(404,'Artifact not found')
 db.delete(a);db.commit()







