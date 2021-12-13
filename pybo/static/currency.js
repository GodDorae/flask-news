const usd_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json";
fetch(usd_url)
.then((response) => response.json())
.then((data) => {
  const usd_kor = document.getElementById("usd");
  usd_kor.innerText = `1 USD: ${Math.round(data.usd.krw)} KRW`
});

const btc_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/btc.json";
fetch(btc_url)
.then((response) => response.json())
.then((data) => {
  const btc_kor = document.getElementById("btc");
  btc_kor.innerText = `1 BTC: ${Math.round(data.btc.krw)} KRW`
});
