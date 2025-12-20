.PHONY: build test lint docs clean help

# Default target
all: build

# Build the project
build:
	go build ./...

# Run tests
test:
	go test -v -race ./...

# Run tests with coverage
test-cover:
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Run linter
lint:
	golangci-lint run --timeout=5m

# Generate API documentation using gomarkdoc
docs:
	@echo "Generating API documentation..."
	@mkdir -p docs
	gomarkdoc --output docs/API.md ./pkg/...
	@echo "Documentation generated at docs/API.md"

# Clean build artifacts
clean:
	rm -f coverage.out coverage.html
	go clean

# Show help
help:
	@echo "Available targets:"
	@echo "  build      - Build the project"
	@echo "  test       - Run tests"
	@echo "  test-cover - Run tests with coverage report"
	@echo "  lint       - Run golangci-lint"
	@echo "  docs       - Generate API documentation (gomarkdoc)"
	@echo "  clean      - Clean build artifacts"
	@echo "  help       - Show this help message"
