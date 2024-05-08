//import logo from './logo.svg';
import funny_meme from "./images/funny_meme.jpg"
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="About me">

      <body>
<div class = "mainHDR">
<h1>About Me</h1>
</div>


<div class = "paragraph">

<div class = "paraHDR">
<h1>Life</h1>
</div>

<p>I have lived in San Bernardino my whole life. I attended Cajon High School and San Bernardino Valley College Before I came to CSUSB. In high school, I played water polo and was on the swim team. </p>


<div class = "paraHDR">
<h1>Food</h1>
</div>

<p> My favorite food is pizza. I also like spaghetti and taquitos. I also like blue cheese burgers from Red Robbin.</p>

<div class = "paraHDR">
<h1>Games</h1>
</div>

<p>I like to play Arkham Batman series of games. I also like to play Metal Gear Solid 5 and games from the Legend of Zelda series. I also play Halo Master Chief Collection and Mortal Kombat 11.</p>
</div>

<div class = "image">

<img id='funny_meme' src={funny_meme} alt="Funny meme go here" ></img>

</div>

<div class = "git">

<a href="https://github.com/RFIG99/Platform-Computing" target="_blank" rel="noreferrer"> Welcome to my Platform Computing Github</a>

</div>

</body>
      </header>
    </div>
    
  );
}

export default App;
