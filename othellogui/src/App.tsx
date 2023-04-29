import React from 'react';
import './App.css';
import { Header, Footer, Information, BoardFeatures } from './containers';
import { Navbar } from './components';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Header />
      <BoardFeatures />
      <Information />
      <Footer />
    </div>
  );
}

export default App;
