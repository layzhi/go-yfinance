# go-yfinance

Go implementation of Yahoo Finance API client, inspired by Python's [yfinance](https://github.com/ranaroussi/yfinance).

## Features

- **TLS Fingerprint Spoofing**: Uses CycleTLS to bypass Yahoo's bot detection with Chrome JA3 fingerprint
- **Automatic Authentication**: Cookie/Crumb management with CSRF fallback for EU users
- **Thread-Safe**: Concurrent-safe client and configuration
- **Comprehensive Error Handling**: Typed errors with proper Go error wrapping

## Installation

```bash
go get github.com/wnjoon/go-yfinance
```

## Implementation Status

- [x] **Phase 0: Foundation**
  - [x] CycleTLS-based HTTP client with Chrome TLS fingerprint
  - [x] Cookie/Crumb authentication system
  - [x] CSRF consent flow fallback (for EU users)
  - [x] Comprehensive error handling
  - [x] Configuration management
- [ ] **Phase 1: Core Data** (Quote, History, Info)
- [ ] **Phase 2: Options**
- [ ] **Phase 3: Financials**
- [ ] **Phase 4: Analysis**
- [ ] **Phase 5: Holdings & Actions**
- [ ] **Phase 6: Search & Screener**
- [ ] **Phase 7: Multi-ticker & Batch**
- [ ] **Phase 8: Real-time WebSocket**
- [ ] **Phase 9: Advanced Features**

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/wnjoon/go-yfinance/pkg/ticker"
)

func main() {
    // Create a ticker
    t := ticker.New("AAPL")
    defer t.Close()

    // Get current quote
    quote, err := t.Quote()
    if err != nil {
        panic(err)
    }
    fmt.Printf("AAPL: $%.2f\n", quote.RegularMarketPrice)

    // Get historical data
    history, err := t.History(ticker.HistoryParams{
        Period:   "1mo",
        Interval: "1d",
    })
    if err != nil {
        panic(err)
    }
    for _, bar := range history {
        fmt.Printf("%s: O=%.2f H=%.2f L=%.2f C=%.2f V=%d\n",
            bar.Date.Format("2006-01-02"),
            bar.Open, bar.High, bar.Low, bar.Close, bar.Volume)
    }

    // Get company info
    info, err := t.Info()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Company: %s\n", info.LongName)
    fmt.Printf("Market Cap: %d\n", info.MarketCap)
}
```

## Configuration

```go
import "github.com/wnjoon/go-yfinance/pkg/config"

// Global configuration
cfg := config.Get()
cfg.SetTimeout(60 * time.Second).
    SetMaxRetries(5).
    SetDebug(true)

// Or create custom config
customCfg := config.NewDefault().
    SetProxy("http://proxy:8080").
    EnableCache(10 * time.Minute)
```

## Project Structure

```
go-yfinance/
├── cmd/example/              # Usage examples
├── internal/
│   └── endpoints/            # Yahoo Finance API endpoints
├── pkg/
│   ├── client/               # HTTP client with TLS fingerprint
│   │   ├── client.go         # CycleTLS-based client
│   │   ├── auth.go           # Cookie/Crumb authentication
│   │   └── errors.go         # Error types
│   ├── config/               # Configuration management
│   ├── ticker/               # Ticker data (Phase 1+)
│   └── models/               # Data models (Phase 1+)
├── DESIGN.md                 # Detailed design document
└── README.md
```

## Documentation

See [DESIGN.md](./DESIGN.md) for detailed architecture and implementation roadmap.

## License

MIT License

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - The original Python library
- [CycleTLS](https://github.com/Danny-Dasilva/CycleTLS) - TLS fingerprint spoofing
