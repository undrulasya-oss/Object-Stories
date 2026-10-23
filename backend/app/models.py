from __future__ import annotations
import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Text, Boolean, DateTime, ForeignKey, Integer, UniqueConstraint, CheckConstraint, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker

class Base(DeclarativeBase): pass
class Category(Base):
    __tablename__='categories'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(80),unique=True); slug:Mapped[str]=mapped_column(String(100),unique=True,index=True); description:Mapped[str]=mapped_column(Text,default='')
    artifacts:Mapped[list['Artifact']]=relationship(back_populates='category')
class Artifact(Base):
    __tablename__='artifacts'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(180),index=True); slug:Mapped[str]=mapped_column(String(200),unique=True,index=True); short_description:Mapped[str]=mapped_column(String(400)); story:Mapped[str]=mapped_column(Text); historical_period:Mapped[str]=mapped_column(String(120),index=True); origin:Mapped[str]=mapped_column(String(160),index=True); materials:Mapped[list]=mapped_column(JSON,default=list); historical_significance:Mapped[str]=mapped_column(Text,default=''); image_url:Mapped[str|None]=mapped_column(String(500),nullable=True); image_attribution:Mapped[str|None]=mapped_column(String(300),nullable=True); source_url:Mapped[str|None]=mapped_column(String(500),nullable=True); tags:Mapped[list]=mapped_column(JSON,default=list); is_published:Mapped[bool]=mapped_column(Boolean,default=True,index=True); category_id:Mapped[int]=mapped_column(ForeignKey('categories.id',ondelete='RESTRICT')); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))
    category:Mapped[Category]=relationship(back_populates='artifacts')
class Relationship(Base):
    __tablename__='artifact_relationships'; __table_args__=(UniqueConstraint('source_artifact_id','target_artifact_id','relationship_type'),CheckConstraint('source_artifact_id != target_artifact_id'))
    id:Mapped[int]=mapped_column(primary_key=True); source_artifact_id:Mapped[int]=mapped_column(ForeignKey('artifacts.id',ondelete='CASCADE')); target_artifact_id:Mapped[int]=mapped_column(ForeignKey('artifacts.id',ondelete='CASCADE')); relationship_type:Mapped[str]=mapped_column(String(80)); explanation:Mapped[str]=mapped_column(Text); curated:Mapped[bool]=mapped_column(Boolean,default=True)
    source:Mapped[Artifact]=relationship(foreign_keys=[source_artifact_id]); target:Mapped[Artifact]=relationship(foreign_keys=[target_artifact_id])
class Trail(Base):
    __tablename__='trails'; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(180)); slug:Mapped[str]=mapped_column(String(200),unique=True); description:Mapped[str]=mapped_column(Text); estimated_minutes:Mapped[int]=mapped_column(Integer,default=10); is_published:Mapped[bool]=mapped_column(Boolean,default=True); steps:Mapped[list['TrailArtifact']]=relationship(back_populates='trail',cascade='all, delete-orphan',order_by='TrailArtifact.position')
class TrailArtifact(Base):
    __tablename__='trail_artifacts'; __table_args__=(UniqueConstraint('trail_id','artifact_id'),UniqueConstraint('trail_id','position'))
    id:Mapped[int]=mapped_column(primary_key=True); trail_id:Mapped[int]=mapped_column(ForeignKey('trails.id',ondelete='CASCADE')); artifact_id:Mapped[int]=mapped_column(ForeignKey('artifacts.id',ondelete='CASCADE')); position:Mapped[int]=mapped_column(Integer); step_explanation:Mapped[str]=mapped_column(Text); trail:Mapped[Trail]=relationship(back_populates='steps'); artifact:Mapped[Artifact]=relationship()
class Exhibition(Base):
    __tablename__='exhibitions'; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(180)); slug:Mapped[str]=mapped_column(String(200),unique=True); description:Mapped[str]=mapped_column(Text); cover_image_url:Mapped[str|None]=mapped_column(String(500),nullable=True); objects:Mapped[list['ExhibitionArtifact']]=relationship(back_populates='exhibition',cascade='all, delete-orphan',order_by='ExhibitionArtifact.position')
class ExhibitionArtifact(Base):
    __tablename__='exhibition_artifacts'; __table_args__=(UniqueConstraint('exhibition_id','artifact_id'),UniqueConstraint('exhibition_id','position'))
    id:Mapped[int]=mapped_column(primary_key=True); exhibition_id:Mapped[int]=mapped_column(ForeignKey('exhibitions.id',ondelete='CASCADE')); artifact_id:Mapped[int]=mapped_column(ForeignKey('artifacts.id',ondelete='CASCADE')); position:Mapped[int]=mapped_column(Integer); exhibition:Mapped[Exhibition]=relationship(back_populates='objects'); artifact:Mapped[Artifact]=relationship()

