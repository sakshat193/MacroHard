"""
MacroHard Data Analyzer
Provides utilities for analyzing and visualizing data trends
"""

import json
from typing import List, Dict, Tuple
from dataclasses import dataclass
from statistics import mean, median, stdev


@dataclass
class DataPoint:
    label: str
    value: float


class DataAnalyzer:
    """Analyze numerical datasets and generate insights"""
    
    def __init__(self, data: List[DataPoint]):
        self.data = data
        self.values = [d.value for d in data]
    
    def get_statistics(self) -> Dict:
        """Calculate basic statistics"""
        if not self.values:
            return {}
        
        return {
            "count": len(self.values),
            "sum": sum(self.values),
            "mean": mean(self.values),
            "median": median(self.values),
            "min": min(self.values),
            "max": max(self.values),
            "range": max(self.values) - min(self.values),
            "stdev": stdev(self.values) if len(self.values) > 1 else 0
        }
    
    def find_outliers(self, threshold: float = 2.0) -> List[DataPoint]:
        """Find outliers using standard deviation"""
        if len(self.values) < 2:
            return []
        
        mean_val = mean(self.values)
        stdev_val = stdev(self.values)
        
        outliers = []
        for point in self.data:
            z_score = abs((point.value - mean_val) / stdev_val)
            if z_score > threshold:
                outliers.append(point)
        
        return outliers
    
    def sort_by_value(self, descending: bool = False) -> List[DataPoint]:
        """Sort data by value"""
        return sorted(self.data, key=lambda x: x.value, reverse=descending)
    
    def filter_range(self, min_val: float, max_val: float) -> List[DataPoint]:
        """Filter data within a range"""
        return [d for d in self.data if min_val <= d.value <= max_val]
    
    def percentage_change(self) -> Tuple[float, str]:
        """Calculate percentage change from first to last value"""
        if len(self.values) < 2:
            return 0.0, "N/A"
        
        first = self.values[0]
        last = self.values[-1]
        change = ((last - first) / first) * 100 if first != 0 else 0
        direction = "↑ Up" if change > 0 else "↓ Down"
        
        return change, direction
    
    def moving_average(self, window: int = 3) -> List[float]:
        """Calculate moving average"""
        if len(self.values) < window:
            return self.values
        
        return [
            mean(self.values[i:i+window])
            for i in range(len(self.values) - window + 1)
        ]
    
    def print_report(self):
        """Print analysis report"""
        stats = self.get_statistics()
        change, direction = self.percentage_change()
        outliers = self.find_outliers()
        
        print("\n" + "="*50)
        print("📊 DATA ANALYSIS REPORT")
        print("="*50)
        
        print(f"\n📈 Statistics:")
        print(f"  Count: {stats['count']}")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Median: {stats['median']:.2f}")
        print(f"  Min: {stats['min']:.2f}")
        print(f"  Max: {stats['max']:.2f}")
        print(f"  Std Dev: {stats['stdev']:.2f}")
        
        print(f"\n📉 Trend:")
        print(f"  Change: {change:.2f}% {direction}")
        
        if outliers:
            print(f"\n⚠️  Outliers Detected ({len(outliers)}):")
            for outlier in outliers:
                print(f"  - {outlier.label}: {outlier.value}")
        else:
            print(f"\n✅ No outliers detected")
        
        print("\n" + "="*50)


class DataProcessor:
    """Load and process data from various sources"""
    
    @staticmethod
    def from_list(labels: List[str], values: List[float]) -> DataAnalyzer:
        """Create analyzer from lists"""
        data = [DataPoint(label, value) for label, value in zip(labels, values)]
        return DataAnalyzer(data)
    
    @staticmethod
    def from_dict(data_dict: Dict[str, float]) -> DataAnalyzer:
        """Create analyzer from dictionary"""
        data = [DataPoint(label, value) for label, value in data_dict.items()]
        return DataAnalyzer(data)


# =====================================================
# EXAMPLE USAGE
# =====================================================
if __name__ == "__main__":
    # Sample sales data
    sales = {
        "January": 45000,
        "February": 52000,
        "March": 48000,
        "April": 61000,
        "May": 58000,
        "June": 72000,
        "July": 150000,  # Outlier - special campaign
        "August": 69000,
        "September": 77000,
    }
    
    analyzer = DataProcessor.from_dict(sales)
    analyzer.print_report()
    
    print("\n🔍 Top 3 Performers:")
    top_3 = analyzer.sort_by_value(descending=True)[:3]
    for point in top_3:
        print(f"  {point.label}: ${point.value:,}")
    
    print("\n📊 Moving Average (3-month):")
    ma = analyzer.moving_average(window=3)
    for i, avg in enumerate(ma, 1):
        print(f"  Period {i}: ${avg:,.0f}")
