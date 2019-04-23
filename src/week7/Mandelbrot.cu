#include <iostream>
#include <math.h>
#include <cstdio>
#include <cstdint>
#include <cuda_profiler_api.h>

__global__
void mandelbrot(int x, int y, int steps, uint8_t *res)
{
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    int size = x * y;
    for (int i = index; i < size; i += stride) {
        float r0 = 3.0f * (i % x) / x - 2.0f;
        float c0 = 2.0f * (i / x) / y - 1.0f;
        float r = r0, c = c0;
        for (int step = 0; step < steps && r < 2 && r > -3 && c < 2 && c > -2; step++) {
            float r2 = r * r - c * c + r0;
            float c2 = 2 * r * c + c0;
            r = r2;
            c = c2;
        }
        if (r > 2 || r < -3 || c > 2 || c < -2) {
            res[i] = 255; 
        } 
    }
}

int main(int argc, char **args)
{
    if (argc != 4) {
        std::cerr << "Bad params" << std::endl;
        return 1;
    }
    int SCALE = atoi(args[1]);
    int STEPS = atoi(args[2]);
    char *OUT = args[3];
    int X = 3 * SCALE, Y = 2*SCALE;
    std::cerr << "Scale: " << SCALE << " (X = " << X << ", Y = " << Y << ")\nSteps: " << STEPS << "\nOutput file: " << OUT << std::endl;

    uint8_t *res;

    // Allocate Unified Memory – accessible from CPU or GPU
    cudaMalloc(&res, X*Y*sizeof(uint8_t));
    if (!res) {
        std::cerr << "Unable to allocate the memory" << std::endl;
        return 1;
    }
    cudaMemset(res, 0, X * Y * sizeof(uint8_t));

    // initialize x and y arrays on the host
    int blockSize = 256;
    int numBlocks = (X*Y + blockSize - 1) / blockSize;
    std::cerr << "blockSize " << blockSize << "numBlocks " << numBlocks << std::endl;
    mandelbrot<<<numBlocks, blockSize>>>(X, Y, STEPS, res);

    // Wait for GPU to finish before accessing on host
    cudaDeviceSynchronize();

    
    uint8_t *dataHost = (uint8_t *)malloc(X * Y * sizeof(uint8_t));
    cudaMemcpy(dataHost, res, X * Y * sizeof(uint8_t), cudaMemcpyDeviceToHost);
    cudaFree(res);
    FILE *output = fopen(OUT, "wb");
    std::cerr << "Writing" << sizeof(uint8_t) * X * Y << " bytes "<< std::endl;
    for (unsigned y = 0; y < Y; y++) {
        for (unsigned x = 0; x < X; x++) {
            fwrite(dataHost+y*X+x, 1, 1, output);
        }
    }
//    fwrite(res, sizeof(uint8_t), X * Y, output);
    std::cerr << "Closing" << std::endl;
    std::cout << "convert -size " << X << "x" << Y << " -depth 8 gray:" << OUT << " res.png" << std::endl;
    fclose(output);
    cudaProfilerStop(); 
    return 0;
}
