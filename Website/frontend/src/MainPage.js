import './App.css';
import {Link} from 'react-router-dom'


function MainPage() {
  return (
    <div className="App">
      <div style={{background:'white', height:'10vw'}}>
        <p style={{color:'darkgreen', fontSize:'60px', position:'absolute', left:'12%', top:'-5%'}}>
          Jack Black
        </p> 
      </div>
      <div style={{width:'100%', background:'white', display:'flex', flexDirection:'row', justifyContent:'space-around', height:'5vw'}}>
        <Link to='/TeamPage' style={{width:'10%', background:'#282c34', color:'white', fontSize:'15px', border:'0px' }}>Our Team</Link>
        <button style={{width:'10%', background:'#282c34', color:'white', fontSize:'15px', border:'0px' }}>Problem Statement</button>
        <button style={{width:'10%', background:'#282c34', color:'white', fontSize:'15px', border:'0px' }}>Specs</button>
        <button style={{width:'10%', background:'#282c34', color:'white', fontSize:'15px', border:'0px' }}>Documents</button>
        <button style={{width:'10%', background:'#282c34', color:'white', fontSize:'15px', border:'0px' }}>Diagrams/Demo</button>
      </div>
      <header className="App-header">
        <p>
          SDP 2022
        </p>

      </header>
    </div>
  );
}

export default MainPage;
