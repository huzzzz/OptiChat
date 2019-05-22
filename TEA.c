#include <stdint.h>
#include <stdio.h>
#include <inttypes.h>

void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i < 32; i++) {                       /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

int main(){
    uint32_t x[2];
    uint32_t k[4];
    x[1] = 0xff7f5f1f;
    x[0] = 0x0f070301;
    printf("%" PRIu32 "\n",x[1]);
    printf("%" PRIu16 "\n",x[0]);
    k[0] = 0x2927c18c;
    k[3] = 0xff0f7457;
    k[2] = 0x43fd99f7;
    k[1] = 0x75f8c48f;
    encrypt(x,k);
    printf("%" PRIu32 "\n",x[1]);
    printf("%" PRIu16 "\n",x[0]);
    decrypt(x,k);

    printf("%" PRIu32 "\n",x[1]);
    printf("%" PRIu16 "\n",x[0]);
}