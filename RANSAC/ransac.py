    # _*_ coding:utf-8 _*_
     
    import numpy as np
    import scipy as sp
    import scipy.linalg as sl
     
    # ransac_fit, ransac_data = ransac(all_data, model, 50, 1000, 7e3, 300, debug=debug, return_all=True)
    def ransac(data, model, n, k, t, d, debug=False, return_all=False):
        '''
        Reference: http://scipy.github.io/old-wiki/pages/Cookbook/RANSAC
             Pseudo code: http://en.wikipedia.org/w/index.php?title=RANSAC&oldid=116358182
             Enter:
                     Data - sample point
                     Model - hypothetical model: determine in advance
                     n - the minimum number of sample points required to generate the model
                     k - the maximum number of iterations
                     t - threshold: as a criterion to satisfy the condition of the model
                     d - the minimum number of sample points required when fitting is good, as a threshold
             Output:
                     Bestfit - best fit solution (return nil if not found)
        iterations = 0
             Bestfit = nil # 
             Besterr = something really large #late update besterr = thiserr
        while iterations < k
        {
                     Maybeinliers = randomly select n from the sample, not necessarily all in-house points, or even all out-of-office points
                     Maybemodel = n maybeinliers fitted models that may meet the requirements
                     Alsoinliers = emptyset #sample points that meet the error requirements, start blanking
                     For (each one is not a sample point of maybeinliers)
            {
                             If it satisfies maybemodel ie error < t
                                     Add points to alsoinliers
            }
                     If (alsoinliers number of sample points > d)
            {
                             % has a good model, test model conformity
                             Bettermodel = Regenerate better models with all maybeinliers and alsoinliers
                             Thiserr = error metric for all maybeinliers and alsoinliers sample points
                if thiserr < besterr
                {
                    bestfit = bettermodel
                    besterr = thiserr
                }
            }
            iterations++
        }
        return bestfit
        '''
        iterations = 0
        bestfit = None
             Besterr = np.inf # set default
        best_inlier_idxs = None
        while iterations < k:
            maybe_idxs, test_idxs = random_partition(n, data.shape[0])
                     Maybe_inliers = data[maybe_idxs, :] # Get size(maybe_idxs) line data (Xi, Yi)
                     Test_points = data[test_idxs] # several rows (Xi, Yi) data points
                     Maybemodel = model.fit(maybe_inliers) # fitted model
                     Test_err = model.get_error(test_points, maybemodel) # Calculation error: minimum sum of squares
            also_idxs = test_idxs[test_err < t]
            also_inliers = data[also_idxs, :]
            if debug:
                print ('test_err.min()', test_err.min())
                print ('test_err.max()', test_err.max())
                print ('numpy.mean(test_err)', numpy.mean(test_err))
                print ('iteration %d:len(alsoinliers) = %d' % (iterations, len(also_inliers)))
            if len(also_inliers > d):
                             Betterdata = np.concatenate((maybe_inliers, also_inliers)) #sample connection
                bettermodel = model.fit(betterdata)
                better_errs = model.get_error(betterdata, bettermodel)
                             Thiserr = np.mean(better_errs) # Average error as a new error
                if thiserr < besterr:
                    bestfit = bettermodel
                    besterr = thiserr
                                     Best_inlier_idxs = np.concatenate((maybe_idxs, also_idxs)) # Update the in-office points and add new points
     
            iterations += 1
        if bestfit is None:
            raise ValueError("did't meet fit acceptance criteria")
        if return_all:
            return bestfit, {'inliers': best_inlier_idxs}
        else:
            return bestfit
     
     
    def random_partition(n, n_data):
        """return n random rows of data and the other len(data) - n rows"""
             All_idxs = np.arange(n_data) # Get the n_data subscript index
             Np.random.shuffle(all_idxs) # disrupt the subscript index
        idxs1 = all_idxs[:n]
        idxs2 = all_idxs[n:]
        return idxs1, idxs2
     
     
    class LinearLeastSquareModel:
             # least squares to find a linear solution for the input model of RANSAC
        def __init__(self, input_columns, output_columns, debug=False):
            self.input_columns = input_columns
            self.output_columns = output_columns
            self.debug = debug
     
        def fit(self, data):
                     A = np.vstack([data[:, i] for i in self.input_columns]).T #First column Xi-->Line Xi
                     B = np.vstack([data[:, i] for i in self.output_columns]).T #Second column Yi-->Line Yi
                     x, resids, rank, s = sl.lstsq(A, B) # residues: residuals and
                     Return x # return the least squares vector
     
        def get_error(self, data, model):
                     A = np.vstack([data[:, i] for i in self.input_columns]).T #First column Xi-->Line Xi
            B = np.vstack([data[:, i] for i in self.output_columns]).T #Second column Yi-->Line Yi
                     B_fit = sp.dot(A, model) # Calculated y value, B_fit = model.k*A + model.b
            err_per_point = np.sum((B - B_fit) ** 2, axis=1)  # sum squared error per row
            return err_per_point
     
     
    def test():
             # Generate ideal data
             N_samples = 500 # number of samples
             N_inputs = 1 # Enter the number of variables
             N_outputs = 1 # number of output variables
             A_exact = 20 * np.random.random((n_samples, n_inputs)) # Randomly generate 500 data between 0-20: row vector
             Perfect_fit = 60 * np.random.normal(size=(n_inputs, n_outputs)) # Random linearity is a random slope
        B_exact = sp.dot(A_exact, perfect_fit)  # y = x * k
     
             # , least squares can be handled very well
             A_noisy = A_exact + np.random.normal(size=A_exact.shape) # 500 * 1 line vector, representing Xi
             B_noisy = B_exact + np.random.normal(size=B_exact.shape) # 500 * 1 line vector, representing Yi
     
        if 1:
                     # Add "outside point"
            n_outliers = 100
                     All_idxs = np.arange(A_noisy.shape[0]) # Get index 0-499
                     Np.random.shuffle(all_idxs) # upset all_idxs
                     Outlier_idxs = all_idxs[:n_outliers] # 100 0-500 random outliers
                     A_noisy[outlier_idxs] = 20 * np.random.random((n_outliers, n_inputs)) # Add noise and extra point of Xi
                     B_noisy[outlier_idxs] = 50 * np.random.normal(size=(n_outliers, n_outputs)) # Add noise and Yi of the outlier
        # setup model
             All_data = np.hstack((A_noisy, B_noisy)) # Form ([Xi,Yi]....) shape:(500,2)500 rows and 2 columns
             Input_columns = range(n_inputs) # The first column of the array x:0
             Output_columns = [n_inputs + i for i in range(n_outputs)] # Array last column y:1
        debug = False
             Model = LinearLeastSquareModel(input_columns, output_columns, debug=debug) # Instantiation of class: Generating known models with least squares
     
        linear_fit, resids, rank, s = sp.linalg.lstsq(all_data[:, input_columns], all_data[:, output_columns])
     
             # run RANSAC algorithm
        ransac_fit, ransac_data = ransac(all_data, model, 100, 1e4, 7, 30, debug=debug, return_all=True)
        # ransac_fit, ransac_data = ransac(all_data, model, 100, 1e4, 0.01, 30, debug=debug, return_all=True)
        '''
             Enter:
             Data - sample point
             Model - hypothetical model: determine in advance
             n - the minimum number of sample points required to generate the model
             k - the maximum number of iterations
             t - threshold: as a criterion to satisfy the condition of the model
             d - the minimum number of sample points required when fitting is good, as a threshold
             Output:
             Bestfit - best fit solution (return nil, if not found)
        '''
     
        if 1:
            import pylab
     
            sort_idxs = np.argsort(A_exact[:, 0])
                     A_col0_sorted = A_exact[sort_idxs] # Array of rank 2
     
            if 1:
                             Pylab.plot(A_noisy[:, 0], B_noisy[:, 0], 'k.', label='data') # scatter plot
                pylab.plot(A_noisy[ransac_data['inliers'], 0], B_noisy[ransac_data['inliers'], 0], 'bx',
                           label="RANSAC data")
            else:
                pylab.plot(A_noisy[non_outlier_idxs, 0], B_noisy[non_outlier_idxs, 0], 'k.', label='noisy data')
                pylab.plot(A_noisy[outlier_idxs, 0], B_noisy[outlier_idxs, 0], 'r.', label='outlier data')
     
            pylab.plot(A_col0_sorted[:, 0],
                       np.dot(A_col0_sorted, ransac_fit)[:, 0],
                       label='RANSAC fit')
            pylab.plot(A_col0_sorted[:, 0],
                       np.dot(A_col0_sorted, perfect_fit)[:, 0],
                       label='perfect fit')
            pylab.plot(A_col0_sorted[:, 0],
                       np.dot(A_col0_sorted, linear_fit)[:, 0],
                       label='linear fit')
            pylab.legend()
            pylab.show()
     
     
    if __name__ == "__main__":
        test()