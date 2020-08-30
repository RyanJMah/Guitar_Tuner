#ifndef FFT
#define FFT

#include <stdio.h>
#include <complex.h>
#include <math.h>

#define pi 3.141592653589793

////////////////////////////////////////////////////////////////////////////////////
// FUNCTION DECLARATIONS
void free_wrapper(float* x);

float magnitude(float complex z);
float* take_magnitude(float complex* Af, unsigned int size);

float complex* Hann(float* x, size_t size);

float complex* dft(float complex* At, unsigned int size);
float complex* fft_complex(float complex* At, unsigned int size);
float* fft(float* At, unsigned int size);

float* bins_to_freq(float sample_rate, unsigned int N);
////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////
// FUNCTION DEFINITIONS
void free_wrapper(float* x) { free(x); }

float* take_magnitude(float complex* Af, unsigned int size) {
	float* results = malloc(size*sizeof(float));
	for (unsigned int i = 0; i < size; i++) {
		results[i] = magnitude(Af[i]);
	}
	return results;
}

float magnitude(float complex z) { return sqrt(crealf(z)*crealf(z) + cimagf(z)*cimagf(z)); }



float complex* Hann(float* x, size_t size) {
	// has two roles: applies a Hanning window to samples in time-domain to make fft more clean
	// it also implicity casts samples "x" from floats to complex floats so it can be used in fft_complex

	float complex* Hann_x = malloc(size*sizeof(float complex));
	for (int i = 0; i < size; i++) {
	    float complex multiplier = (0.5*(1 - cos(2*pi*i/(size - 1)))) + 0.0*I;
	    Hann_x[i] = multiplier*x[i];
	}
	return Hann_x;
}



float complex* dft(float complex* At, unsigned int N) {
	float complex* Af = malloc(N*sizeof(float complex));

	for (unsigned int k = 0; k < N; k++) {
		
		float complex sum = 0.0 + 0.0*I;
		for (unsigned int n = 0; n < N; n++) {
			sum += At[n]*( ccosf((-2.0*pi*k*n)/N) + csinf((-2.0*pi*k*n)/N) );
		}
		Af[k] = sum;
	}

	return Af;
}

float complex* fft_complex(float complex* At, unsigned int N) {
	if (N == 1) {
		float complex* ret = malloc(sizeof(float complex));
		*ret = *At;
		return ret;
	}

	else {
		/////////////////////////////////////////////////////////////////////////
		// handles most of the recursion
		float complex even[N/2];
		float complex odd[N/2];

		// unsigned int j = 0;
		for (unsigned int i = 0; i < N/2; i += 2) {
			even[i/2] = At[i+1];
			odd[i/2] = At[i];
			// j += 1;
		}

		float complex* At_even = fft_complex(even, N/2);
		float complex* At_odd = fft_complex(odd, N/2);
		/////////////////////////////////////////////////////////////////////////
		// recombine odd and even
		float complex* Af_ret = malloc(N*sizeof(float complex));
		
		for (unsigned int k = 0; k < N/2; k++) {
			float complex W = cosf((-2*pi*k)/N) + sinf((-2*pi*k)/N)*I;

			Af_ret[k] = (At_even[k] + At_odd[k]*W);
			Af_ret[k+N/2] = (At_even[k] - At_odd[k]*W);
		}
		free(At_even);
		free(At_odd);

		At_even = NULL;
		At_odd = NULL;

		return Af_ret;
	}
}

float* fft(float* At, unsigned int N) {
	float complex* Hann_At = Hann(At, N);
	float complex* results = fft_complex(Hann_At, N);
	
	free(Hann_At);
	Hann_At = NULL;

	float* real_results = take_magnitude(results, N);
	free(results);
	results = NULL;

	return real_results;
}



float* bins_to_freq(float sample_rate, unsigned int N) {
	float* freqs = malloc(N*sizeof(float));
	for (unsigned int i = 0; i < N; i++) {
		freqs[i] = i*(sample_rate/N);
	}
	return freqs;
}

////////////////////////////////////////////////////////////////////////////////////

#endif

