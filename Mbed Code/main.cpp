
#include <stdio.h>
#include "mbed.h"
#include "rtos.h"
#include "ultrasonic.h"
#include "XNucleo53L0A1.h"
#include "Motor.h"

volatile int sonarDistance = 0;
volatile uint32_t ToFDistance = 0;
volatile int forward = 0;
volatile int backward = 0;
volatile int left = 0;
volatile int right = 0; 
volatile int forwardEnabled = 1;
volatile int backwardEnabled = 1;

Motor motor1(p23, p12, p8); // pwma, fwd (AIN1), rev (AIN2)
Motor motor2(p22, p11, p10); // pwmb, fwd (BIN1), rev (BIN2)

Serial pc(USBTX, USBRX); 

RawSerial  pi(USBTX, USBRX);

DigitalOut led1(LED1);

DigitalOut shdn(p26);
// This VL53L0X board test application performs a range measurement in polling mode
// Use 3.3(Vout) for Vin, p28 for SDA, p27 for SCL, P26 for shdn on mbed LPC1768

//I2C sensor pins
#define VL53L0_I2C_SDA   p28
#define VL53L0_I2C_SCL   p27

static XNucleo53L0A1 *board=NULL;

void dist(int distance)
{
    pc.printf("Back Distance %d mm\r\n", distance);
}

ultrasonic mu(p6, p7, .1, 1, &dist); // trig, echo, updateSpeed. timeout

void Sonar(void const *argument) {
    mu.startUpdates();
    while(1)
    {
        mu.checkDistance();
        sonarDistance = mu.getCurrentDistance();
        Thread::wait(500);
    }
}

void ToF(void const *argument) {
    int status;
    uint32_t distance;
    DevI2C *device_i2c = new DevI2C(VL53L0_I2C_SDA, VL53L0_I2C_SCL);
    /* creates the 53L0A1 expansion board singleton obj */
    board = XNucleo53L0A1::instance(device_i2c, A2, D8, D2);
    shdn = 0; //must reset sensor for an mbed reset to work
    Thread::wait(100);
    shdn = 1;
    Thread::wait(100);
    /* init the 53L0A1 board with default values */
    status = board->init_board();
    while (status) {
        pc.printf("Failed to init board! \r\n");
        status = board->init_board();
    }
    //loop taking and printing distance
    while (1) {
        status = board->sensor_centre->get_distance(&distance);
        if (status == VL53L0X_ERROR_NONE) {
            ToFDistance = distance;
            pc.printf("Front Distance=%ld mm\r\n", distance);
        }
        Thread::wait(500);
    }
}
 
void dev_recv()
{
    char temp = 0;
    led1 = !led1;
    while(pi.readable()) {
        temp = pi.getc();
        if (temp=='0') { // forward
            forward = 1; 
            backward = 0;
            left = 0;
            right = 0;
        } else if (temp=='1') { // backward
            forward = 0;
            backward = 1;
            left = 0;
            right = 0; 
        } else if (temp=='2') { // left
            forward = 0; 
            backward = 0;
            left = 1;
            right = 0;
        } else if (temp=='3') { // right
            forward = 0; 
            backward = 0;
            left = 0;
            right = 1; 
        } else if (temp=='4') { // no button pushed
            forward = 0; 
            backward = 0;
            left = 0;
            right = 0; 
        }
    }
}
void piControl(void const *args) {
    pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {
        sleep();
    }
}

int main() {
    Thread t1(Sonar);
    Thread t2(ToF);
    Thread t3(piControl);

    while(1) {
        if (ToFDistance <= 300 && sonarDistance <= 300) { // can only turn left or right
            forwardEnabled = 0;
            backwardEnabled = 0;
        } else if (ToFDistance <= 300 && sonarDistance > 300) { // backward, left, right enable
            forwardEnabled = 0;
            backwardEnabled = 1;
        } else if (ToFDistance > 300 && sonarDistance <= 300) { // forward, left, right enable
            forwardEnabled = 1;
            backwardEnabled = 0;
        } else { // forward, backward, left, right enable
            forwardEnabled = 1;
            backwardEnabled = 1;
        }

        if (forward && forwardEnabled) { // hold the forward button and no obstacles at the front
            motor1.speed(0.5);
            motor2.speed(0.5);
        } else if (backward && backwardEnabled) { // hold the backward button and no obstacles behind the car
            motor1.speed(-0.5);
            motor2.speed(-0.5);
        } else if (left) { // hold the left button
            motor1.speed(-0.4);
            motor2.speed(0.4);
        } else if (right) { // hold the right button
            motor1.speed(0.4);
            motor2.speed(-0.4);
        } else { // no buttons pushed (idle state)
            motor1.speed(0.0);
            motor2.speed(0.0);
        }
    }
}