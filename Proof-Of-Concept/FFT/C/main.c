#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <complex.h>

#include "FFT.h"

#define pi 3.141592653589793
#define len(a) (sizeof(a)/sizeof(*a))


void write_to_csv(char* path, float* data, unsigned int size) {
	FILE* f = fopen(path, "w");
	for(unsigned int i = 0; i < size; i++) {
		fprintf(f, "%.15f\n", data[i]);
	}

	fclose(f);
}

int generate_time_array(
	float t_start,
	float t_stop,
	float sample_rate,
	float* t_arr,
	unsigned int t_arr_size) {

	float t_step = 1/sample_rate;

	// printf("%d\n", (int) sizeof(t_arr));

	unsigned int i = 0;
	float t = t_start;
	while ((t < t_stop) && (i < t_arr_size)) {
		t_arr[i] = t;
		// printf("%d\n", i);
		t += t_step;
		i += 1;
	}
}


int main() {
	// printf("%d\n", (int)sizeof(int complex));
	// printf("%d\n", sizeof(float complex));
	unsigned int bins = 1024;

	float t_arr[bins];
	generate_time_array(0, 1, 1024*10, t_arr, len(t_arr));


	float freq = 1111;
	float complex x[bins];
	for (int t = 0; t < len(t_arr); t++) {
		x[t] = (sinf(2*pi*freq*t_arr[t]) + sin(2*pi*freq*3*t_arr[t]));
		// printf("%f + %fj\n", creal(f[t]), cimag(f[t]));
	}
	float complex* Hann_x;

			
	clock_t time = clock();

	float* thing;
	for (unsigned int i = 0; i < 100; i++) {
		Hann_x = Hann(x, bins);
		thing = fft(Hann_x, bins);
		free(thing);
		free(Hann_x);
	}
	
	
	time = clock() - time;
	float time_taken = ( (float)time )/CLOCKS_PER_SEC;
	time_taken /= 100;
	printf("time = %.15fms\n", time_taken*1E3);
		
	float complex* x_windowed = Hann(x, bins);
	float* results = fft(x_windowed, bins);



	// write_to_csv("/home/ryan/Desktop/shared/Personal/Guitar-Tuner-Project/src/FFT/Python/dft_data.csv", results, bins);	// ubuntu
	write_to_csv("C:\\shared\\Personal\\Guitar-Tuner-Project\\src\\Proof-Of-Concept\\FFT\\Python\\dft_data.csv", results, bins);	// windows



	// free(results);
    return 0;
}
