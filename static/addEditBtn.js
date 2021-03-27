"use strict";
function addEdit(movieId) {
  let editBtn = document.createElement("a");
  editBtn.innerHTML = "Edit";
  editBtn.style.backgroundColor = "rgb(206 155 1 / 90%)";
  editBtn.classList.add("playbtn");
  editBtn.href = `http://circleftp.net/wp-admin/post.php?post=${movieId}&action=edit`;
  editBtn.target = "_blank";
  document.querySelector(`#post-${movieId} > div`).appendChild(editBtn);
}
function addEditBtn() {
  const allMovies = document.querySelectorAll("article");
  for (let i = 0; i < allMovies.length; i++) {
    console.log(allMovies[i].classList[1]);
    const movieId = allMovies[i].classList[1].split("-")[1];
    addEdit(movieId);
  }
}
addEditBtn();
