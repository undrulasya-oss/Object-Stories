import {Header,Footer} from '../components';import{SavedList}from'../saved-components';
export default function Saved(){return <main className="wrap"><Header/><section className="collection"><div className="eyebrow">Your cabinet</div><h1 className="serif" style={{fontSize:54}}>Saved objects.</h1><p className="story">A collection kept in this browser.</p><SavedList/></section><Footer/></main>}
