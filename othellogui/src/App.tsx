import React from 'react';
import './App.css';
import { Header, Footer, Information, BoardFeatures } from './containers';
import { Navbar } from './components';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Header />
      <div className='othello_bg'>
        <BoardFeatures />
      </div>
      <Information />
      <Footer />
    </div>
  );
}

export default App;
