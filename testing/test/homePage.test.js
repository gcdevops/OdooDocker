/* eslint-disable no-unused-vars */

const {
    describe,
    it,
    before,
    afterEach
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

                await page.visit('/web/login');
            });

            afterEach(async () => {
                await page.quit();

            });

            it('find the input box and log in button', async () => {
                await page.findInputAndButton();

            });

            it('add username, password and click login button', async () => {
                await page.submitBtnAndLogIn();
            });

            it('navigate to the employee page', async () => {
                await page.navigateEmployeePage();
            });

            it('edit employee', async () => {
                await page.editEmployee();
            });

        });
    } catch (ex) {
        console.log(new Error(ex.message));
    } finally {
        page.quit();
    }
})();