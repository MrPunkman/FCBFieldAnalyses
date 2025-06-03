import numpy as np

class DataSeries:
    def __init__(self, time, data, name="Unnamed Series"):
        self.name = name
        self.data_series = {t: d for t, d in zip(time, data)}
        self.length = len(self.data_series)
        # self.mean_value = self.calculate_mean()
        # self.std = self.calculate_std()
        # self.filtered_data = self._calculate_filtered_data()
        # self.filtered_series = None  # Placeholder for filtered DataSeries
    
    def calculate_mean(self):
        values = list(self.data_series.values())
        self.mean_value = np.mean(values)
        return self.mean_value

    def calculate_std(self):
        self.std = np.std(list(self.data_series.values())) if self.length > 0 else None
        return self.std

    def get_Value(self, i):
        return list(self.data_series.values())[i]

    def calculate_outliers(self, threshold=1):
        """
        Identifies outliers based on the standard deviation method.
        Any data point beyond 'threshold' standard deviations from the mean is considered an outlier.
        """
        if self.length == 0:
            return {}
        if not hasattr(self, 'mean_value'):
            self.calculate_mean()
        if not hasattr(self, 'std'):
            self.calculate_std()

        outliers = {t: d for t, d in self.data_series.items() if abs(d - self.mean_value) > threshold * self.std}
        return outliers
    
    def _calculate_filtered_data(self, threshold=1):
        """
        Returns a dictionary with outliers removed.
        """
        if self.length == 0:
            return {}
        
        if not hasattr(self, 'mean_value'):
            self.calculate_mean()
        if not hasattr(self, 'std'):
            self.calculate_std()
        
        return {t: d for t, d in self.data_series.items() if abs(d - self.mean_value) <= threshold * self.std}
    
    def get_filtered_series(self, threshold=1):
        """
        Returns a new DataSeries object with outliers removed, based on the given threshold.
        """
        filtered_data = self._calculate_filtered_data(threshold)
        return DataSeries(list(filtered_data.keys()), list(filtered_data.values()), name=f"{self.name} - Filtered ({threshold} SD)")
    
    def get_series_in_time_span(self, start_time, end_time):
        """
        Returns a new DataSeries object containing only the data within the specified time span,
        with recalculated mean and standard deviation.
        """
        filtered_data = {t: d for t, d in self.data_series.items() if start_time <= t <= end_time}
        if not filtered_data:
            return DataSeries([], [], name=f"{self.name} - Time Span {start_time}-{end_time}")
        
        # Recalculate mean and std for the new series within the time range
        return DataSeries(list(filtered_data.keys()), list(filtered_data.values()), name=f"{self.name} - Time Span {start_time}-{end_time}")
    
    def clone_with_new_data(self, new_data):
        """Returns a new DataSeries object with the given cropped data."""
        return DataSeries(self.name, new_data)


# Example usage:
# time_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# data_values = [10, 12, 13, 11, 15, 14, 200, 16, 17, 12]  # 200 is an outlier

# data_series = DataSeries(time_series, data_values)
# print("Length:", data_series.length)
# print("Mean Value:", data_series.calculate_mean())
# print("Standard Deviation:", data_series.std)
# print("Outliers:", data_series.calculate_outliers())
# filtered_series = data_series.get_filtered_series()
# print("Filtered Data Series Length:", filtered_series.length)
# time_span_series = data_series.get_series_in_time_span(3, 7)
# print("Time Span Data Series Length:", time_span_series.length)
# print("Time Span Mean:", time_span_series.mean_value)
# print("Time Span Standard Deviation:", time_span_series.std)
# time_span_series_filtered = time_span_series.get_filtered_series()
# print("Time Span Data Series Length:", time_span_series_filtered.length)
# print("Time Span Mean:", time_span_series_filtered.mean_value)
# print("Time Span Standard Deviation:", time_span_series_filtered.std)
