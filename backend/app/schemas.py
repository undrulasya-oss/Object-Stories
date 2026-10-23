from pydantic import BaseModel, Field, ConfigDict
class ArtifactIn(BaseModel):
 name:str=Field(min_length=2,max_length=180);slug:str=Field(pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$');short_description:str=Field(max_length=400);story:str;historical_period:str;origin:str;materials:list[str]=[];historical_significance:str='';image_url:str|None=None;image_attribution:str|None=None;source_url:str|None=None;tags:list[str]=[];category_id:int;is_published:bool=True
class ArtifactPatch(BaseModel):
 name:str|None=None;slug:str|None=Field(None,pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$');short_description:str|None=None;story:str|None=None;historical_period:str|None=None;origin:str|None=None;materials:list[str]|None=None;historical_significance:str|None=None;image_url:str|None=None;image_attribution:str|None=None;source_url:str|None=None;tags:list[str]|None=None;category_id:int|None=None;is_published:bool|None=None
class CategorySummary(BaseModel): id:int;name:str;slug:str
class ArtifactOut(BaseModel):
 model_config=ConfigDict(from_attributes=True)
 id:int;name:str;slug:str;short_description:str;story:str;historical_period:str;origin:str;materials:list[str];historical_significance:str;image_url:str|None;image_attribution:str|None;source_url:str|None;tags:list[str];is_published:bool;category:CategorySummary
class Page(BaseModel): items:list[ArtifactOut];total:int;page:int;page_size:int;pages:int


