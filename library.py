import pandas as pd
import numpy as np

from datetime import datetime
from scipy import stats
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm

# Create Platform Categories for better understanding our data:
# platforms = {'Playstation : [PS, PS2, PS3, PS4],
#             Xbox : [XB, X360, XOne], 
#             PC : [PC],
#             Nintendo : [Wii, WiiU],
#             Portable : [GB, GBA, GC, DS, 3DS, PSP, PSV]}

# Playstation     == 1
# Xbox            == 2
# PC              == 3
# Nintendo        == 4
# Portable        == 5


def platforms(platform):
    if platform in ['PS', 'PS2', 'PS3', 'PS4']:
        return 1
    elif platform in ['XB', 'X360', 'XOne']:
        return 2
    elif platform in ['PC']:
        return 3
    elif platform in ['Wii', 'WiiU']:
        return 4
    else:
        return 5
    

# Calculate Welch's t-statistic for two samples
# control-->shooter 
# sports-->treatment

def welch_t(a, b):

    numerator = a.mean() - b.mean()
    
    # “ddof = Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof, 
    #  where N represents the number of elements. By default ddof is zero.
    
    denominator = np.sqrt(a.var(ddof=1)/a.size + b.var(ddof=1)/b.size)
    
    return np.abs(numerator/denominator)



# Calculate the effective degrees of freedom for two samples
def welch_df(a, b):
    
    s1 = a.var(ddof=1) 
    s2 = b.var(ddof=1)
    n1 = a.size
    n2 = b.size
    
    numerator = (s1/n1 + s2/n2)**2
    denominator = (s1/ n1)**2/(n1 - 1) + (s2/ n2)**2/(n2 - 1)
    
    return numerator/denominator



# Calculate p-value
def p_value(a, b, two_sided=False):

    t = welch_t(a, b)
    df = welch_df(a, b)
    
    p = 1-stats.t.cdf(np.abs(t), df)
    
    if two_sided:
        return 2*p
    else:
        return p
    
    
# Calculate Cohen's d
def Cohen_d(shooter, sports):

    # Compute Cohen's d.

    # group1: Series or NumPy array
    # group2: Series or NumPy array

    # returns a floating point number 

    diff = shooter.mean() - sports.mean()

    n1, n2 = len(shooter), len(sports)
    var1 = shooter.var()
    var2 = sports.var()

    # Calculate the pooled threshold as shown earlier
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_var)
    
    return d


# Calculate effect size
def effect_size(shooter, sports):
    e = shooter.mean()-sports.mean()
    
    return e
    
    
# calculate PDF    
def evaluate_PDF(rv, x=4):
    '''Input: a random variable object, standard deviation
    output : x and y values for the normal distribution
    '''
    
    # Identify the mean and standard deviation of random variable 
    mean = rv.mean()
    std = rv.std()

    # Use numpy to calculate evenly spaced numbers over the specified interval (4 sd) and generate 100 samples.
    xs = np.linspace(mean - x*std, mean + x*std, 100)
    
    # Calculate the peak of normal distribution i.e. probability density. 
    ys = rv.pdf(xs)

    return xs, ys # Return calculated values   


# Overlap
def overlap_superiority(shooter, sports, n=1000):
    """Estimates overlap and superiority based on a sample.
    
    group1: scipy.stats rv object
    group2: scipy.stats rv object
    n: sample size
    """

    # Get a sample of size n from both groups
    shooter_sample = shooter.rvs(n)
    sports_sample = sports.rvs(n)
    
    # Identify the threshold between samples
    thresh = (shooter.mean() + sports.mean()) / 2
    print(thresh)
    
    # Calculate no. of values above and below for group 1 and group 2 respectively
    above = sum(shooter_sample < thresh)
    below = sum(sports_sample > thresh)
    
    # Calculate the overlap
    overlap = (above + below) / n
    
    # Calculate probability of superiority
    superiority = sum(x > y for x, y in zip(shooter_sample, sports_sample)) / n

    return overlap, superiority


# Plot PDF
def plot_pdfs(cohen_d=1.4):
    """Plot PDFs for distributions that differ by some number of stds.
    
    cohen_d: number of standard deviations between the means
    """
    shooter = scipy.stats.norm(0, 1)
    sports = scipy.stats.norm(cohen_d, 1)
    xs, ys = evaluate_PDF(shooter)
    plt.fill_between(xs, ys, label='shooter', color='#ff2289', alpha=0.7)

    xs, ys = evaluate_PDF(sports)
    plt.fill_between(xs, ys, label='sports', color='#376cb0', alpha=0.7)
    
    o, s = overlap_superiority(shooter, sports)
    print('overlap', o)
    print('superiority', s)
# use library.plot_pdfs(5)    


