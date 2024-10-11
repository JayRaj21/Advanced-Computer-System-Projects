include <iostream>
#include <vector>
#include <thread>
#include <immintrin.h>
#include <omp.h>

using namespace std;

typedef vector<vector<double>> Matrix; //defining Matrix object


const int BLOCK_SIZE = 64; // blocking size for cache optimization

// Function to perform blocked matrix multiplication (cache-optimized)
void matrixMultBlock(const Matrix &A, const Matrix &B, Matrix &C, bool simdEnabled) {
    int n = A.size();
    for (int ii = 0; ii < n; ii += BLOCK_SIZE) {
        for (int jj = 0; jj < n; jj += BLOCK_SIZE) {
            for (int kk = 0; kk < n; kk += BLOCK_SIZE) {
                for (int i = ii; i < min(ii + BLOCK_SIZE, n); ++i) {
                    for (int j = jj; j < min(jj + BLOCK_SIZE, n); ++j) {
                        double sum = 0.0;
                        if (simdEnabled) {
                            __m256d vectorSum = _mm256_setzero_pd();
                            for (int k = kk; k < min(kk + BLOCK_SIZE, n); k += 4) {
                                __m256d vectorA = _mm256_loadu_pd(&A[i][k]);
                                __m256d vectorB = _mm256_loadu_pd(&B[k][j]);
                                vectorSum = _mm256_fmadd_pd(vectorA, vectorB, vectorSum);
                            }
                            double temp[4];
                            _mm256_storeu_pd(temp, vectorSum);
                            sum = temp[0] + temp[1] + temp[2] + temp[3];
                        } else {
                            for (int k = kk; k < min(kk + BLOCK_SIZE, n); ++k) {
                                sum += A[i][k] * B[k][j];
                            }
                        }
                        C[i][j] += sum;
                    }
                }
            }
        }
    }
}

// Function to perform matrix multiplication without cache blocking
void matrixMultBasic(const Matrix &A, const Matrix &B, Matrix &C, bool simdEnabled) {
    int n = A.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            if (simdEnabled) {
                __m256d vectorSum = _mm256_setzero_pd();
                for (int k = 0; k < n; k += 4) {
                    __m256d vectorA = _mm256_loadu_pd(&A[i][k]);
                    __m256d vectorB = _mm256_loadu_pd(&B[k][j]);
                    vectorSum = _mm256_fmadd_pd(vectorA, vectorB, vectorSum);
                }
                double temp[4];
                _mm256_storeu_pd(temp, vectorSum);
                sum = temp[0] + temp[1] + temp[2] + temp[3];
            } else {
                for (int k = 0; k < n; ++k) {
                    sum += A[i][k] * B[k][j];
                }
            }
            C[i][j] += sum;
        }
    }
}

// Multi-threaded matrix multiplication
void matrixMultThreaded(const Matrix &A, const Matrix &B, Matrix &C, bool cacheOptimized, bool simdEnabled, int numThreads) {
    int n = A.size();
    omp_set_num_threads(numThreads);
    #pragma omp parallel for
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = 0.0;
        }
    }
    
    #pragma omp parallel for
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (cacheOptimized) {
                matrixMultBlock(A, B, C, simdEnabled);
            } else {
                matrixMultBasic(A, B, C, simdEnabled);
            }
        }
    }
}

// Function to generate a matrix of given size
Matrix generateMatrix(int size, bool sparse = false) {
    Matrix mat(size, vector<double>(size, 0.0));
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            if (sparse) {
                if (rand() % 10 < 2) {  // chekcs for 20% sparsity
                    mat[i][j] = rand() % 10 + 1;
                }
            } else {
                mat[i][j] = rand() % 10 + 1;
            }
        }
    }
    return mat;
}

// Driver function for matrix multiplication with optional configurations
void multiplyMatrices(Matrix &A, Matrix &B, Matrix &C, bool multithreading, bool simdEnabled, bool cacheOptimized, int numThreads) {
    if (multithreading) {
        matrixMultThreaded(A, B, C, cacheOptimized, simdEnabled, numThreads);
    } else {
        if (cacheOptimized) {
            matrixMultBlock(A, B, C, simdEnabled);
        } else {
            matrixMultBasic(A, B, C, simdEnabled);
        }
    }
}

int main(int argc, char* argv[]) {
    int matrixSize = 1024;
    bool useMultithreading = false;
    bool useSimd = false;
    bool useCacheOptimization = false;
    int numThreads = 1;

    // Parsing command-line arguments for enabling and disabling optimizations
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if (arg == "--multithreading") {
            useMultithreading = true;
        } else if (arg == "--simd") {
            useSimd = true;
        } else if (arg == "--cache") {
            useCacheOptimization = true;
        } else if (arg == "--threads") {
            if (i + 1 < argc) {
                numThreads = stoi(argv[++i]);
            }
        } else if (arg == "--size") {
            if (i + 1 < argc) {
                matrixSize = stoi(argv[++i]);
            }
        }
    }

    // Generating test matrices
    Matrix A = generateMatrix(matrixSize);
    Matrix B = generateMatrix(matrixSize);
    Matrix C(matrixSize, vector<double>(matrixSize, 0.0));

    // Perform matrix multiplication with specified optimizations
    multiplyMatrices(A, B, C, useMultithreading, useSimd, useCacheOptimization, numThreads);

    cout << "Matrix multiplication completed with size: " << matrixSize << endl;
    return 0;
}