#!/usr/bin/env python3
"""
Compare go-yfinance output with Python yfinance output.

Usage:
    1. First run the Go example: go run cmd/example/main.go > go_output.txt
    2. Then run this script: python3 test/compare_with_python.py

This script will output the same data using Python yfinance for comparison.
"""

import sys
sys.path.insert(0, '..')  # Add parent directory to path for yfinance

import yfinance as yf

def main():
    symbol = "AAPL"

    print(f"=== Python yfinance: {symbol} ===\n")

    # Create ticker
    t = yf.Ticker(symbol)

    # 1. Current Quote (using fast_info)
    print("1. Current Quote")
    print("----------------")
    try:
        fast_info = t.fast_info
        print(f"Symbol: {symbol}")
        print(f"Price: ${fast_info.last_price:.2f}")
        print(f"Day Range: ${fast_info.day_low:.2f} - ${fast_info.day_high:.2f}")
        print(f"52 Week Range: ${fast_info.year_low:.2f} - ${fast_info.year_high:.2f}")
        print(f"Volume: {fast_info.last_volume}")
        print(f"Market Cap: ${int(fast_info.market_cap)}")
    except Exception as e:
        print(f"Error getting fast_info: {e}")
    print()

    # 2. Historical Data
    print("2. Historical Data (Last 10 Days)")
    print("----------------------------------")
    try:
        history = t.history(period="1mo", interval="1d", auto_adjust=True)
        print(f"{'Date':<12} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12}")
        for date, row in history.tail(10).iterrows():
            print(f"{date.strftime('%Y-%m-%d'):<12} {row['Open']:>10.2f} {row['High']:>10.2f} {row['Low']:>10.2f} {row['Close']:>10.2f} {int(row['Volume']):>12}")
    except Exception as e:
        print(f"Error getting history: {e}")
    print()

    # 3. Company Info
    print("3. Company Info")
    print("---------------")
    try:
        info = t.info
        print(f"Name: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Country: {info.get('country', 'N/A')}")
        print(f"Employees: {info.get('fullTimeEmployees', 'N/A')}")
        print(f"Website: {info.get('website', 'N/A')}")
        print(f"\nKey Statistics:")
        print(f"  Market Cap: ${info.get('marketCap', 'N/A')}")
        print(f"  Enterprise Value: ${info.get('enterpriseValue', 'N/A')}")
        print(f"  Trailing PE: {info.get('trailingPE', 'N/A'):.2f}" if info.get('trailingPE') else "  Trailing PE: N/A")
        print(f"  Forward PE: {info.get('forwardPE', 'N/A'):.2f}" if info.get('forwardPE') else "  Forward PE: N/A")
        print(f"  PEG Ratio: {info.get('pegRatio', 'N/A'):.2f}" if info.get('pegRatio') else "  PEG Ratio: N/A")
        print(f"  Price to Book: {info.get('priceToBook', 'N/A'):.2f}" if info.get('priceToBook') else "  Price to Book: N/A")
        print(f"  Revenue: ${info.get('totalRevenue', 'N/A')}")
        profit_margins = info.get('profitMargins')
        print(f"  Profit Margins: {profit_margins*100:.2f}%" if profit_margins else "  Profit Margins: N/A")
        print(f"  Recommendation: {info.get('recommendationKey', 'N/A')} ({info.get('recommendationMean', 'N/A')})")
    except Exception as e:
        print(f"Error getting info: {e}")
    print()

    # 4. Dividends
    print("4. Recent Dividends")
    print("-------------------")
    try:
        dividends = t.dividends
        if len(dividends) > 0:
            for date, amount in dividends.tail(5).items():
                print(f"{date.strftime('%Y-%m-%d')}: ${amount:.4f}")
        else:
            print("No dividend history")
    except Exception as e:
        print(f"Error getting dividends: {e}")
    print()

    # 5. Splits
    print("5. Stock Splits")
    print("---------------")
    try:
        splits = t.splits
        if len(splits) > 0:
            for date, ratio in splits.items():
                print(f"{date.strftime('%Y-%m-%d')}: {ratio}:1")
        else:
            print("No split history")
    except Exception as e:
        print(f"Error getting splits: {e}")
    print()

    print("=== Python yfinance Complete ===")

if __name__ == "__main__":
    main()
