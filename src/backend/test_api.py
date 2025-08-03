#!/usr/bin/env python3
"""
Test script để kiểm tra API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful:")
            print(f"   Status: {data['status']}")
            print(f"   ML Features: {data['ml_features_available']}")
            print(f"   Uptime: {data['uptime']:.2f}s")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_analyze_code():
    """Test analyze-code endpoint với sample C code"""
    print("\n🔍 Testing /analyze-code endpoint...")
    
    # Sample AI-like code (descriptive names, comments, clean structure)
    ai_code = '''#include <stdio.h>
#include <stdlib.h>

// Function to calculate the sum of two numbers
int calculateSum(int firstNumber, int secondNumber) {
    // Return the sum of both parameters
    return firstNumber + secondNumber;
}

int main() {
    int userInput1, userInput2;
    int resultSum;
    
    // Get input from user
    printf("Enter first number: ");
    scanf("%d", &userInput1);
    
    printf("Enter second number: ");
    scanf("%d", &userInput2);
    
    // Calculate the sum
    resultSum = calculateSum(userInput1, userInput2);
    
    // Display the result
    printf("The sum is: %d\\n", resultSum);
    
    return 0;
}'''

    # Sample Human-like code (short vars, minimal comments)
    human_code = '''#include <stdio.h>

int main() {
    int a, b, c;
    scanf("%d %d", &a, &b);
    c = a + b;
    printf("%d", c);
    return 0;
}'''

    test_cases = [
        ("AI-like code", ai_code, "cpp"),
        ("Human-like code", human_code, "c")
    ]
    
    for name, code, lang in test_cases:
        print(f"\n🧪 Testing {name}...")
        try:
            payload = {
                "code": code,
                "language": lang,
                "filename": f"test.{lang}"
            }
            
            response = requests.post(f"{BASE_URL}/analyze-code", json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Analysis successful:")
                print(f"   Prediction: {data['detection']['prediction']}")
                print(f"   Confidence: {data['detection']['confidence']}")
                print(f"   LOC: {data['features']['loc']}")
                print(f"   Processing time: {data['processing_time']:.3f}s")
                print(f"   Reasoning: {data['detection']['reasoning'][:2]}")  # First 2 reasons
            else:
                print(f"❌ Analysis failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Analysis error: {e}")

def test_submit_feedback():
    """Test submit-feedback endpoint"""
    print("\n📝 Testing /submit-feedback endpoint...")
    
    try:
        payload = {
            "code": "int main() { return 0; }",
            "predicted_label": "AI-generated",
            "actual_label": "Human-written",
            "feedback_notes": "Test feedback from API test script"
        }
        
        response = requests.post(f"{BASE_URL}/submit-feedback", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Feedback submitted successfully:")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Feedback failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Feedback error: {e}")

def main():
    print("🚀 Starting API Tests...")
    print(f"Testing API at: {BASE_URL}")
    
    # Test endpoints in sequence
    if test_health():
        test_analyze_code()
        test_submit_feedback()
    else:
        print("❌ Health check failed. Make sure server is running.")
        print("   Run: cd src/backend && make dev")
    
    print("\n✨ API tests completed!")

if __name__ == "__main__":
    main()