const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const main = async (drug, ntweets, delay_in_ms) => {
  const browser = await puppeteer.launch({
    headless: false,
    ignoreHTTPSErrors: true,
    args: [`--window-size=1920,1080`],
    defaultViewport: {
      width: 1920,
      height: 1080,
    },
  });
  const page = await browser.newPage();
  //const drug = "remdesivir";
  await page.goto(
    `https://twitter.com/search?q=${drug}&src=typed_query&f=live`,
    { waitUntil: "networkidle0" }
  );
  page.waitForSelector("nav", { visible: true });
  const tweets = await autoScroll(
    page,
    parseInt(ntweets),
    parseInt(delay_in_ms)
  );
  console.log(tweets);
  saveToDisk(tweets, `data/tweets/${drug}.${tweets.length}.json`);
  await browser.close();
};

async function autoScroll(page, ntweets, delay_in_ms) {
  console.log("ntweets", ntweets);
  console.log("Delay (ms)", delay_in_ms);
  const output = await page.evaluate(
    async (ntweets, delay_in_ms) => {
      return await new Promise((resolve, reject) => {
        var totalHeight = 0;
        var distance = 100;
        var articles = [];
        var timer = setInterval(() => {
          var scrollHeight = document.body.scrollHeight;

          window.scrollBy(0, distance);
          totalHeight += distance;
          console.log(articles.length);

          function uniq(a) {
            return Array.from(new Set(a));
          }
          console.log(ntweets);
          var _articles = Array.prototype.map.call(
            document.querySelectorAll("article"),
            (el) => el.textContent.trim()
          );
          articles.push.apply(articles, _articles);
          articles = uniq(articles);

          if (articles.length > ntweets) {
            clearInterval(timer);
            console.log("done");
            resolve(articles);
          }
        }, delay_in_ms);
      }).then(function (results) {
        return results;
      });
    },
    ntweets,
    delay_in_ms
  );

  return output;
}

const saveToDisk = (js_object, filepath) => {
  const absolutePath = path.resolve(filepath);
  let data = JSON.stringify(js_object);
  fs.writeFileSync(absolutePath, data);
};

const args = process.argv;
const drug_name = args[2];
const ntweets = args[3];
const delay_in_ms = args[4];
main(drug_name, ntweets, delay_in_ms);
