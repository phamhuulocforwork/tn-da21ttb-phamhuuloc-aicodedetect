from typing import Dict, List
from .main import FeatureGroup

def prepare_boxplot_data(feature_groups: Dict[str, FeatureGroup]) -> Dict[str, Dict]:
    """Prepare data for chartjs-chart-boxplot visualization"""
    boxplot_data = {}
    
    for group_name, group in feature_groups.items():
        if not group.features:
            continue
            
        
        values = [f.value for f in group.features]
        feature_names = [f.name for f in group.features]
        
        if len(values) < 5:  
            continue
            
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        min_val = sorted_values[0]
        q1 = sorted_values[n // 4]
        median = sorted_values[n // 2]
        q3 = sorted_values[3 * n // 4]
        max_val = sorted_values[-1]     
        
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        outliers = [v for v in sorted_values if v < lower_fence or v > upper_fence]
        
        boxplot_data[group_name] = {
            "label": group.group_name,
            "data": [{
                "min": min_val,
                "q1": q1,
                "median": median,
                "q3": q3,
                "max": max_val,
                "outliers": outliers,
                "mean": sum(values) / len(values),
                "std": (sum((x - sum(values) / len(values))**2 for x in values) / len(values))**0.5
            }],
            "backgroundColor": "rgba(54, 162, 235, 0.2)",
            "borderColor": "rgba(54, 162, 235, 1)",
            "borderWidth": 1,
            "feature_details": [
                {
                    "name": fname,
                    "value": fval,
                    "interpretation": feature.interpretation,
                    "baseline_comparison": feature.baseline_comparison.dict() if feature.baseline_comparison and hasattr(feature.baseline_comparison, 'dict') else None
                }
                for fname, fval, feature in zip(feature_names, values, group.features)
            ]
        }
    return boxplot_data

def prepare_enhanced_chart_data(feature_groups: Dict[str, FeatureGroup]) -> Dict[str, Dict]:
    """Prepare comprehensive chart data for multiple visualization types"""
    chart_data = {
        "boxplot": prepare_boxplot_data(feature_groups),
        "comparison": {},
        "distribution": {},
        "correlation": {}
    }
    
    for group_name, group in feature_groups.items():
        ai_similarities = []
        human_similarities = []
        feature_names = []
        
        for feature in group.features:
            if feature.baseline_comparison:
                ai_similarities.append(feature.baseline_comparison.ai_similarity)
                human_similarities.append(feature.baseline_comparison.human_similarity)
                feature_names.append(feature.name)
        
        if ai_similarities and human_similarities:
            chart_data["comparison"][group_name] = {
                "labels": feature_names,
                "ai_similarities": ai_similarities,
                "human_similarities": human_similarities,
                "group_description": group.description
            }
    
    for group_name, group in feature_groups.items():
        values = [f.value for f in group.features]
        if values:
            chart_data["distribution"][group_name] = {
                "values": values,
                "labels": [f.name for f in group.features],
                "histogram_bins": 10,
                "group_score": group.group_score
            }
    
    return chart_data