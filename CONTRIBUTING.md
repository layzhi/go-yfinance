# Development Guidelines

This document outlines the development workflow and guidelines for go-yfinance.

## Phase Development Workflow

### 1. Branch Creation

```bash
# Create phase branch from main
git checkout main
git pull origin main
git checkout -b phase{N}/{feature-name}

# Create feature sub-branches as needed
git checkout -b phase{N}/{sub-feature}
```

### 2. Implementation

- Follow existing code patterns and structure
- Use idiomatic Go conventions
- Add appropriate error handling
- Implement caching where beneficial

### 3. Testing

- Write unit tests for all new functionality
- Include table-driven tests where appropriate
- Test edge cases and error conditions
- Run tests before committing:

```bash
go test ./... -v
```

### 4. Documentation

- Use gomarkdoc standard for documentation comments
- Update `pkg/ticker/doc.go` with new methods
- Update `pkg/models/doc.go` with new types
- Update `STATUS.md` with completion status

### 5. API Consistency Check

**Before proceeding to the next phase, verify consistency with Python yfinance:**

| Check Item | Description |
|------------|-------------|
| Method Names | Go method names should match Python method names (PascalCase conversion) |
| Parameters | Input parameters should match Python's interface |
| Return Types | Output data structures should contain equivalent fields |

**Python yfinance reference methods:**

| Python | Go |
|--------|-----|
| `ticker.major_holders` | `MajorHolders()` |
| `ticker.institutional_holders` | `InstitutionalHolders()` |
| `ticker.mutualfund_holders` | `MutualFundHolders()` |
| `ticker.insider_transactions` | `InsiderTransactions()` |
| `ticker.insider_roster_holders` | `InsiderRosterHolders()` |
| `ticker.insider_purchases` | `InsiderPurchases()` |
| `ticker.calendar` | `Calendar()` |
| `ticker.recommendations` | `Recommendations()` |
| `ticker.analyst_price_targets` | `AnalystPriceTargets()` |
| `ticker.earnings_estimate` | `EarningsEstimate()` |
| `ticker.revenue_estimate` | `RevenueEstimate()` |
| `ticker.eps_trend` | `EPSTrend()` |
| `ticker.eps_revisions` | `EPSRevisions()` |
| `ticker.earnings_history` | `EarningsHistory()` |
| `ticker.growth_estimates` | `GrowthEstimates()` |

### 6. Merge to Main

```bash
# Merge feature branches to phase branch
git checkout phase{N}/{feature-name}
git merge phase{N}/{sub-feature}

# Merge phase branch to main
git checkout main
git merge phase{N}/{feature-name}
```

### 7. Push and Verify Documentation

**After merging to main:**

1. Push to remote:
```bash
git push origin main
```

2. Wait for CI/CD to complete (GitHub Actions)

3. Verify documentation was generated correctly:
   - Check `docs/API.md` was updated
   - Review generated documentation for accuracy

4. Only proceed to next phase after verification

## Code Style Guidelines

### Naming Conventions

- Use PascalCase for exported functions and types
- Use camelCase for unexported functions and variables
- Use descriptive names that match Python yfinance where applicable

### Error Handling

- Return errors instead of panicking
- Wrap errors with context using `fmt.Errorf("context: %w", err)`
- Use typed errors where appropriate

### Caching

- Cache API responses to minimize redundant requests
- Provide cache clearing methods
- Document caching behavior

### Documentation Comments

```go
// MethodName does something important.
//
// Detailed description of what the method does.
//
// Example:
//
//	result, err := ticker.MethodName()
//	if err != nil {
//	    log.Fatal(err)
//	}
//	fmt.Println(result)
func (t *Ticker) MethodName() (*Result, error) {
    // implementation
}
```

### Deprecation

When renaming methods, keep the old method as a deprecated alias:

```go
// NewMethod is the current implementation.
func (t *Ticker) NewMethod() (*Result, error) {
    // implementation
}

// OldMethod is deprecated. Use NewMethod instead.
//
// Deprecated: Use NewMethod instead.
func (t *Ticker) OldMethod() (*Result, error) {
    return t.NewMethod()
}
```

## Pre-Phase Checklist

Before starting a new phase:

- [ ] Previous phase is merged to main
- [ ] Previous phase is pushed to remote
- [ ] CI/CD documentation generation completed
- [ ] Documentation verified for accuracy
- [ ] API consistency with Python yfinance verified

## Post-Phase Checklist

After completing a phase:

- [ ] All tests pass
- [ ] Documentation updated (doc.go, STATUS.md)
- [ ] API consistency verified with Python yfinance
- [ ] Code merged to main
- [ ] Changes pushed to remote
- [ ] CI/CD documentation generation verified
- [ ] Ready for next phase
