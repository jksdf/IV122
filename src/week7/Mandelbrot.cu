#include <iostream>
#include <math.h>
#include <cstdio>
#include <cstdint>
#include <cuda_profiler_api.h>

#define MIN(X,Y) ((X) < (Y) ? (X) : (Y))

#define ull unsigned long long

__global__
void mandelbrot(ull x, ull y, int steps, uint8_t *res)
{
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    ull size = y * x/8;
    for (ull i = index; i < size; i += stride) {
        for (int bytepos = 0; bytepos < 8; bytepos++) {
            float r0 = 3.0f * ((i*8+bytepos) % x) / x - 2.0f;
            float c0 = 2.0f * ((i*8+bytepos) / x) / y - 1.0f;
            float r = r0, c = c0;
            for (int step = 0; step < steps && r < 2 && r > -3 && c < 2 && c > -2; step++) {
                float r2 = r * r - c * c + r0;
                float c2 = 2 * r * c + c0;
                r = r2;
                c = c2;
            }
            if (r > 2 || r < -3 || c > 2 || c < -2) {
                res[i] |= 0x80 >> bytepos;
            }
        }
    }
}

int main(int argc, char **args)
{
    if (argc != 4) {
        std::cerr << "Bad params" << std::endl;
        return 1;
    }
    cudaError_t error;
    int SCALE = atoi(args[1]);
    int STEPS = atoi(args[2]);
    char *OUT = args[3];
    ull X = 3 * SCALE, Y = 2*SCALE;
    if (X % 8 != 0) {
        std::cerr << "Scale has to be divisible by 8\n";
        return 1;
    }
    std::cerr << "Scale: " << SCALE << " (X = " << X << ", Y = " << Y << ")\nSteps: " << STEPS << "\nOutput file: " << OUT << std::endl;

    uint8_t *res;
    error = cudaMalloc(&res, X*Y*sizeof(uint8_t) / 8);
    if (!res || error == cudaErrorMemoryAllocation) {
        std::cerr << "Unable to allocate " << X*Y*sizeof(uint8_t)/8 << " bytes of GPU memory" << std::endl;
        return 1;
    }
    
    uint8_t *dataHost = (uint8_t *)malloc(X * Y * sizeof(uint8_t)/8);
    if (!dataHost) {
        std::cerr << "Not enough RAM" << std::endl;
        return 1;
    }

    FILE *output = fopen(OUT, "wb");

    std::cerr << "Writing" << sizeof(uint8_t) * X * Y /8 << " bytes "<< std::endl;
    cudaMemset(res, 0x0, X * Y * sizeof(uint8_t)/8);
    int blockSize = 256;
    int numBlocks = (X*Y + blockSize - 1) / blockSize;
    mandelbrot<<<numBlocks, blockSize>>>(X, Y, STEPS, res);
    cudaDeviceSynchronize();
    cudaMemcpy(dataHost, res, X * Y * sizeof(uint8_t)/8, cudaMemcpyDeviceToHost);
    fwrite(dataHost, sizeof(uint8_t), X*Y/8, output);
    
    
    cudaFree(res);
    std::cerr << "Closing" << std::endl;
    std::cout << "convert -size " << X << "x" << Y << " -depth 1 -define png:compression-strategy=3 gray:" << OUT << " res.png" << std::endl;
    fclose(output);
    cudaProfilerStop(); 
    return 0;
}
