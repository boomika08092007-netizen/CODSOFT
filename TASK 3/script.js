/**
 * ATM Machine Simulation - Web Version
 * Core Logic using ES6 Classes
 */

class BankAccount {
    constructor(initialBalance = 10000) {
        this._balance = initialBalance;
    }

    get balance() {
        return this._balance;
    }

    deposit(amount) {
        if (amount <= 0) return { success: false, message: "Invalid Input" };
        this._balance += amount;
        return { success: true, message: "Transaction Successful" };
    }

    withdraw(amount) {
        if (amount <= 0) return { success: false, message: "Invalid Input" };
        if (amount > this._balance) return { success: false, message: "Insufficient Balance" };
        
        this._balance -= amount;
        return { success: true, message: "Transaction Successful" };
    }
}

class ATMController {
    constructor() {
        this.account = new BankAccount(12500.75);
        this.currentAction = null;
        
        // DOM Elements
        this.screens = {
            welcome: document.getElementById('welcome-screen'),
            menu: document.getElementById('menu-screen'),
            action: document.getElementById('action-screen')
        };
        
        this.elements = {
            balanceDisplay: document.getElementById('display-balance'),
            amountInput: document.getElementById('amount-input'),
            actionTitle: document.getElementById('action-title'),
            actionDesc: document.getElementById('action-desc'),
            quickAmounts: document.getElementById('quick-amounts'),
            notification: document.getElementById('notification'),
            notifMsg: document.getElementById('notif-message'),
            notifIcon: document.getElementById('notif-icon'),
            dateTime: document.getElementById('date-time')
        };

        this.init();
    }

    init() {
        this.updateDateTime();
        setInterval(() => this.updateDateTime(), 60000);
        this.bindEvents();
    }

    updateDateTime() {
        const now = new Date();
        this.elements.dateTime.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    bindEvents() {
        // Start Session
        document.getElementById('start-btn').addEventListener('click', () => {
            this.showScreen('menu');
            this.updateBalanceUI();
        });

        // Menu Actions
        document.querySelectorAll('.menu-item').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = btn.dataset.action;
                if (action === 'exit') {
                    this.logout();
                } else if (action === 'balance') {
                    this.showNotification('Current Balance: ' + this.formatCurrency(this.account.balance), 'success');
                } else {
                    this.prepareAction(action);
                }
            });
        });

        // Action Screen
        document.getElementById('back-btn').addEventListener('click', () => this.showScreen('menu'));
        document.getElementById('confirm-btn').addEventListener('click', () => this.handleTransaction());

        // Quick Amount Buttons
        this.elements.quickAmounts.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-btn')) {
                this.elements.amountInput.value = e.target.dataset.value;
            }
        });
    }

    showScreen(screenName) {
        Object.values(this.screens).forEach(s => s.classList.remove('active'));
        this.screens[screenName].classList.add('active');
    }

    updateBalanceUI() {
        this.elements.balanceDisplay.textContent = this.formatCurrency(this.account.balance);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }

    prepareAction(action) {
        this.currentAction = action;
        this.elements.amountInput.value = '';
        
        if (action === 'withdraw') {
            this.elements.actionTitle.textContent = "Withdraw Cash";
            this.elements.actionDesc.textContent = "Select or enter an amount to withdraw";
            this.renderQuickAmounts([500, 1000, 2000, 5000, 10000]);
        } else {
            this.elements.actionTitle.textContent = "Deposit Cash";
            this.elements.actionDesc.textContent = "Enter the amount you wish to deposit";
            this.renderQuickAmounts([1000, 5000, 10000, 20000, 50000]);
        }
        
        this.showScreen('action');
    }

    renderQuickAmounts(amounts) {
        this.elements.quickAmounts.innerHTML = amounts
            .map(amt => `<button class="quick-btn" data-value="${amt}">₹${amt}</button>`)
            .join('');
    }

    handleTransaction() {
        const amount = parseFloat(this.elements.amountInput.value);
        
        if (isNaN(amount) || amount <= 0) {
            this.showNotification('Invalid Input', 'error');
            return;
        }

        const result = this.currentAction === 'withdraw' 
            ? this.account.withdraw(amount)
            : this.account.deposit(amount);

        if (result.success) {
            this.showNotification(result.message, 'success');
            this.updateBalanceUI();
            this.showScreen('menu');
        } else {
            this.showNotification(result.message, 'error');
        }
    }

    showNotification(message, type) {
        this.elements.notifMsg.textContent = message;
        this.elements.notification.className = `notification show notif-${type}`;
        this.elements.notifIcon.textContent = type === 'success' ? '✔' : '✕';

        setTimeout(() => {
            this.elements.notification.classList.remove('show');
        }, 3000);
    }

    logout() {
        this.showNotification('Session Ended. Goodbye!', 'success');
        setTimeout(() => {
            this.showScreen('welcome');
        }, 1000);
    }
}

// Initialize the ATM App
document.addEventListener('DOMContentLoaded', () => {
    window.atmApp = new ATMController();
});
