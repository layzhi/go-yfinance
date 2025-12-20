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

## Quick Start

```go
package main

import (
    "fmt"
    "log"

    "github.com/wnjoon/go-yfinance/pkg/models"
    "github.com/wnjoon/go-yfinance/pkg/ticker"
)

func main() {
    // Create a ticker
    t, err := ticker.New("AAPL")
    if err != nil {
        log.Fatal(err)
    }
    defer t.Close()

    // Get current quote
    quote, err := t.Quote()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("AAPL: $%.2f (%+.2f%%)\n",
        quote.RegularMarketPrice,
        quote.RegularMarketChangePercent)

    // Get historical data
    bars, err := t.History(models.HistoryParams{
        Period:   "1mo",
        Interval: "1d",
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("\nLast 5 days:\n")
    start := len(bars) - 5
    if start < 0 {
        start = 0
    }
    for _, bar := range bars[start:] {
        fmt.Printf("%s: O=%.2f H=%.2f L=%.2f C=%.2f V=%d\n",
            bar.Date.Format("2006-01-02"),
            bar.Open, bar.High, bar.Low, bar.Close, bar.Volume)
    }

    // Get company info
    info, err := t.Info()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("\nCompany: %s\n", info.LongName)
    fmt.Printf("Sector: %s\n", info.Sector)
    fmt.Printf("Industry: %s\n", info.Industry)
    fmt.Printf("Market Cap: $%d\n", info.MarketCap)
}
```

## Rate Limiting

> ⚠️ **Note**: This library does not enforce rate limiting internally. Yahoo Finance may block IP addresses with excessive request volume. To avoid `429 Too Many Requests` errors, manage concurrency on the client side using worker pools, semaphores, or request throttling.

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

- [DESIGN.md](./DESIGN.md) - Architecture and implementation roadmap
- [STATUS.md](./STATUS.md) - Current implementation progress and status

## Credits

This project is a Go implementation inspired by the Python library [yfinance](https://github.com/ranaroussi/yfinance).
Special thanks to [Ran Aroussi](https://github.com/ranaroussi) and all contributors of the original project for their excellent work.

### Dependencies

- [CycleTLS](https://github.com/Danny-Dasilva/CycleTLS) - TLS fingerprint spoofing
- [gorilla/websocket](https://github.com/gorilla/websocket) - WebSocket client for real-time streaming

## Disclaimer

> **Please read this carefully before using this library.**

1. **Unofficial API**: This library is **not affiliated with, endorsed by, or connected to Yahoo! Finance**. It wraps unofficial API endpoints intended for web browser consumption.

2. **Terms of Service**: Use of this library must comply with [Yahoo!'s Terms of Service](https://policies.yahoo.com/us/en/yahoo/terms/index.htm). Users are solely responsible for ensuring their usage is compliant.

3. **Risk of Blocking**: Since this library relies on unofficial methods, Yahoo! Finance may change their API structure or block IP addresses making excessive requests at any time without notice.

4. **No Warranty**: This software is provided "as is", without warranty of any kind, express or implied. The authors shall not be held liable for any damages or legal issues arising from the use of this software.

## License

MIT License
