import math
import matplotlib.pyplot as plt
from typing import List, Tuple

class Rule345Transformer:
    """
    A robust implementation of the 3-4-5 Data Transformation Algorithm.
    Designed for Data Mining & Data Preparation workflows.
    """
    
    def __init__(self, data: List[float]):
        """Initializes the transformer with raw numerical data."""
        self.raw_data = data
        self.sorted_data = sorted(data)
        self.n = len(data)
        
        # Processed Results
        self.lower_tail: List[float] = []
        self.upper_tail: List[float] = []
        self.remaining_data: List[float] = []
        
        self.new_min: float = 0.0
        self.new_max: float = 0.0
        self.msd_unit: float = 0.0
        self.iv: int = 0
        self.num_groups: int = 0
        self.group_width: float = 0.0
        self.groups: List[Tuple[str, List[float]]] = []
        
    def _calculate_msd_unit(self, val: float) -> float:
        """Finds the Most Significant Digit (MSD) unit for a given value."""
        if val == 0:
            return 1.0
        return 10 ** math.floor(math.log10(abs(val)))

    def fit_transform(self) -> List[Tuple[str, List[float]]]:
        """
        Executes the 3-4-5 rule steps and returns the categorized data.
        Adheres to the unrounded splitting criterion for analytical precision.
        """
        # Step 1 & 2: Sort and trim 5% tails
        remove_count = round(self.n * 0.05)
        self.lower_tail = self.sorted_data[:remove_count]
        self.upper_tail = self.sorted_data[-remove_count:]
        self.remaining_data = self.sorted_data[remove_count:-remove_count]
        
        self.new_min = self.remaining_data[0]
        self.new_max = self.remaining_data[-1]
        
        # Step 3: Find MSD and calculate rounded boundaries
        msd_unit_max = self._calculate_msd_unit(self.new_max)
        msd_unit_min = self._calculate_msd_unit(self.new_min)
        self.msd_unit = max(msd_unit_max, msd_unit_min)
        
        rounded_min = math.floor(self.new_min / self.msd_unit) * self.msd_unit
        rounded_max = math.ceil(self.new_max / self.msd_unit) * self.msd_unit
        
        # Step 4: Calculate Interval Value (IV)
        self.iv = int((rounded_max - rounded_min) / self.msd_unit)
        
        # Step 5: Determine number of main groups based on 3-4-5 rule parameters
        if self.iv in [3, 6, 7, 9]:
            self.num_groups = 3
        elif self.iv in [2, 4, 8]:
            self.num_groups = 4
        elif self.iv in [1, 5, 10]:
            self.num_groups = 5
        else:
            self.num_groups = 5 # Default fallback
            
        # Splitting criterion (using exact min/max as shown in lecture examples)
        self.group_width = (self.new_max - self.new_min) / self.num_groups
        
        # Step 6: Construct the group intervals
        self.groups.append(("Lower 5% (Outliers)", self.lower_tail))
        
        current_val = self.new_min
        for i in range(self.num_groups):
            next_val = current_val + self.group_width
            
            # Inclusive lower bound for the first group, strictly greater for subsequent groups
            if i == 0:
                group_vals = [x for x in self.remaining_data if current_val <= x <= next_val]
            else:
                group_vals = [x for x in self.remaining_data if current_val < x <= next_val]
                
            label = f"[{current_val:.1f}, {next_val:.1f}]"
            self.groups.append((label, group_vals))
            current_val = next_val
            
        self.groups.append(("Upper 5% (Outliers)", self.upper_tail))
        return self.groups

    def generate_report(self) -> None:
        """Prints a highly polished terminal report of the algorithm's execution."""
        print("=" * 65)
        print(f"{'3-4-5 DATA TRANSFORMATION ALGORITHM REPORT':^65}")
        print("=" * 65)
        print(f"Total Records Processed : {self.n}")
        print(f"5% Trim Count           : {len(self.lower_tail)} records from each tail")
        print(f"New Minimum Value       : {self.new_min}")
        print(f"New Maximum Value       : {self.new_max}")
        print(f"Calculated MSD Unit     : {self.msd_unit}")
        print(f"Intervals Count (IV)    : {self.iv}")
        print("-" * 65)
        print(f"DECISION: IV = {self.iv} -> Splitting into {self.num_groups} main groups.")
        print(f"Splitting Criterion     : {self.group_width:.2f} (width per group)")
        print("-" * 65)
        
        print("\nFINAL GROUPINGS:")
        print(f"{'Group Interval / Label':<25} | {'Count':<7} | {'Percentage':<10}")
        print("-" * 65)
        
        total_items = 0
        for label, vals in self.groups:
            count = len(vals)
            pct = (count / self.n) * 100
            print(f"{label:<25} | {count:<7} | {pct:>5.1f}%")
            total_items += count
            
        print("-" * 65)
        status = "SUCCESS" if total_items == self.n else "FAILED"
        print(f"Validation Check: {total_items}/{self.n} items categorized. [Status: {status}]")
        print("=" * 65)

    def export_visualization(self, filename: str = "homework_chart.png") -> None:
        """Generates a professional-grade matplotlib chart for the grouped data."""
        # Use a clean, professional aesthetic
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(11, 6))
        
        labels = [g[0] for g in self.groups]
        counts = [len(g[1]) for g in self.groups]
        
        # Colors: Highlight outliers (red) differently from main groups (blue)
        colors = ['#e74c3c'] + ['#3498db'] * self.num_groups + ['#e74c3c']
        
        # Render bars with a distinct border and bring to front (zorder)
        bars = ax.bar(labels, counts, color=colors, edgecolor='black', linewidth=1.2, zorder=3)
        
        ax.set_title("3-4-5 Rule Data Distribution", fontsize=16, fontweight='bold', pad=15)
        ax.set_xlabel("Data Intervals / Groups", fontsize=12, fontweight='bold', labelpad=10)
        ax.set_ylabel("Frequency (Count)", fontsize=12, fontweight='bold', labelpad=10)
        
        # Formats and gridlines
        plt.xticks(rotation=25, ha='right', fontsize=10)
        plt.yticks(range(0, max(counts) + 3, 2))
        ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
        
        # Data labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.3, 
                    int(yval), ha='center', va='bottom', fontsize=11, fontweight='bold')
            
        # Add custom legend
        import matplotlib.patches as mpatches
        outlier_patch = mpatches.Patch(color='#e74c3c', label='Trimmed Tails (5%)')
        main_patch = mpatches.Patch(color='#3498db', label='Main Data Groups')
        ax.legend(handles=[outlier_patch, main_patch], loc='upper left', fontsize=10)

        plt.tight_layout()
        plt.savefig(filename, dpi=300) # High resolution for reports
        print(f"\n[SUCCESS] High-resolution chart exported to: '{filename}'")


if __name__ == "__main__":
    # The 60 dataset values provided in the homework
    homework_data = [
        -123, -121, -102, -94, -83, -77, -68, -65, -58, -57, -31, -27, -17, -17, -16,
        -12, -5, -5, 0, 13, 19, 49, 76, 91, 108, 116, 124, 128, 135, 147,
        152, 163, 186, 190, 203, 204, 222, 226, 233, 238, 249, 260, 270, 273, 275,
        298, 305, 308, 308, 315, 316, 327, 335, 336, 336, 345, 347, 351, 358, 367
    ]
    
    # 1. Initialize the Transformer
    transformer = Rule345Transformer(homework_data)
    
    # 2. Execute the Data Preparation steps
    transformer.fit_transform()
    
    # 3. Output results
    transformer.generate_report()
    transformer.export_visualization("homework_chart.png")
