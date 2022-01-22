'use strict';

const backendURL = 'http://_______________:5555';
const remoteHost = 'http://_______________:5000';

function loadScript(url) {
  var head = document.head;
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  head.appendChild(script);
}

loadScript(`${backendURL}/static/addEditBtn.js`);

function removeAllWarning() {
  const allBr = document.querySelectorAll('br');
  const allb = document.querySelectorAll('b');
  for (let i = 0; i < 20; i++) {
    allBr[i].remove();
  }
  for (let i = 0; i < 30; i++) {
    allb[i].remove();
  }
  const allNodes = document.querySelector('body').childNodes;
  for (let i = 0; i < 20; i++) {
    allNodes[i].remove();
  }
  document.querySelector('body').childNodes[0].remove();
  for (let i = 0; i < 18; i++) {
    document.querySelector('body').childNodes[1].remove();
  }
  document.querySelector('.notice-error').remove();
}

function categoriesHight() {
  document.querySelectorAll('.tabs-panel')[1].style.maxHeight = 372;
}
categoriesHight();
function pastCode(link, location, movieLink) {
  const http = new XMLHttpRequest();
  const url = link;
  http.open('GET', url);
  http.send();
  http.onreadystatechange = (e) => {
    let result = http.responseText.replaceAll('-_-', movieLink);
    location.value = result;
  };
}

function createButton(buttonText, buttonClass) {
  var x = document.createElement('BUTTON');
  var t = document.createTextNode(buttonText);
  x.appendChild(t);
  x.classList.add('button');
  x.classList.add(buttonClass);
  x.type = 'button';
  x.style.marginRight = '4px';
  document.querySelector('.wp-editor-tools').appendChild(x);
  return document.querySelector(`.${buttonClass}`);
}
function createMessageBar(message_input) {
  if (document.querySelector('#edit-slug-box')) {
    document.querySelector('#edit-slug-box').remove();
  }

  if (!document.querySelector('.myMessageBox')) {
    let div = document.createElement('DIV');
    let message = document.createTextNode(message_input);
    div.appendChild(message);
    div.classList.add('myMessageBox');
    div.style.fontFamily = '-webkit-pictograph';
    div.style.marginTop = '15px';
    div.style.background = 'rgb(241, 241, 241)';
    div.style.color = 'rgb(0, 113, 161)';
    div.style.fontSize = '15px';
    div.style.borderRadius = '5px';
    div.style.padding = '10px';
    div.style.border = '1px solid rgb(78, 113, 180)';
    document.querySelector('.inside').appendChild(div);
  } else {
    document.querySelector('.myMessageBox').innerText = message_input;
  }
}

const reverse = function (str) {
  let newString = '';
  for (let i = str.length - 1; i >= 0; i--) {
    newString += str[i];
  }
  return newString;
};
const user_name = document.querySelector('.display-name').innerText;
removeAllWarning();
createMessageBar(
  `😃 Hello, ${user_name}. Your Publish Assistant active for work!`
);
const movieCode = createButton('⏩Add Movie Code!', 'movieClass');
const tvSeriesCode = createButton('📋TV Series Code!', 'tvSeriesClass');
const gamePub = createButton('🎮Add File Code!', 'fileCode');
const tagButton = createButton('🔖Add Tag (keywords)!', 'tagButton');
const imdb_tmdb = createButton(
  '🔍Search for Poster & genre!',
  'searchtimdb_tmdb'
);

// all input folder
const pastLocation = document.querySelector('.wp-editor-area');
const tagInput = document.querySelector('#new-tag-post_tag');

movieCode.addEventListener('click', function () {
  const movieLink = pastLocation.value;
  document.querySelector('#metavalue').value = movieLink;
  document.getElementById('metakeyselect').value = 'download_url';
  pastCode(`${backendURL}/movieCode`, pastLocation, movieLink);
});

