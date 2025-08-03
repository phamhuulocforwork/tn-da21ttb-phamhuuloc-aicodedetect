#!/usr/bin/env python3
"""
Debug script để hiểu chi tiết detection logic
"""
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.ml_integration import analyze_code_features, detect_ai_code, ai_detector

def debug_detection(code: str, language: str = "cpp"):
    """Debug detection step by step"""
    print("🔍 DEBUGGING AI DETECTION LOGIC")
    print("=" * 50)
    
    # Extract features
    print("📊 EXTRACTING FEATURES...")
    features = analyze_code_features(code, language)
    for key, value in features.items():
        print(f"   {key}: {value}")
    
    print("\n🤖 CHECKING AI PATTERNS...")
    ai_score = 0.0
    ai_reasons = []
    
    for i, pattern_func in enumerate(ai_detector.ai_patterns):
        score, reason = pattern_func(code, features)
        ai_score += score
        print(f"   Pattern {i+1}: +{score:0.3f} - {reason if reason else 'No match'}")
        if reason:
            ai_reasons.append(reason)
    
    print(f"\n👤 CHECKING HUMAN PATTERNS...")
    human_reasons = []
    
    for i, pattern_func in enumerate(ai_detector.human_patterns):
        score, reason = pattern_func(code, features)
        ai_score -= score
        print(f"   Pattern {i+1}: -{score:0.3f} - {reason if reason else 'No match'}")
        if reason:
            human_reasons.append(reason)
    
    print(f"\n📈 FINAL SCORING...")
    print(f"   Raw AI Score: {ai_score:0.3f}")
    
    # Normalize
    ai_score_normalized = max(0.0, min(1.0, ai_score))
    print(f"   Normalized AI Score: {ai_score_normalized:0.3f}")
    
    # Make prediction
    if ai_score_normalized > 0.6:
        prediction = "AI-generated"
        confidence = ai_score_normalized
        print(f"   → AI-generated (confidence: {confidence:0.3f})")
    elif ai_score_normalized < 0.4:
        prediction = "Human-written"
        confidence = 1.0 - ai_score_normalized
        print(f"   → Human-written (confidence: {confidence:0.3f})")
    else:
        prediction = "Uncertain"
        confidence = 0.5
        print(f"   → Uncertain (confidence: {confidence:0.3f})")
    
    print(f"\n📝 REASONING:")
    print(f"   AI indicators found: {len(ai_reasons)}")
    for reason in ai_reasons:
        print(f"     • {reason}")
    print(f"   Human indicators found: {len(human_reasons)}")
    for reason in human_reasons:
        print(f"     • {reason}")
    
    # Test actual function
    print(f"\n✅ ACTUAL API RESULT:")
    prediction_api, confidence_api, reasoning_api = detect_ai_code(code, features)
    print(f"   Prediction: {prediction_api}")
    print(f"   Confidence: {confidence_api}")
    print(f"   Reasoning: {reasoning_api}")
    
    return features, prediction_api, confidence_api, reasoning_api

def main():
    # Test với sample code có template pattern
    print("🧪 TEST CASE 1: Code có template pattern")
    code1 = '''#include <stdio.h>
#include <stdlib.h>

int main() {
    int a, b, c;
    scanf("%d %d", &a, &b);
    c = a + b;
    printf("%d\\n", c);
    return 0;
}'''
    
    debug_detection(code1, "cpp")
    
    print("\n" + "="*70 + "\n")
    
    # Test với AI-like code
    print("🧪 TEST CASE 2: AI-like code")
    code2 = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to calculate sum of two numbers
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
    
    // Calculate the sum using our function
    resultSum = calculateSum(userInput1, userInput2);
    
    // Display the final result
    printf("The sum is: %d\\n", resultSum);
    
    return 0;
}'''
    
    debug_detection(code2, "cpp")

if __name__ == "__main__":
    main()