package main

import "fmt"

const header = `
 __  __            _      _____ _____ _
|  \/  | ___   ___| | __ |_   _/ ____| |
| |\/| |/ _ \ / __| |/ /   | || (___ | |
| |  | | (_) | (__|   <    | | \___ \| |
|_|  |_|\___/ \___|_|\_\   |_| ____) |_|
`

func main() {
	fmt.Print(header)
	fmt.Println("Mock EUDI Token Status List server")
	fmt.Println("Run the FastAPI service with: uvicorn app:app --reload")
}
