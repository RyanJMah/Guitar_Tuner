#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdbool.h>
#include <math.h>
#include <complex.h>


/////////////////////////////////////////////////////////////////////////////
// FUNCTION DECLARATIONS
float* harmonic_product_spectrum(float* x, float* freqs, size_t N);

float* high_pass_filter(float* x, size_t N, size_t bin_cutoff);
double quadratic_interpolation(float alpha, float beta, float gamma);
/////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////
// FUNCTION DEFINITIONS
float* harmonic_product_spectrum(float* x,float* freqs, size_t N) {
	/*

	The formula for the harmonic product specturm is the following:

			             r=R
					   -------  /            \
				        |   |  |  |        |  |
				Y(f) =  |   |  |  | x(f*r) |  |
			            |   |  |  |        |  |
			             r=1    \            /

	Where x(f) a signal in frequency domain, R is the number of harmonics being considered,
	and Y(f) is the harmonic product spectrum of x(f).

	In terms of arrays, this can be translated into the following:

				Y[k] = x[k]x[2k]x[3k]...x[Rk]

	Henceforth, the fundamental frequency can then be approximated as:

				                    /      \                 -1
				f_fundamental = max|  f(Y)  |, where f(Y) = Y
                                    \      /

	I will apply the harmonic product spectrum for R = 5 times, as this is the most amount of harmonics
	that I've seen appear in the FFT, and will probably need to be fine-tuned

	*/

	float* Y = malloc(N*sizeof(float));
	for (size_t i = 0; (i < (N/5)); i++) {
		Y[i] = x[i]*x[i*2]*x[i*3]*x[i*4]*x[i*5];
	}

	for (size_t i = N/5; i < N; i++) {
		Y[i] = 0;
	}

	return Y;
}



float* high_pass_filter(float* x, size_t N, size_t bin_cutoff) {
	// applies a heaviside function as a high-pass filter
	float heaviside[N];
	for (size_t i = 0; i < bin_cutoff; i++) {
		heaviside[i] = 0;
	}
	for (size_t i = bin_cutoff; i < N; i++) {
		heaviside[i] = 1;
	}

	float* X = malloc(N*sizeof(float));
	for (size_t i = 0; i < N; i++) {
		X[i] = x[i]*heaviside[i];
	}
	return X;
}


double quadratic_interpolation(float alpha, float beta, float gamma) {
	// alpha is the bin before the peak, beta is the bin with the peak,
	// and gamma is the bin after the peak

	double p = 0.5*( (alpha - gamma)/(alpha - 2.0*beta + gamma) );
	return p;
}
/////////////////////////////////////////////////////////////////////////////


