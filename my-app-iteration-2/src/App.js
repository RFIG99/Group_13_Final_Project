//import logo from './logo.svg';
import funny_meme from "./images/funny_meme.jpg"
import funny_meme_2 from "./images/funny_meme2.jpg"
import good_boy from "./images/good_Boy.jpg"
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

<p>I have lived in San Bernardino my whole life. I attended Cajon High School and San Bernardino Valley College as a student before I came to CSUSB. In high school, I played water polo and was on the swim team. </p>


<div class = "paraHDR">
<h1>Food</h1>
</div>

<p> My favorite food is pizza. I also like spaghetti and taquitos. I also like blue cheese burgers from Red Robbin.</p>

<div class = "paraHDR">
<h1>Games</h1>
</div>

<p>I like to play Arkham Batman series of games. I also like to play Metal Gear Solid 5 and games from the Legend of Zelda series. I also play Halo Master Chief Collection and Mortal Kombat 11.</p>

<div class = "paraHDR">
<h1>Extra</h1>
</div>

<p> The bee movie was weird.</p>
<p> The foods, tacos, sushi, and pizza taste good.</p>
<p> How much wood would a woodchuck chuck if a woodchuck could chuck wood? He would chuck, he would, as much as he could, and chuck as much wood as a woodchuck would if a woodchuck could chuck wood.</p>
<p> Sally sells seashells by the seashore.</p>
<p> Students go to school every day in high school but in college they go every other day. WE are goinf to collage for a degree related to computers. The degrees may be in computer science or computer systems or computer enginering.</p>
</div>

<div class = "image">

<img id='funny_meme' src={funny_meme} alt="Funny meme go here" ></img>

<img id='funny_meme_2' src={funny_meme_2} alt="Funny meme go here" ></img>

<img id='good_boy' src={good_boy} alt="good boy" ></img>

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
