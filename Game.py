import random

class StockGame:
    def __init__(self):
        self.balance = 10000
        self.portfolio = {}
        self.stock_market = {'AAPL': 150, 'GOOGL': 2500, 'AMZN': 3300, 'MSFT': 300}
        self.idle_cash_interest_rate = random.uniform(1.38, 5.88) / 100
        self.minimum_capital_requirement = 0.05
        self.margin_interest_rate = 0.015
        self.margin_buying_power_multiplier = 1.05

    def apply_interest_and_price_changes(self):
        self.balance *= (1 + self.idle_cash_interest_rate)

        # Apply interest on margin trading
        margin_balance = sum(self.portfolio[symbol]['shares'] for symbol in self.portfolio) * max(self.stock_market.values())
        margin_interest = margin_balance * self.margin_interest_rate

        if margin_balance < self.minimum_capital_requirement * self.balance:
            self.close_positions()
        elif margin_interest > 0:
            self.balance -= margin_interest

        # Apply price changes with random up and down within 10%
        for symbol in self.stock_market:
            price_change = random.uniform(-0.10, 0.10)
            self.stock_market[symbol] *= (1 + price_change)

    def close_positions(self):
        for symbol, data in self.portfolio.items():
            price = self.stock_market.get(symbol, 0)
            if data['shares'] > 0:  # Closing long position
                sell_proceeds = data['shares'] * price
                self.balance += sell_proceeds
            elif data['shares'] < 0:  # Closing short position
                buy_cost = abs(data['shares']) * data['buy_price']
                self.balance -= buy_cost
        self.portfolio = {}

    def display_menu(self):
        print("\nStock Game Menu:")
        print("1. View Stock Prices")
        print("2. Buy Stock")
        print("3. Sell Stock")
        print("4. View Portfolio")
        print("5. View Cash Balance and Buying Power")
        print("6. Deposit Funds")
        print("7. Withdraw Funds")
        print("8. View Earnings/Losses")
        print("9. Next Round")
        print("10. Quit")

    def view_stock_prices(self):
        print("\nStock Prices:")
        for symbol, price in self.stock_market.items():
            print(f"{symbol}: ${price:.2f}")

    def view_cash_balance(self):
        print(f"\nCash Balance: ${max(0, self.balance):.2f}")

    def view_buying_power(self):
        buying_power = self.calculate_buying_power()
        print(f"\nBuying Power: ${max(0, buying_power):.2f}")

    def deposit_funds(self):
        amount = float(input("Enter the amount to deposit: "))
        if amount > 0:
            self.balance += amount
            print(f"Successfully deposited ${amount:.2f}.")
        else:
            print("Invalid amount. Please enter a positive value.")

    def withdraw_funds(self):
        amount = float(input("Enter the amount to withdraw: "))
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Successfully withdrew ${amount:.2f}.")
        elif amount <= 0:
            print("Invalid amount. Please enter a positive value.")
        else:
            print("Insufficient funds for withdrawal.")

    def calculate_buying_power(self):
        return self.balance * self.margin_buying_power_multiplier

    def buy_stock(self):
        self.view_stock_prices()
        symbol = input("Enter the stock symbol you want to buy: ").upper()
        if symbol in self.stock_market:
            price = self.stock_market[symbol]
            max_shares = int(self.calculate_buying_power() / price)
            shares = int(input(f"Current price: ${price:.2f}\n"
                               f"You can buy up to {max_shares} shares. Enter the number of shares to buy: "))
            cost = shares * price
            if cost <= self.calculate_buying_power():
                self.balance -= cost
                if symbol in self.portfolio:
                    self.portfolio[symbol]['shares'] += shares
                else:
                    self.portfolio[symbol] = {'shares': shares, 'buy_price': price}
                print(f"You have successfully bought {shares} shares of {symbol} for ${cost:.2f}.")
            else:
                print("Insufficient buying power.")
        else:
            print("Invalid stock symbol.")

    def sell_stock(self):
        if not self.portfolio:
            print("Your portfolio is empty.")
            return

        print("\nYour Portfolio:")
        for symbol, data in self.portfolio.items():
            print(f"{symbol}: {data['shares']} shares")

        symbol = input("Enter the stock symbol you want to sell: ").upper()
        if symbol in self.portfolio:
            price = self.stock_market[symbol]
            shares = int(input(f"Current price: ${price:.2f}\n"
                               f"You have {self.portfolio[symbol]['shares']} shares. "
                               f"Enter the number of shares to sell: "))
            if shares <= self.portfolio[symbol]['shares']:
                self.balance += shares * price
                self.portfolio[symbol]['shares'] -= shares
                if self.portfolio[symbol]['shares'] == 0:
                    del self.portfolio[symbol]
                print(f"You have successfully sold {shares} shares of {symbol} for ${shares * price:.2f}.")
            else:
                print("You don't have enough shares to sell.")
        else:
            print("Invalid stock symbol.")

    def view_portfolio(self):
        print("\nYour Portfolio:")
        if not self.portfolio:
            print("Empty.")
        else:
            for symbol, data in self.portfolio.items():
                print(f"{symbol}: {data['shares']} shares, Buy Price: ${data['buy_price']:.2f}")

    def view_earnings_losses(self):
        total_value = 0
        total_cost = 0

        for symbol, data in self.portfolio.items():
            if symbol in self.stock_market:
                price = self.stock_market[symbol]
                value = data['shares'] * price
                cost = abs(data['shares']) * data['buy_price']
                total_value += value
                total_cost += cost

        earnings_losses = total_value - total_cost
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Total Portfolio Cost: ${total_cost:.2f}")
        print(f"Earnings/Losses: ${earnings_losses:.2f}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-10): ")

            if choice == '1':
                self.view_stock_prices()
            elif choice == '2':
                self.buy_stock()
            elif choice == '3':
                self.sell_stock()
            elif choice == '4':
                self.view_portfolio()
            elif choice == '5':
                self.view_cash_balance()
                self.view_buying_power()
            elif choice == '6':
                self.deposit_funds()
            elif choice == '7':
                self.withdraw_funds()
            elif choice == '8':
                self.view_earnings_losses()
            elif choice == '9':
                self.apply_interest_and_price_changes()
            elif choice == '10':
                print("Thank you for playing. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    game = StockGame()
    game.run()


