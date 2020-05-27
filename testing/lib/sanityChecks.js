/* global driver */
/* eslint-disable no-useless-escape */

var Page = require('./basePage');
const webdriver = require('selenium-webdriver');

let submitBtn, navMenu, employeesBtn, selectEmployee, editBtn, saveBtn;

Page.prototype.findInputAndButton = async function () {
    await this.findById('login');
    await this.findById('password');
    submitBtn = await this.findByClassName('btn');
};

Page.prototype.submitBtnAndLogIn = async function () {
    await this.findInputAndButton();
    await this.write('login', process.env.ODOO_TEST_USER);
    await this.write('password', process.env.ODOO_TEST_PASSWORD);
    return await submitBtn.click();
}

Page.prototype.navigateEmployeePage = async function () {
    await this.submitBtnAndLogIn();
    navMenu = await this.findByClassName('o_menu_apps');
    employeesBtn = await this.findByCss('a[href*=\"#menu_id=95\"]');
    await navMenu.click();
    await employeesBtn.click();
};

Page.prototype.selectEmployee = async function () {
    await this.navigateEmployeePage();
    await this.findByCss('.o_searchview_input');
    await driver.findElement(webdriver.By.css('.o_searchview_input')).sendKeys('Smith, Brad\n');
    selectEmployee = await this.findByCss('td[title*=\"Smith, Brad\"]');
    await selectEmployee.click();
}

Page.prototype.editEmployee = async function () {
    await this.selectEmployee();
    editBtn = await this.findByCss('.o_form_button_edit');
    await editBtn.click();
    await this.findByCss('.o_field_email');
    await driver.findElement(webdriver.By.css('.o_field_email')).sendKeys('Brad@example.com');
    saveBtn = await this.findByCss('.o_form_button_save');
    await saveBtn.click();
}
module.exports = Page;