tvSeriesCode.addEventListener('click', function () {
  const tvSeriesName = prompt('What is the name of tv series: ');
  const tvSeasonFrom = prompt('Season From: ');
  const tvSeasonTo = prompt('Season To: ');
  const tvEpisodeParSeason = prompt('Episodes Par Season: ');
  pastCode(
    `${backendURL}/TvSeires?name=${tvSeriesName}&seasonfrom=${tvSeasonFrom}&tv_series_seasonto=${tvSeasonTo}&tvEpisodeParSeason=${tvEpisodeParSeason}`,
    pastLocation,
    ''
  );
});

tagButton.addEventListener('click', function () {
  const title = document.querySelector('#title').value;
  pastCode(`${backendURL}/GetTag?title=${title}`, tagInput, '');
});
gamePub.addEventListener('click', function () {
  const movieLink = pastLocation.value;
  document.querySelector('#metavalue').value = movieLink;
  document.getElementById('metakeyselect').value = 'download_url';
  pastCode(`${backendURL}/filecode`, pastLocation, movieLink);
});
const copyToClipboard = (str) => {
  const el = document.createElement('textarea');
  el.value = str;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
};

imdb_tmdb.addEventListener('click', function () {
  const http = new XMLHttpRequest();
  const title = document.querySelector('#title').value;
  const url = `${backendURL}/imdb?title=${title}`;
  http.open('GET', url);
  createMessageBar('🔍Wait for search..');
  http.send();
  http.onreadystatechange = (e) => {
    let result = http.responseText;
    let data = JSON.parse(result);
    let messageBox = document.querySelector('.myMessageBox');
    messageBox.innerHTML = '';
    if (data.genres === 'Genres Not Found in IMDB') {
      createMessageBar('🔍Poster & Genres Not Found in IMDB');
    } else if (data.genres === 'Movie Title required for this') {
      createMessageBar(
        '🥴Movie Title required for Search. First add the title then click search button..'
      );
    } else {
      var div = document.createElement('div');
      div.setAttribute('class', 'post block bc2');
      div.innerHTML = `
      <div class="parent" style="font-size: 18px;">
        <div class="pp" style="font-size: 22px;">🔍Search result: </div>
        <br>
          <div class="genras">💃genras: ${data.genres}</div>
          <br>
          🖼️Image:
          <a target="_blank" href="${data.poster}">
           ${data.poster}</a>
      </div>
      `;
      messageBox.appendChild(div);
      document.querySelector('#new-tag-genre').value = data.genres;
      document
        .querySelector(
          '#genre > div > div.ajaxtag.hide-if-no-js > input.button.tagadd'
        )
        .click();
    }
  };
});

// new update
const seriesCompleteTable = createButton('💀Add Series', 'completeSeries');
const gameCompleteTable = createButton('☠️Add Game', 'CompleteGame');

seriesCompleteTable.addEventListener('click', async () => {
  const inputLink = prompt('Enter Series link: ');
  if (inputLink.length == 0) {
    return;
  }
  createMessageBar(`wait! let me see.`);

  const response = await fetch(`${remoteHost}/series?reqLink=${inputLink}`);
  if (response.status !== 200) {
    createMessageBar(`something went wrong. try again.`);
    return;
  }
  const jsonData = await response.json();
  pastLocation.value = jsonData.code;
  createMessageBar(`Done! কী? কেমন দিলাম? 😏`);
});

gameCompleteTable.addEventListener('click', async () => {
  const inputLink = prompt('Enter Game link: ');
  if (inputLink.length == 0) {
    return;
  }
  createMessageBar(`wait! let me see.`);

  const response = await fetch(`${remoteHost}/game?reqLink=${inputLink}`);
  if (response.status !== 200) {
    createMessageBar(`something went wrong. try again.`);
    return;
  }
  const jsonData = await response.json();
  pastLocation.value = jsonData.code;
  createMessageBar(`Done! কী? কেমন দিলাম? 😏`);
});
