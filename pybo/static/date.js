let today = new Date();

let year = today.getFullYear();
let month = today.getMonth() + 1;
let date = today.getDate();
let daynum = today.getDay();

const content = document.querySelector("#calendar");

if (daynum === 0) {
  let day = "Sunday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 1) {
  let day = "Monday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 2) {
  let day = "Tuesday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 3) {
  let day = "Wednesday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 4) {
  let day = "Thursday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 5) {
  let day = "Friday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
} else if (daynum === 6) {
  let day = "Saturday"
  content.innerText = `${day} , ${month} / ${date} , ${year}`
}