
# AI Code Detection Evaluation Report
## Method: Rule-Based

### Summary Statistics
- **Total Samples**: 200
- **Correct Predictions**: 111
- **Overall Accuracy**: 55.50%

### Performance Metrics
- **Precision**: 0.545 (Of predicted AI, how many are actually AI)
- **Recall (Sensitivity)**: 0.606 (Of actual AI, how many detected)
- **F1-Score**: 0.574 (Harmonic mean of precision & recall)
- **Specificity**: 0.505 (Of actual Human, how many correctly identified)
- **Balanced Accuracy**: 0.555 (Average of sensitivity & specificity)

### Confidence Analysis
- **Average Confidence**: 0.602
- **Confidence Calibration**: 0.080 (How well confidence correlates with correctness)

### Confusion Matrix
```
                 Predicted
                AI    Human
Actual   AI     60      39
        Human   50      51
```

### Error Analysis
\n#### Common Error Patterns (89 errors)\n\n**False Positives** (50): Human code predicted as AI\n- submission_5281.c: Formatting nhất quán (score: +0.150)\n- submission_3185.c: Tên biến mô tả chi tiết (score: +0.250)\n- submission_5428.c: Formatting nhất quán (score: +0.150)\n\n**False Negatives** (2): AI code predicted as Human\n- submission_11.cpp: Formatting nhất quán (score: +0.150)\n- submission_32.c: Formatting nhất quán (score: +0.150)\n\n### Advanced Metrics\n- **AUC-ROC**: 0.630\n- **Average Precision**: 0.709\n