const domain = 'http://localhost:8000/api/';

let list = document.getElementById('list');
let listLoader = new XMLHttpRequest();

listLoader.addEventListener('readystatechange', () => {
  if (listLoader.readyState == 4) {
    if (listLoader.status == 200) {
      let data = JSON.parse(listLoader.responseText);
      let s = '<ul>';
      for (let i = 0; i < data.length; i++) {
        let d = data[i];
        s += '<li>' + d.name + '</li>';
      }
      s += '</ul>';
      list.innerHTML = s;
    } else {
      window.alert(listLoader.statusText);
    }
  }
});

function listLoad() {
  listLoader.open('GET', domain, true);
  listLoader.send();
}

listLoad();
