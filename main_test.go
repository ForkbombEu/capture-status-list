package main

import "testing"

func TestHeaderIsPresent(t *testing.T) {
	if header == "" {
		t.Fatal("expected ASCII art header")
	}
}
