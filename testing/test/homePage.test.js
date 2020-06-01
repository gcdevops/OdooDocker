/* eslint-disable no-unused-vars */


/**
 * TODO: 
 * 1. Fix select employee function in sanityChecks - select only the first employee
 * 2. Fix edit employee - edit only the first employee
 * 3. Adjust screenshots - take screenshots where needed 
 * 
*/

const {
    describe,
    it,
    before,
    beforeEach
} = require('mocha');
const Page = require('../lib/sanityChecks');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

chai.use(chaiAsPromised);


process.on('unhandledRejection', () => {});

(async function example() {
    let driver, page;
    try {
        describe('Log in Page', async function () {
            this.timeout(50000);
            

            before(async () => {
                page = new Page();
                driver = page.driver;
            });

            beforeEach(async () => {
                await page.clearBrowserData();
                await page.visit('/web/login');
                await page.takeScreenShot('loginpage');

            });

            it('find the input box and log in button', async () => {
                await page.findInputAndButton();
            });

            it('add username, password and click login button', async () => {
                await page.submitBtnAndLogIn();
            });

            it('navigate to the employee page', async () => {
                await page.navigateEmployeePage();
                await page.takeScreenShot('navigate to employee');
            });

            it('edit employee', async () => {
                await page.editEmployee();
                await page.takeScreenShot('select employee');
            });

        });
    } catch (ex) {
        console.log(new Error(ex.message));
    } finally {
        page.quit();
    }
})();