const base = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';
export type Artifact = { id:number; name:string; slug:string; short_description:string; story:string; historical_period:string; origin:string; materials:string[]; historical_significance:string; image_url:string|null; image_attribution:string|null; source_url:string|null; category:{name:string;slug:string}; tags:string[] };
export type Page<T> = {items:T[];total:number;page:number;page_size:number;pages:number};
export async function api<T>(path:string):Promise<T>{const init=path==='/discover/random'||path.startsWith('/artifacts')?{cache:'no-store' as const}:{next:{revalidate:60}};const r=await fetch(`${base}${path}`,init);if(!r.ok)throw new Error(`Museum API returned ${r.status}`);return r.json()}
