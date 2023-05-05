import React from 'react';
import './App.css';
import { Header, Footer, Information, BoardFeatures } from './containers';
import { Navbar } from './components';

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className='othello_bg'>
        <Header />
        <BoardFeatures />
        <Information />
      </div>
      <Footer />
    </div>
  );
}

export default App;
