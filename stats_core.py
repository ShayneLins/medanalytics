import numpy as np
import scipy as sp
import scipy.stats as stats
from model import ResponseData, ChartData


def parse_input(request):
    """ Function to parse gRPC input to Python data
    - Return (xarray, yarray)
     - xarray: [[1,2,3], [2,3,4]...], for different Xs, each X is an array of numbers. Or None
     - yarray: similar to xarray or None
    """
    return (request.x, request.y)


def cal_basic_statistics(request):
    """
    The module is to calculate the basic statistics summarize of the data
    """
    # extract input data
    xarrays, _ = parse_input(request)
    trows = []
    boxplots = []
    for xs in xarrays:
        # build table data
        xmean = np.mean(xs)
        xstd = np.std(xs)
        xmin = np.min(xs)
        xmax = np.max(xs)
        x25 = np.percentile(xs, 25)
        x50 = np.percentile(xs, 50)
        x75 = np.percentile(xs, 75)
        trows.append([xmean, xstd, xmin, x25, x50, x75, xmax])
        # boxplot data
        boxplots.append([xmin, x25, x50, x75, xmax])
    # compose table data
    chart1 = ChartData(chartId=0, yaxis=['均值', '标准差', '最小值', '25分位值', '50分位值', '75分位值', '最大值'], y=trows)
    # compose boxplot data
    chart2 = ChartData(chartId=4, y=boxplots)
    # composite result data
    result = ResponseData(total=2, info='ok', chartArray=[chart1, chart2])
    return result


def cal_test_of_normality(request):
    """
    The module is to test whether the data follows normal distribution.
    - Calculate skewness and kurtosis (偏度和峰度), calculate the Sharpiro-Wilk Test if the size of data
      set is less then 5000, otherwise calculate the Kolmogorov Test.
    - Give the judgement based on the result
    - cdf to draw the CDF plot of data
    Input:  request as stats.proto.ComputeRequest
    Return: chart_id = 0 for table. Each dataset has a chart_id=2 plot data
    """
    xarrays, _ = parse_input(request)
    is_norm = []
    for xs in xarrays:
        skew = stats.skew(xs)
        kurtosis = stats.kurtosis(xs)

        if len(xs) >= 5000:
            test_res = stats.kstest(xs, 'norm')
        else:
            test_res = stats.shapiro(xs)
        is_norm.append([test_res, skew, kurtosis])

    result = stats_pb2.ComputeResponse()
    result.total = 1
    chart_data1 = result.chart_data_array.add()
    chart_data1.chart_id = 0
    chart_data1.yaxis.extend(['是否正态分布', '偏度', '峰度', '样本数', '检验', 'p-value'])
    chart_data1.yarray.extend(is_norm)
    return result


def cal_test_relative(request):
    """
    The module calculate 
    https://zhuanlan.zhihu.com/p/343361192
    """
    xarray, yarray = parse_input(request)


def cal_significant_test(request):
    """
    https://baike.baidu.com/item/显著性/10211648
    """
    xarray, yarray = parse_input(request)