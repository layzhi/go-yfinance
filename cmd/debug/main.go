// Debug authentication flow
package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/Danny-Dasilva/CycleTLS/cycletls"
)

const ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0"
const userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

func main() {
	fmt.Println("=== Debug: Authentication Flow ===\n")

	client := cycletls.Init()
	defer client.Close()

	// Step 1: Get cookie from fc.yahoo.com
	fmt.Println("Step 1: GET https://fc.yahoo.com")
	resp, err := client.Do("https://fc.yahoo.com", cycletls.Options{
		Ja3:       ja3,
		UserAgent: userAgent,
		Headers: map[string]string{
			"Accept":          "*/*",
			"Accept-Language": "en-US,en;q=0.5",
		},
	}, "GET")
	if err != nil {
		log.Fatalf("Failed to get cookie: %v", err)
	}
	fmt.Printf("Status: %d\n", resp.Status)
	fmt.Printf("Headers: %v\n", resp.Headers)

	// Look for Set-Cookie header
	var cookie string
	for key, value := range resp.Headers {
		if strings.ToLower(key) == "set-cookie" {
			cookie = value
			fmt.Printf("Set-Cookie: %s\n", value)
			break
		}
	}
	fmt.Println()

	// Step 2: Get crumb
	fmt.Println("Step 2: GET https://query1.finance.yahoo.com/v1/test/getcrumb")
	headers := map[string]string{
		"Accept":          "*/*",
		"Accept-Language": "en-US,en;q=0.5",
	}
	if cookie != "" {
		headers["Cookie"] = cookie
	}

	resp, err = client.Do("https://query1.finance.yahoo.com/v1/test/getcrumb", cycletls.Options{
		Ja3:       ja3,
		UserAgent: userAgent,
		Headers:   headers,
	}, "GET")
	if err != nil {
		log.Fatalf("Failed to get crumb: %v", err)
	}
	fmt.Printf("Status: %d\n", resp.Status)
	fmt.Printf("Body: %s\n", resp.Body)
	fmt.Printf("Is HTML: %v\n", strings.Contains(resp.Body, "<html>"))

	crumb := strings.TrimSpace(resp.Body)
	if crumb == "" || strings.Contains(crumb, "<html>") {
		fmt.Println("\nCrumb fetch failed!")
		return
	}
	fmt.Printf("\nCrumb: %s\n\n", crumb)

	// Step 3: Test API with crumb
	fmt.Println("Step 3: Test Quote API")
	url := fmt.Sprintf("https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL&crumb=%s", crumb)
	resp, err = client.Do(url, cycletls.Options{
		Ja3:       ja3,
		UserAgent: userAgent,
		Headers:   headers,
	}, "GET")
	if err != nil {
		log.Fatalf("Failed to get quote: %v", err)
	}
	fmt.Printf("Status: %d\n", resp.Status)
	if len(resp.Body) > 500 {
		fmt.Printf("Body (truncated): %s...\n", resp.Body[:500])
	} else {
		fmt.Printf("Body: %s\n", resp.Body)
	}

	fmt.Println("\n=== Debug Complete ===")
}
