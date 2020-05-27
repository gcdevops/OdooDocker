const webdriver = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const path = require('chromedriver').path;
const proxy = require('selenium-webdriver/proxy');

var service = new chrome.ServiceBuilder(path).build();
chrome.setDefaultService(service);

var o = new chrome.Options();
o.addArguments('disable-infobars');
o.setUserPreferences({
    credential_enable_service: false
});

var Page = function() {

    var chromeDriverBuilder = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome());
    chromeDriverBuilder = chromeDriverBuilder.setChromeOptions(o.addArguments('--headless', '--disable-extensions','--no-sandbox', '--whitelisted-ips'));

    if (process.env.SECURITY_MODE === 'true') {
        chromeDriverBuilder.setProxy(proxy.manual({http: `${process.env.ZAP_ADDR}`},{https: `${process.env.ZAP_ADDR}`}))
    }

    var driver = chromeDriverBuilder.build();

    this.baseUrl = function() {
        return `${process.env.SITE_URL}`;
    }

    // visit a webpage
    this.visit = async function(theUrl) {
        return await driver.get(this.baseUrl() + theUrl);
    };

    // quit current session
    this.quit = async function () {
        return await driver.quit();
    };

    // get the session cookies
    this.deleteCookies = async function () {
        return await driver.manage().deleteAllCookies();
    }

    // wait and find a specific element with it's id
    this.findById = async function (id) {
        await driver.wait(webdriver.until.elementLocated(webdriver.By.id(id)), 5000)
        return await driver.findElement(webdriver.By.id(id));
    };

    // wait and find a specific element with it's name
    this.findByName = async function (name) {
        await driver.wait(webdriver.until.elementLocated(webdriver.By.name(name)), 5000)
        return await driver.findElement(webdriver.By.name(name));
    };

    // wait and find a specific element with it's className
    this.findByClassName = async function (c) {
        await driver.wait(webdriver.until.elementLocated(webdriver.By.className(c)), 5000)
        return await driver.findElement(webdriver.By.className(c));
    };

    // wait and find a specific element with it's css selector
    this.findByCss = async function (item) {
        await driver.wait(webdriver.until.elementLocated(webdriver.By.css(item)), 5000)
        return await driver.findElement(webdriver.By.css(item));
    }

    // fill input web elements
    this.write = async function (el, txt) {
        return await driver.findElement(webdriver.By.id(el)).sendKeys(txt);
    };
};

module.exports = Page;