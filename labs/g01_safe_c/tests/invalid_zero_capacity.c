#include "g01_lab.h"

G01_DECLARE_QUEUE(invalid_queue, 0);

int main(void) {
    return (int)invalid_queue.count;
}
