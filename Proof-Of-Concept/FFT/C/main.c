#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <complex.h>

#include "FFT.h"
#include "peak_detection.h"

#define pi 3.141592653589793
#define len(a) (sizeof(a)/sizeof(*a))


void write_to_csv(char* path, float* data, size_t size) {
	FILE* f = fopen(path, "w");
	for(size_t i = 0; i < size; i++) {
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
	unsigned int bins = pow(2, 15);
	unsigned int sample_rate = 44.1E3;

	float t_arr[bins];
	generate_time_array(0, 5, sample_rate, t_arr, len(t_arr));


	float freq = 440;
	float complex x[bins];
	for (int t = 0; t < len(t_arr); t++) {
		x[t] = (sin(2*pi*freq*t_arr[t]) + sin(2*pi*freq*3*t_arr[t]) + sin(pi*freq*t_arr[t]));
	}

	float* freq_bins = bins_to_freq(sample_rate, bins);
	// clock_t time = clock();

	// float* thing;
	// for (unsigned int i = 0; i < 100; i++) {
	// 	thing = fft(x, bins, 100);
	// 	free(thing);
	// }
		
	// time = clock() - time;
	// float time_taken = ( (float)time )/CLOCKS_PER_SEC;
	// time_taken /= 100;
	// printf("time = %.15fms\n", time_taken*1E3);
		

	float* results = fft(x, bins, 100);
	double fundamental = get_fundamental_freq(results, freq_bins, bins, 3.0);

	printf("fundamental freq = %f Hz\n", fundamental);


	// write_to_csv("/home/ryan/Desktop/shared/Personal/Guitar-Tuner-Project/src/FFT/Python/dft_data.csv", results, bins);	// ubuntu
	write_to_csv("C:\\shared\\Personal\\Guitar-Tuner-Project\\src\\Proof-Of-Concept\\FFT\\Python\\dft_data.csv", results, bins);	// windows



	free(results);
    return 0;
}
