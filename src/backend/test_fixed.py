#!/usr/bin/env python3
"""
Test fixed reasoning logic
"""
import requests
import json

def test_fixed_reasoning():
    """Test với sample code để verify fix"""
    
    # Case 1: Code có template nhưng overall human-like
    human_code = '''#include <stdio.h>

int main() {
    int a, b, c;
    scanf("%d %d", &a, &b);
    c = a + b;
    printf("%d", c);
    return 0;
}'''

    # Case 2: Code rõ ràng AI-like
    ai_code = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to calculate sum of two numbers
int calculateSum(int firstNumber, int secondNumber) {
    // Return the sum of both parameters
    return firstNumber + secondNumber;
}

// Function to get user input
void getUserInput(int* number, const char* prompt) {
    // Display prompt to user
    printf("%s", prompt);
    // Read integer from user
    scanf("%d", number);
}

int main() {
    int userInputFirst, userInputSecond;
    int calculatedResult;
    
    // Get first number from user
    getUserInput(&userInputFirst, "Enter first number: ");
    
    // Get second number from user  
    getUserInput(&userInputSecond, "Enter second number: ");
    
    // Calculate the sum using our dedicated function
    calculatedResult = calculateSum(userInputFirst, userInputSecond);
    
    // Display the final result to user
    printf("The calculated sum is: %d\\n", calculatedResult);
    
    return 0;
}'''

    test_cases = [
        ("Human-like code (có template)", human_code),
        ("AI-like code (descriptive)", ai_code)
    ]

    for name, code in test_cases:
        print(f"\\n🧪 {name}")
        print("=" * 50)
        
        try:
            response = requests.post("http://localhost:8000/analyze-code", json={
                "code": code,
                "language": "cpp"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"Prediction: {data['detection']['prediction']}")
                print(f"Confidence: {data['detection']['confidence']}")
                print(f"Features:")
                print(f"  LOC: {data['features']['loc']}")
                print(f"  Comment ratio: {data['features']['comment_ratio']:.3f}")
                print(f"  Cyclomatic avg: {data['features']['cyclomatic_avg']}")
                print(f"Reasoning:")
                for reason in data['detection']['reasoning']:
                    print(f"  • {reason}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_fixed_reasoning()