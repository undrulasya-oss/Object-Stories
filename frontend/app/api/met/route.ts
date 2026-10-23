import {NextRequest,NextResponse} from 'next/server';
const root='https://collectionapi.metmuseum.org/public/collection';
const headers={'Accept':'application/json','User-Agent':'ObjectStories/1.0 collection explorer'};
type MetObject={objectID:number;title:string;artistDisplayName:string;objectDate:string;culture:string;medium:string;department:string;primaryImage:string;primaryImageSmall:string;objectURL:string;isPublicDomain:boolean;creditLine:string;objectName:string;isHighlight:boolean;};
async function getJson(url:string){const response=await fetch(url,{headers,next:{revalidate:3600},signal:AbortSignal.timeout(12000)});if(!response.ok)throw new Error('Museum collection request failed');return response.json()}
export async function GET(request:NextRequest){
 const params=request.nextUrl.searchParams,q=(params.get('q')||'mask').trim().slice(0,100);
 try{
  const url=new URL(root+'/v1.1/search');url.searchParams.set('q',q);url.searchParams.set('hasImages','true');url.searchParams.set('limit','8');
  const search=await getJson(url.toString()) as {total:number;objectIDs:number[]|null};
  const ids=(search.objectIDs||[]).slice(0,8),records: (MetObject|null)[]=[];
  for(let i=0;i<ids.length;i+=3){const batch=await Promise.all(ids.slice(i,i+3).map(async id=>{try{return await getJson(root+'/v1/objects/'+id) as MetObject}catch{return null}}));records.push(...batch)}
  const items=records.filter((item):item is MetObject=>!!item&&item.isPublicDomain&&!!item.primaryImage).map(item=>({id:item.objectID,title:item.title,artist:item.artistDisplayName||'',date:item.objectDate||'',culture:item.culture||'',medium:item.medium||'',department:item.department||'',image:item.primaryImageSmall||item.primaryImage,url:item.objectURL,credit:item.creditLine||'',objectName:item.objectName||'',highlight:item.isHighlight}));
  return NextResponse.json({query:q,total:search.total||0,items,source:'The Metropolitan Museum of Art Open Access API'});
 }catch{return NextResponse.json({query:q,total:0,items:[],source:'The Metropolitan Museum of Art Open Access API',error:'The live museum collection is unavailable right now. Try again in a moment.'},{status:502})}
}

