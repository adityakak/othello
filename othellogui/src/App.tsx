import React from 'react';
import './App.css';
import { Header, Footer, Information, BoardFeatures } from './containers';


function App() {
  return (
    <div className="App">
      <Header />
      <BoardFeatures />
      <Information />
      <Footer />
    </div>
  );
}

export default App;
