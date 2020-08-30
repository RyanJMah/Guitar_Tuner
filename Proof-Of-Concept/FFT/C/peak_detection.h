#ifndef PEAK_DETECTION
#define PEAK_DETECTION

#include <stdio.h>
#include <math.h>
#include <complex.h>
#include <stdbool.h>


/////////////////////////////////////////////////////////////////////////////
// FUNCTION DECLARATIONS
double quadratic_interpolation(float alpha, float beta, float gamma);
double get_fundamental_freq(float* x, float* freqs, size_t N, float threshold);
/////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////
// FUNCTION DEFINITIONS
double quadratic_interpolation(float alpha, float beta, float gamma) {
	double p = 0.5*( (alpha - gamma)/(alpha - 2.0*beta + gamma) );
	return p;
}

double get_fundamental_freq(float* x, float* freqs, size_t N, float threshold) {
	for (size_t i = 1; i < N; i++) {
		float alpha = x[i-1];
		float beta = x[i];
		float gamma = x[i+1];

		bool found = (abs(alpha - beta) > threshold) &&
				  	 (abs(beta - gamma) > threshold) &&
				  	 (alpha < beta) &&
					 (beta > gamma);

		if (found) {
			// printf("i = %d\n", i);
			return freqs[i] + quadratic_interpolation(alpha, beta, gamma);
		}
	}
}
/////////////////////////////////////////////////////////////////////////////


#endif
