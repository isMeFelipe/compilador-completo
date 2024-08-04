#include <iostream>
using namespace std;

int main() {
int i;
int i2;
i2 = 1;
L1:
cout << i;
i = i + 1;

if (((i == 10))) goto L2;
goto L1;
L2:


return 0;
}